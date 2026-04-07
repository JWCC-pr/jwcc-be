import mimetypes
import time
from urllib.parse import quote, unquote

from django.utils.text import get_valid_filename
from storages.backends.s3boto3 import S3Boto3Storage


class DefaultMediaStorage(S3Boto3Storage):
    location = ""

    def url(self, name, format=None, **kwargs):
        return unquote(super().url(name, format, **kwargs))

    def generate_presigned_post(self, name, is_download=False):
        # 파일명에서 공백 등 특수문자를 _로 변환
        parts = name.rsplit("/", 1)
        raw_file_name = parts[-1]
        file_name = get_valid_filename(raw_file_name)
        name = f"{parts[0]}/{file_name}" if len(parts) > 1 else file_name

        # 경로에 타임스탬프 디렉토리를 추가하여 파일명 충돌 방지 (랜덤 suffix 대신)
        ts = str(int(time.time() * 1000))
        parts_path = name.rsplit("/", 1)
        if len(parts_path) > 1:
            object_key = f"{parts_path[0]}/{ts}/{parts_path[1]}"
        else:
            object_key = f"{ts}/{name}"
        encoded_filename = quote(file_name)

        content_type, _ = mimetypes.guess_type(object_key)
        if content_type is None:
            content_type = "application/octet-stream"  # 기본값
        fields = {
            "Content-Type": content_type,
        }
        conditions = [
            {"Content-Type": content_type},
            ["content-length-range", 0, 100 * 1024 * 1024],
        ]  # 100MB

        if is_download:
            fields.update(
                {"Content-Disposition": f"attachment; filename=\"{file_name}\"; filename*=UTF-8''{encoded_filename}"}
            )
            conditions.append(
                {"Content-Disposition": f"attachment; filename=\"{file_name}\"; filename*=UTF-8''{encoded_filename}"}
            )

        response = self.bucket.meta.client.generate_presigned_post(
            self.bucket.name,
            f"{self.location}/{object_key}",
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=360,
        )
        return response


class StaticStorage(S3Boto3Storage):
    endpoint_url = "https://s3.ap-northeast-2.amazonaws.com"
    location = "_static"
    file_overwrite = True
    querystring_auth = False


class PublicMediaStorage(DefaultMediaStorage):
    endpoint_url = "https://s3.ap-northeast-2.amazonaws.com"
    location = "_media/public"
    file_overwrite = False
    querystring_auth = False


class PrivateMediaStorage(DefaultMediaStorage):
    endpoint_url = "https://s3.ap-northeast-2.amazonaws.com"
    location = "_media/private"
    file_overwrite = False
    querystring_auth = True


class DownloadableMediaStorage(PublicMediaStorage):
    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)

        file_name = name.rsplit("/", 1)[-1]
        encoded_filename = quote(file_name)

        content_type, _ = mimetypes.guess_type(name)
        if content_type is None:
            content_type = "application/octet-stream"

        params.update(
            {
                "ContentType": content_type,
                "ContentDisposition": (f'attachment; filename="{file_name}"; ' f"filename*=UTF-8''{encoded_filename}"),
            }
        )

        return params

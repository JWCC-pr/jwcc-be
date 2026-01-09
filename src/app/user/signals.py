from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app.user.models import User
from app.board_comment.models import BoardComment
from app.department_board_comment.models import DepartmentBoardComment
from app.liturgy_flower_comment.models import LiturgyFlowerComment
from app.passing_notice_comment.models import PassingNoticeComment


@receiver(pre_delete, sender=User)
def soft_delete_user_comments(sender, instance, **kwargs):
    BoardComment.objects.filter(user=instance).delete()
    DepartmentBoardComment.objects.filter(user=instance).delete()
    LiturgyFlowerComment.objects.filter(user=instance).delete()
    PassingNoticeComment.objects.filter(user=instance).delete()

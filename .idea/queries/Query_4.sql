 SELECT DISTINCT u.*
  FROM "user" u
  INNER JOIN user_sub_department_set us ON u.id = us.user_id
  INNER JOIN sub_department sd ON us.subdepartment_id = sd.id
  WHERE sd.department_id =;

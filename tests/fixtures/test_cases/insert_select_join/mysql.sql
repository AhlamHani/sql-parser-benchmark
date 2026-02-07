/*
tables = ['permissions', 'role_permissions', 'roles']
columns = []
engine = 'mysql'
*/

INSERT INTO role_permissions (role_id, permission_id)
SELECT
    r.id AS role_id,
    p.id AS permission_id
FROM roles r
  JOIN permissions p
WHERE r.name in('merchant-basic-operations')
  AND p.name = 'merchant_ops_dashboard';

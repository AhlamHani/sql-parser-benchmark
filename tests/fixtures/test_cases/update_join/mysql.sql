/*
tables = ['address', 'merchants']
columns = []
engine = 'mysql'
*/

UPDATE address a
JOIN merchants m ON a.entity_id = m.id
SET a.city_id = m.city_id, a.area_id = m.area_id
WHERE a.entity_id in (1084322, 1083736, 1083273);

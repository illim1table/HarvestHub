INSERT INTO users (username, email, hashed_password, role, is_active)
VALUES (
  'seed_buyer',
  'seed_buyer@harvesthub.local',
  '$2b$12$a.M.buscjxItFluLEXeUXe0aMbqDOKT0zzAEO.lV2rkszR/.FI3ea',
  'consumer',
  TRUE
)
ON DUPLICATE KEY UPDATE username = VALUES(username);

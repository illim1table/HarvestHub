INSERT INTO users (username, email, hashed_password, role, is_active)
VALUES (
  'seed_seller',
  'seed_seller@harvesthub.local',
  '$2b$12$JFUUz7D.TZyBrcT6j7h3rOK0YW0hJE2AoBJK4fG4uBU4hQz22BC5S',
  'seller',
  TRUE
)
ON DUPLICATE KEY UPDATE username = VALUES(username);

SET @seller_id = (SELECT id FROM users WHERE email = 'seed_seller@harvesthub.local' LIMIT 1);

INSERT INTO categories (name, description, is_active)
VALUES
  ('水果', '应季与特色水果', TRUE),
  ('蔬菜', '新鲜蔬菜直供', TRUE),
  ('粮油', '米面粮油及副食', TRUE)
ON DUPLICATE KEY UPDATE
  description = VALUES(description),
  is_active = VALUES(is_active);

INSERT INTO products (name, description, price, unit, stock, image_url, seller_id, category_id)
SELECT '有机红富士苹果', '产自山东烟台，有机种植，口感脆甜', 12.80, '斤', 500, 'https://placehold.co/300x200?text=苹果', u.id, c.id
FROM users u JOIN categories c ON c.name = '水果' WHERE u.email = 'seed_seller@harvesthub.local'
UNION ALL
SELECT '丹东草莓', '新鲜采摘，果香浓郁', 25.00, '500g/盒', 180, 'https://placehold.co/300x200?text=草莓', u.id, c.id
FROM users u JOIN categories c ON c.name = '水果' WHERE u.email = 'seed_seller@harvesthub.local'
UNION ALL
SELECT '新鲜大白菜', '当日现摘，叶片水嫩', 1.50, '斤', 1000, 'https://placehold.co/300x200?text=白菜', u.id, c.id
FROM users u JOIN categories c ON c.name = '蔬菜' WHERE u.email = 'seed_seller@harvesthub.local'
UNION ALL
SELECT '有机西红柿', '温室种植，酸甜适中', 4.80, '斤', 420, 'https://placehold.co/300x200?text=西红柿', u.id, c.id
FROM users u JOIN categories c ON c.name = '蔬菜' WHERE u.email = 'seed_seller@harvesthub.local'
UNION ALL
SELECT '东北五常大米', '稻花香2号，口感软糯', 45.00, '5kg/袋', 300, 'https://placehold.co/300x200?text=大米', u.id, c.id
FROM users u JOIN categories c ON c.name = '粮油' WHERE u.email = 'seed_seller@harvesthub.local';

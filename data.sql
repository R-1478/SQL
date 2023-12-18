-- Sample data for Customer table
INSERT INTO Customer (first_name, last_name) VALUES
('Alice', 'Smith'),
('Bob', 'Johnson'),
('Charlie', 'Brown');

-- Sample data for Restaurant table
INSERT INTO Restaurant (id, name) VALUES
(1, 'Tasty Bites'),
(2, 'Sizzling Grill'),
(3, 'Spicy Delight');

-- Sample data for Review table
-- Note: customer_id and restaurant_id are references to the Customer and Restaurant tables
INSERT INTO Review (customer_id, restaurant_id, rating) VALUES
(1, 1, 4),
(2, 1, 5),
(1, 2, 3),
(3, 2, 4),
(2, 3, 2),
(3, 3, 5);

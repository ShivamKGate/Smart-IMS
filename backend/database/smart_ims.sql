DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS warehouses CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    location VARCHAR NOT NULL
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    contact VARCHAR
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    category_id INTEGER NOT NULL,
    price FLOAT NOT NULL,
    reorder_level INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- composite primary key
CREATE TABLE inventory (
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

INSERT INTO categories (name) VALUES
('Electronics'),
('Clothing'),
('Home & Garden'),
('Sports & Outdoors'),
('Books');

INSERT INTO warehouses (location) VALUES
('Main Warehouse - Downtown'),
('North Branch'),
('South Distribution Center');

INSERT INTO suppliers (name, contact) VALUES
('TechSupply Co', 'tech@supply.com'),
('Fashion Distributors', 'orders@fashion.com'),
('HomeGoods Inc', 'wholesale@homegoods.com'),
('SportWorld', 'sales@sportworld.com'),
('BookSource', 'orders@booksource.com');

INSERT INTO products (name, category_id, price, reorder_level) VALUES
-- Electronics (category_id = 1)
('Laptop', 1, 999.99, 10),
('Smartphone', 1, 699.99, 15),
('Tablet', 1, 399.99, 12),
('Headphones', 1, 149.99, 25),

-- Clothing (category_id = 2)
('T-Shirt', 2, 19.99, 50),
('Jeans', 2, 79.99, 30),
('Sneakers', 2, 129.99, 20),

-- Home & Garden (category_id = 3)
('Coffee Maker', 3, 89.99, 15),
('Garden Hose', 3, 24.99, 20),
('Dining Chair', 3, 159.99, 8),

-- Sports & Outdoors (category_id = 4)
('Basketball', 4, 29.99, 30),
('Tent', 4, 249.99, 5),
('Hiking Boots', 4, 179.99, 12),

-- Books (category_id = 5)
('Programming Guide', 5, 49.99, 25),
('Fiction Novel', 5, 14.99, 40);

-- Insert Inventory data (some items set to low stock for testing)
INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES
-- Main Warehouse (warehouse_id = 1)
(1, 1, 15),  -- Laptop - OK
(2, 1, 8),   -- Smartphone - LOW
(3, 1, 20),  -- Tablet - OK
(4, 1, 35),  -- Headphones - OK
(5, 1, 45),  -- T-Shirt - LOW
(6, 1, 25),  -- Jeans - LOW
(7, 1, 22),  -- Sneakers - OK
(8, 1, 18),  -- Coffee Maker - OK

-- North Branch (warehouse_id = 2)
(1, 2, 5),   -- Laptop - LOW
(2, 2, 12),  -- Smartphone - LOW
(9, 2, 25),  -- Garden Hose - OK
(10, 2, 6),  -- Dining Chair - LOW
(11, 2, 28), -- Basketball - LOW
(12, 2, 3),  -- Tent - LOW

-- South Distribution Center (warehouse_id = 3)
(3, 3, 8),   -- Tablet - LOW
(4, 3, 40),  -- Headphones - OK
(13, 3, 10), -- Hiking Boots - LOW
(14, 3, 30), -- Programming Guide - OK
(15, 3, 35); -- Fiction Novel - LOW

-- Display summary of created data
SELECT 'Database schema and sample data created successfully!' as status;

SELECT 
    'Summary:' as info,
    (SELECT COUNT(*) FROM categories) as categories_count,
    (SELECT COUNT(*) FROM warehouses) as warehouses_count,
    (SELECT COUNT(*) FROM suppliers) as suppliers_count,
    (SELECT COUNT(*) FROM products) as products_count,
    (SELECT COUNT(*) FROM inventory) as inventory_entries_count;

-- Show low stock items (quantity below reorder level)
SELECT 
    'Low Stock Items:' as alert,
    p.name as product_name,
    w.location as warehouse_location,
    i.quantity as current_stock,
    p.reorder_level as reorder_level
FROM inventory i
JOIN products p ON i.product_id = p.id
JOIN warehouses w ON i.warehouse_id = w.id
WHERE i.quantity < p.reorder_level
ORDER BY p.name, w.location;
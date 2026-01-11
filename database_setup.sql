-- ============================================================================
-- Food Ordering Chatbot - Manual Database Setup for WAMP Server
-- ============================================================================
-- Run this SQL script in phpMyAdmin to create all tables manually
-- ============================================================================

-- Use the database
USE food_ordering_db;

-- ============================================================================
-- Table 1: orders
-- ============================================================================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_status ENUM('Placed', 'Preparing', 'Out for Delivery', 'Delivered', 'Cancelled') NOT NULL DEFAULT 'Placed',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount FLOAT NOT NULL DEFAULT 0.0,
    INDEX idx_order_status (order_status),
    INDEX idx_order_date (order_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Table 2: order_items
-- ============================================================================
CREATE TABLE order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Table 3: menu_items
-- ============================================================================
CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    category VARCHAR(50),
    is_available TINYINT(1) NOT NULL DEFAULT 1,
    INDEX idx_item_name (item_name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Insert Sample Menu Items
-- ============================================================================

-- Pizzas
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('Margherita Pizza', 8.99, 'Pizza', 1),
('Pepperoni Pizza', 10.99, 'Pizza', 1),
('Veggie Pizza', 9.99, 'Pizza', 1),
('BBQ Chicken Pizza', 11.99, 'Pizza', 1);

-- Burgers
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('Classic Burger', 7.99, 'Burger', 1),
('Cheese Burger', 8.99, 'Burger', 1),
('Veggie Burger', 7.49, 'Burger', 1),
('Bacon Burger', 9.99, 'Burger', 1);

-- Pasta
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('Spaghetti Carbonara', 12.99, 'Pasta', 1),
('Penne Arrabbiata', 11.99, 'Pasta', 1),
('Fettuccine Alfredo', 13.99, 'Pasta', 1);

-- Sides
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('French Fries', 3.99, 'Sides', 1),
('Garlic Bread', 4.99, 'Sides', 1),
('Onion Rings', 4.49, 'Sides', 1),
('Caesar Salad', 5.99, 'Sides', 1);

-- Drinks
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('Coca Cola', 1.99, 'Drinks', 1),
('Pepsi', 1.99, 'Drinks', 1),
('Orange Juice', 2.99, 'Drinks', 1),
('Water', 0.99, 'Drinks', 1);

-- Desserts
INSERT INTO menu_items (item_name, price, category, is_available) VALUES
('Chocolate Cake', 5.99, 'Desserts', 1),
('Ice Cream', 3.99, 'Desserts', 1),
('Cheesecake', 6.99, 'Desserts', 1);

-- ============================================================================
-- Verify Installation
-- ============================================================================

-- Check tables created
SHOW TABLES;

-- Check menu items
SELECT * FROM menu_items;

-- ============================================================================
-- Optional: Create a dedicated database user (Recommended for security)
-- ============================================================================

-- CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT ALL PRIVILEGES ON food_ordering_db.* TO 'chatbot_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ============================================================================
-- Database Schema Complete!
-- ============================================================================

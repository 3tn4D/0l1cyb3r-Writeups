<?php

$pdo = new PDO("sqlite:/tmp/db.sqlite");
$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
$pdo->exec(<<<EOT
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    money INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL
);

INSERT INTO products (id, name, price) VALUES 
    (1, 'not the flag', 3), 
    (2, 'yet again not the flag', 2), 
    (3, 'no flag for you :(', 5), 
    (4, 'random item (not the flag)', 8), 
    (99, 'flag', 100) 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (user) REFERENCES users(username),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
EOT);

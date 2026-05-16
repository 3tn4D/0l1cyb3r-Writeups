<?php
session_start(['use_strict_mode' => 1]);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /');
    die;
}

if (!isset($_SESSION['username'])) {
    header('Location: /');
    die;
}

if (!isset($_POST['product_id'])) {
    die('Missing product_id');
}

$username = $_SESSION['username'];
$product_id = trim($_POST['product_id']);

require_once __DIR__ . '/database.php';

$user = $pdo->query("SELECT * FROM users WHERE username='$username'")->fetch();
$product = $pdo->query("SELECT * FROM products WHERE id='$product_id'")->fetch();

if (!$product) {
    die('Invalid product_id');
}
if ($product['price'] > $user['money']) {
    die('Not enough money');
}
if (!in_array(intval($product_id), [1, 2, 3, 4])) {
    die("I don't know how you got here, but you can't buy the flag");
}

$pdo->query("INSERT INTO inventory (user, product_id) VALUES ('$username', $product_id);");

$pdo->query("UPDATE users SET money = money - " . $product['price'] . " WHERE username='$username';");

header('Location: /');

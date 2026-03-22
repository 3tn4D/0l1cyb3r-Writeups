<?php
session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

//If user is logged return to home page
if (!isLogged()) {
    header('Location: login.php');
    exit();
}
if (!isPost() || !isset($_POST['item_id'])) {
    header('Location: index.php');
    exit();
}

$item_id = $_POST['item_id'];
$obj = Item::filter_by([
    'item_id' => $item_id
]);

if (count($obj) == 0) {
    header('Location: index.php');
    exit();
}

$obj = $obj[0];

// Get current cart
$cart = get_cart();
if ($cart === null) {
    header('Location: index.php');
    exit();
}

if (isset($cart[$obj['item_id']])) {
    $cart[$obj['item_id']]['qty'] += 1;
} else {
    $cart[$obj['item_id']] = [
        'qty' => 1,
    ];
}

store_cart($cart);

header("Location: cart.php");
exit();

<?php
require_once __DIR__ . '/../lib/Utils.php';
exitIfRequested(__FILE__);
?>
<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="template/style.css">
    <title>Meme shop</title>
</head>

<body>
    <header class="page-header">
        <div id="logo">
            <a href=".">
                MEME SHOP
            </a>
        </div>
        <nav id="navbar">
            <ul>
                <?php if (isLogged()) {
                    $user = User::filter_by([
                        'user_id' => $_SESSION['user_id']
                    ])[0];
                ?>
                    <li class="nav-item">Bilancio:<?php echo ($user['balance']); ?> € - </li>
                    <li class="nav-item"><a href="index.php">Shop</a></li>
                    <li class="nav-item"><a href="cart.php">Carrello</a></li>
                    <li class="nav-item"><a href="buy_list.php">Lista acquisti</a></li>
                <?php } else { ?>
                    <li class="nav-item"><a href="login.php">Login</a></li>
                    <li class="nav-item"><a href="register.php">Register</a></li>
                <?php } ?>
            </ul>
        </nav>
    </header>

    <main class="page-content">
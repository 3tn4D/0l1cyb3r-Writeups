<?php
session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

//If user is logged return to home page
if (!isLogged()) {
    header('Location: login.php');
    exit();
}
?>

<?php require_once __DIR__ . '/template/header.php'; ?>

<div class="d-flex">
    <?php
    $ans = get_cart();
    $total = 0;
    foreach ($ans as $k => $v) {
        $total += $v['price'] * $v['qty'];
    ?>
        <div class="meme-row m-auto">
            <div class="meme-text">
                <p><?php echo $k; ?></p>
                <p><?php echo "x" . $v['qty']; ?></p>
                <p><?php echo $v['price'] * $v['qty'] . " €"; ?></p>
            </div>
        </div>
    <?php
    }
    ?>
    <div class="meme-row m-auto">
        <div class="meme-text">
            <p>TOTALE</p>
            <p><?php echo $total . " €"; ?></p>
            <form method="POST" action="/checkout.php">
                <button type="submit" class="meme-button background-red p-10">
                    Checkout
                </button>
            </form>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
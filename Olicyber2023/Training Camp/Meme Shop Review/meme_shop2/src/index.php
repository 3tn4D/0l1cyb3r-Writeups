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
    $ans = Item::filter_by();
    foreach ($ans as $x) {
    ?>
        <div class="meme-row m-auto">
            <div class="meme-text">
                <p><?php echo $x['name']; ?></p>
                <p><?php echo $x['price']; ?></p>
                <form action="/add_to_cart.php" method="POST">
                    <input type="hidden" name="item_id" value="<?php echo $x['item_id']; ?>">
                    <button type="submit" class="meme-button background-red p-10">
                        Aggiungi al carrello
                    </button>
                </form>
            </div>

        </div>
    <?php
    }
    ?>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
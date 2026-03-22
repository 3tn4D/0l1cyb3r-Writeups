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
    $ans = Purchase::filter_by([
        'user_id' => $_SESSION['user_id']
    ]);

    foreach ($ans as $x) {
        $item = Item::filter_by([
            'item_id' => $x['item_id']
        ]);
        if (count($item) == 0) {
            continue;
        }
        $item = $item[0];
    ?>
        <div class="meme-row m-auto">
            <div class="meme-text">
                <p><?php echo $item['name']; ?></p>

                <?php if (substr($item['content'], 0, 1) === '/') {
                ?>
                    <a href="<?php echo $item['content']; ?>">Esterno</a>
                <?php
                } else {
                ?>
                    <p><?php echo $item['content']; ?></p>
                <?php } ?>
            </div>
        </div>
    <?php
    }
    ?>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
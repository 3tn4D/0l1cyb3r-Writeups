<?php
session_start(['use_strict_mode' => 1]);

require_once __DIR__ . '/database.php';

if (!isset($_SESSION['username'])) {
    // initialize user
    // usually we would have a registration + login process, but it's not relevant for the challenge, so we simplify this
    $_SESSION['username'] = session_id();

    $stmt = $pdo->prepare('INSERT INTO users (username) VALUES (?)');
    $stmt->execute([$_SESSION['username']]);
}

$username = $_SESSION['username'];

$stmt = $pdo->prepare('SELECT * FROM users WHERE username=?');
$stmt->execute([$_SESSION['username']]);
$user = $stmt->fetch();

$stmt = $pdo->prepare('SELECT products.* FROM inventory INNER JOIN products ON product_id=products.id WHERE user=?');
$stmt->execute([$_SESSION['username']]);
$inventory = $stmt->fetchAll();

$stmt = $pdo->prepare('SELECT * FROM products');
$stmt->execute();
$products = $stmt->fetchAll();

include_once __DIR__ . '/header.php';
?>

<main class="py-24 mx-auto w-full max-w-6xl">
    <h1 class="text-4xl font-bold">Simple shop</h1>
    <h3 class="text-2xl font-semibold mt-2 text-neutral-700">Your balance: <span class="font-mono"><?= $user['money']; ?></span></h3>

    <div class="grid grid-cols-4 gap-4 mt-8">
        <?php
        foreach ($products as $product) {
        ?>
            <div class="border border-neutral-300 rounded-md shadow-sm px-4 py-3 flex flex-col">
                <div class="text-xl font-bold">
                    <?= $product['name']; ?>
                </div>
                <div class="mt-3 flex-grow">
                    Price: <span class="font-mono"><?= $product['price']; ?></span>
                </div>
                <form class="mt-5 text-center" method="post" action="/buy.php">
                    <input type="hidden" value="<?= $product['id']; ?>" name="product_id">
                    <button class="rounded-full bg-pink-300 px-10 py-0.5 cursor-pointer hover:bg-pink-400">
                        Buy now!
                    </button>
                </form>
            </div>
        <?php
        }
        ?>
    </div>

    <h2 class="text-3xl font-bold mt-20">My inventory</h2>
    <div class="flex flex-col mt-4">
        <?php
        if (count($inventory) === 0) {
        ?>
            <div class="italic mt-4">
                Buy at least one item to see it in your inventory
            </div>
        <?php
        }

        foreach ($inventory as $product) {
        ?>
            <div class="border-b border-neutral-300 p-4">
                <div class="text-xl font-bold">
                    <?= $product['name']; ?>
                </div>
                <?php
                if ($product['name'] === 'flag') { ?>
                    <div>
                        <?= $_ENV['FLAG']; ?>
                    </div>
                <?php } ?>
            </div>
        <?php
        }
        ?>
    </div>
</main>
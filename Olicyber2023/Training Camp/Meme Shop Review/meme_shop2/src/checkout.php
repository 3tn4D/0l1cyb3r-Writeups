<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

//If user is logged return to home page
if (!isLogged()) {
    header('Location: login.php');
    exit();
}

$user = User::toObject(User::filter_by([
    'user_id' => $_SESSION['user_id']
])[0]);

$ans = get_cart();
$actual_cart = [];
$total = 0;
foreach ($ans as $k => $v) {
    $ans = Item::filter_by([
        'item_id' => $k
    ]);
    if (count($ans) == 0) {
        continue;
    }
    if (!is_numeric($v['qty']) || $v['qty'] < 1) {
        continue;
    }

    $ans = $ans[0];
    $total += $ans['price'] * $v['qty'];
    $actual_cart[$ans['item_id']] = [
        'price' => $ans['price'],
    ];
}

if ($total == 0) {
    header("Location: index.php");
    exit();
}

if ($total > $user->balance) {
    require_once __DIR__ . '/template/header.php';
?>
    <h1 style="color: red;">Credito insufficiente!</h1>
<?php require_once __DIR__ . '/template/footer.php';
    setcookie('cart', '', time() - 3600);
} else {

    foreach ($actual_cart as $k => $v) {
        $p = new Purchase();
        $p->user_id = $user->user_id;
        $p->item_id = $k;

        $p->save();
    }

    $user->balance -= $total;
    $user->save();

    setcookie('cart', '', time() - 3600);
    header("Location: buy_list.php");
    exit();
}
?>
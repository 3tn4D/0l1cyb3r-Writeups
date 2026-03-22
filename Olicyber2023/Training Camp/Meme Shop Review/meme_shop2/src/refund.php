<?php
session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

function refundPost()
{
    if ($_SESSION['username'] !== "administrator") {
        echo "Illegale in tutti i paesi del mondo, non farlo mai più...";
        exit();
    }

    if (!isset($_POST['user_id']) || !isset($_POST['amount']) || !is_numeric($_POST['amount'])) {
        return [
            "error" => "Form non valido!"
        ];
    }

    $ans = User::filter_by([
        'user_id' => $_POST['user_id']
    ]);

    if (count($ans) == 0) {
        return [
            "error" => "Utente non esistente!"
        ];
    }

    $user = User::toObject($ans[0]);
    $user->balance += $_POST['amount'];
    $user->save();

    return [];
}

//If user is logged return to home page
if (!isLogged()) {
    header('Location: login.php');
    exit();
}

if (isPost()) {
    $ans = refundPost();
}
?>

<?php require_once __DIR__ . '/template/header.php'; ?>

<div class="d-flex">
    <div class="form-background p-20" style="width:300px; margin:auto">
        <header style="width:200px; margin: auto;">
            <h2 class="center">
                Rimborso
            </h2>
        </header>

        <form action="" method="POST">
            <input class="form-input" type="number" name="amount" placeholder="Importo">
            <select class="form-input" style="background-color: white;" name="user_id" id="username">
                <?php
                $ans = User::filter_by();
                foreach ($ans as $x) {
                    echo '<option value="' . $x['user_id'] . '">' . htmlspecialchars($x['username']) . '</option>';
                }
                ?>
            </select>
            <input class="form-input form-button background-red" type="submit" name="submit" value="Riscatta" <?php if ($_SESSION['username'] != "administrator") {
                                                                                                                    echo "disabled";
                                                                                                                } ?>>
            <div class="error-banner center">
                <?php if (isset($ans) && isset($ans['error'])) echo $ans['error']; ?>
            </div>

        </form>
    </div>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
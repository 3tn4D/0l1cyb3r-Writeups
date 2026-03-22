<?php
session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

function reportPost()
{
    if (!isset($_POST['url'])) {
        return [
            "error" => "Form non valido!"
        ];
    }

    $report_url = getenv('REPORT_URL');

    // curl to bot server
    $r = curl_init();

    curl_setopt($r, CURLOPT_URL, $report_url);
    curl_setopt($r, CURLOPT_POST, true);
    curl_setopt($r, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($r, CURLOPT_HEADER, false);
    curl_setopt($r, CURLOPT_POSTFIELDS, 'url=' . $_POST['url']);

    $result = curl_exec($r);
    curl_close($r);

    echo $result;

    return ["error" => "url reportata correttamente"];
}

//If user is logged return to home page
if (!isLogged()) {
    header('Location: login.php');
    exit();
}

if (isPost()) {
    $ans = reportPost();
}
?>

<?php require_once __DIR__ . '/template/header.php'; ?>

<div class="d-flex">
    <div class="form-background p-20" style="width:300px; margin:auto">
        <header style="width:200px; margin: auto;">
            <h2 class="center">
                Report
            </h2>
        </header>

        <form action="" method="POST">
            <input class="form-input" type="text" name="url" placeholder="http://...">
            <input class="form-input form-button background-red" type="submit" name="submit" value="Reporta">
            <div class="error-banner center">
                <?php if (isset($ans) && isset($ans['error'])) echo $ans['error']; ?>
            </div>

        </form>
    </div>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
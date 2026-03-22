<?php
session_start();
require_once __DIR__ . '/lib/Utils.php';
require_once __DIR__ . '/lib/Models.php';

//POST request handler
function signupPost()
{
    $ans = [
        'user_id' => null,
        'error' => null,
    ];

    //Check form data
    if (
        !isset($_POST['password']) || !is_string($_POST['password']) ||
        !isset($_POST['username']) || !is_string($_POST['username']) ||
        !isset($_POST['passwordConfirm']) || !is_string($_POST['passwordConfirm'])
    ) {
        $ans['error'] = 'Valori mancanti!';
        return $ans;
    }

    //Check for username length
    $username = trim($_POST['username']);
    if (strlen($username) < 8) {
        $ans['error'] = "L'username inserito non è valido!";
        return $ans;
    }

    $password = trim($_POST['password']);
    $passwordConfirm = trim($_POST['passwordConfirm']);

    //Check if user submited same password as confirm
    if ($password != $passwordConfirm) {
        $ans['error'] = 'Le due password non coincidono';
        return $ans;
    }

    //Create new user object and set data
    $newUser = new User();
    $newUser->username = $username;
    $newUser->setPassword($password);

    try {
        //Attempt to save new user
        $newUser->save();

        //Query for it to get the full data
        $users = User::filter_by([
            'username' => $newUser->username
        ]);

        $ans['user_id'] = $users[0]['user_id'];
        return $ans;
    } catch (DuplicateKeyException $e) {
        //If exception is raised username or email already exists
        $ans['error'] = 'Username o email già esistente!';
        return $ans;
    }
}

//If user is logged redirect to home page
if (isLogged()) {
    header('Location: index.php');
    exit();
}

$ans = null;

if (isPost()) {
    $ans = signupPost();
    if ($ans['error'] === null) {
        //If no error happened set session variables and redirect to home page
        $_SESSION['user_id'] = $ans['user_id'];
        header('Location: index.php');
        exit();
    }
}

?>

<?php require_once __DIR__ . '/template/header.php'; ?>

<div class="splitted-container">
    <div class="left-container form-background">
        <header>
            <h2 class="center">
                Registrati
            </h2>
        </header>
        <form id="form" action="" method="POST">
            <input class="form-input" type="text" name="username" placeholder="Username" required>
            <input class="form-input" type="password" name="password" placeholder="Password" required>
            <input class="form-input" type="password" name="passwordConfirm" placeholder="Conferma password" required>
            <div class="error-banner center">
                <?php if ($ans != null) echo $ans['error']; ?>
            </div>
            <input id="submitButton" class="form-input form-button background-red" type="submit" name="submit" value="Registrati">
        </form>
    </div>
    <div class="right-container centered-container">
        <h2 class="center">
            Bentornato!
        </h2>
        <p class="center">
            Fai già parte della nostra community?
        </p>
        <a href="login.php" class="form-input form-button background-red">
            Login
        </a>
    </div>
</div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
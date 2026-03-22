<?php
    session_start();
    require_once __DIR__ . '/lib/Utils.php';
    require_once __DIR__ . '/lib/Models.php';

    //POST request handler
    function signinPost(){
        $ans = [
            'user_id' => null,
            'error' => null
        ];

        //check submitted data
        if(!isset($_POST['username']) || !is_string($_POST['username']) ||
            !isset($_POST['password']) || !is_string($_POST['password'])){
            $ans['error'] = 'Valori mancanti';
            return $ans;
        }

        $username = trim($_POST['username']);
        $password = trim($_POST['password']);

        $user = User::login($username, $password);
        if($user === null){
            $ans['error'] = 'Nome utente o password sbagliati';
            return $ans;
        }

        $ans['user_id'] = $user->user_id;
        return $ans;
    }

    //If user is logged return to home page
    if(isLogged()){
        header('Location: index.php');
        exit();
    }

    $ans = null;

    if(isPost()){
        $ans = signinPost();
        //If login worked set session variables and redirect to home page
        if($ans['error'] === null){
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
                    Login
                </h2>
            </header>
            <form action="" method="POST">
                <input class="form-input" type="text" name="username" placeholder="Username">
                <input class="form-input" type="password" name="password" placeholder="Password">
                <div class="error-banner center">
                    <?php if($ans != null) echo $ans['error']; ?>
                </div>
                <input class="form-input form-button background-red" type="submit" name="submit" value="Login">
            </form>
        </div>
        <div class="right-container centered-container">
            <header>
                <h2 class="center">
                    Benvenuto!
                </h2>
            </header>
            <p class="center">
                Entra anche tu a far parte della nostra community?
            </p>

            <a href="register.php" class="form-input form-button background-red">
                Registrati
            </a>

        </div>
    </div>

<?php require_once __DIR__ . '/template/footer.php'; ?>
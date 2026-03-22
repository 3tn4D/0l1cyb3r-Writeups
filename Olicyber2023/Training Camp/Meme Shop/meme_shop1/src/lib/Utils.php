<?php

    /*
     * This file is used to store common methods and constant value across
     * all the application
     */

    //Exit if the page is requested directly instead of import
    function exitIfRequested($callingFile){
        if (strcasecmp(str_replace('\\', '/', $callingFile), $_SERVER['SCRIPT_FILENAME']) == 0) {
            http_response_code(404);
            exit();
        }
    }
    exitIfRequested(__FILE__);

    function throwDatabaseError(){
        http_response_code(500);
        exit('Database Error, please contact the administrator');
    }

    //Check if user is logged, REMEMBER TO START THE SESSION
    function isLogged(){
        return (isset($_SESSION['user_id']) && ($_SESSION['user_id'] !== null));
    }

    function checkPassword($password){
        if(strlen($password) < 8 || !preg_match("/[a-z]/", $password) ||
            !preg_match("/[A-Z]/", $password) || !preg_match("/\d/", $password) ||
            !preg_match("/\W|_/", $password)){
            return false;
        }
        return true;
    }

    function isPost(){
        return strcmp($_SERVER['REQUEST_METHOD'], 'POST') === 0;
    }

    function isGet(){
        return strcmp($_SERVER['REQUEST_METHOD'], 'GET') === 0;
    }


    //Use this function to print user provided content to avoid XSS
    function escapeString($string){
        return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
    }

    //returns a json and set a status code - default is 200
    function exitWithJson($obj, $code = 200){
        http_response_code($code);
        echo json_encode($obj);
        exit();
    }

    //Check if a string is an integer number
    function isNumber($str){
        return is_string($str) && preg_match("/^-?\d{1,}$/", $str);
    }

    function get_cart(){
        if(!isset($_COOKIE["cart"])){
            return [];
        }

        $cart = $_COOKIE["cart"];
        $cart = base64_decode($cart);
        if ($cart === false){
            return [];
        }

        $cart = json_decode($cart, true);
        if ($cart === null){
            return [];
        }

        return $cart;
    }

    function store_cart($cart){
        $cart = json_encode($cart);
        $cart = base64_encode($cart);

        setcookie("cart", $cart);
    }

?>
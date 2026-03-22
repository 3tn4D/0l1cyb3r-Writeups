<?php

require_once __DIR__ . '/ORM.php';

class User extends Entity
{
    public $user_id;
    public $username;
    public $balance;
    public $hash;

    public function __construct()
    {
        $this->balance = new DefaultValue();
    }

    public function setPassword($password)
    {
        $this->hash = password_hash($password, PASSWORD_DEFAULT);
    }

    //Checks for user existance and password match
    public static function login($username, $password)
    {
        $ans = static::filter_by([
            'username' => $username
        ]);

        if (count($ans) == 0)
            return null;

        $record = $ans[0];

        if (password_verify($password, $record['hash'])) {
            return static::toObject($record);
        }

        return null;
    }
}

class Item extends Entity
{
    public $item_id;
    public $name;
    public $content;
    public $price;

    public function __construct()
    {
        $this->price = new DefaultValue();
    }
}

class Purchase extends Entity
{
    public $purchase_id;
    public $user_id;
    public $item_id;

    public function __construct()
    {
    }
}

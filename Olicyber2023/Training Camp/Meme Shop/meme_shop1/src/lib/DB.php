<?php

    require_once __DIR__ . '/Utils.php';

    /* Avoid direct page request */
    exitIfRequested(__FILE__);

    /* DB Singleton */
    /* Singleton has been used to get a common shared DB connection */
    class DB{

        private static $instance = null;
        private $connection = null;

        private $hostname = 'meme_shop_mysql';
        private $dbname = 'meme_shop';
        private $username = 'root';
        private $password = 'password';

        /*
         * Get db shared instance
         */
        public static function getInstance(){
            //If no PDO instance has been created
            if(static::$instance === null){
                //Create it
                static::$instance = new DB();
            }

            //Return shared DB connection
            return static::$instance;
        }

        private function __construct(){
            try{
                //Make DB connection
                $this->connection = new PDO("mysql:host={$this->hostname};dbname={$this->dbname}", $this->username, $this->password);
                //Set error mode to exception
                $this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                $this->connection->setAttribute(PDO::ATTR_EMULATE_PREPARES, false );
            }
            catch(PDOException $e){
                //If db connection error occurs return 500 status code (Server error)
                var_dump($e);
                exitWithJson(['error' => 'Error connecting with the database'], 500);
            }
        }

        public function __destruct(){
            //Close db connection on destruction
            $this->connection = null;
            static::$instance = null;
        }

        /*
         * Executes single query statement:
         * with or without parameters
         * with or without result set
         */
        public function exec($query, $values = []){
            //Make prepared statement
            $prepared = $this->connection->prepare($query);
            //Execute prepared query with or without parameters
            $prepared->execute($values);

            try{
                //Attempt to fetch result set as associative aray
                $result = $prepared->fetchAll(PDO::FETCH_ASSOC);
            }
            catch(PDOException $e){
                //If no result set is found return true if rows have been affected
                return ($prepared->rowCount() > 0);
            }

            //If there is a result set return it
            return $result;
        }

        /* Avoid object clonation */
        private function __clone(){
        }
    }
?>
CREATE DATABASE meme_shop;
USE meme_shop;

-- -------
-- User --
-- -------
CREATE TABLE `user`(
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `balance` INT DEFAULT 10,
    `hash` VARCHAR(255) NOT NULL,

    PRIMARY KEY (`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------
-- Items --
-- --------
CREATE TABLE `item`(
    `item_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `content` VARCHAR(100) NOT NULL,
    `price` INT DEFAULT 10,

    PRIMARY KEY (`item_id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- -----------
-- purchase --
-- -----------
CREATE TABLE `purchase`(
    `purchase_id` INT NOT NULL AUTO_INCREMENT,

    `user_id` INT NOT NULL,
    `item_id` INT NOT NULL,

    PRIMARY KEY (`purchase_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`item_id`) REFERENCES `item`(`item_id`) ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `item` VALUES
    (DEFAULT, 'flag', 'flag{REDATTO}', 100),
    (DEFAULT, 'Videogame', '/memes/videogame.jpg', 1),
    (DEFAULT, 'AI', '/memes/ai.jpg', 1),
    (DEFAULT, 'Malevisione', '/memes/malevisione.jpg', 1),
    (DEFAULT, 'Seal of approval', '/memes/seal_of_approval.jpg', 1),
    (DEFAULT, 'Gaspare', '/memes/gaspare.jpg', 1);


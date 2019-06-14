SHOW WARNINGS;

/*
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
*/

DROP DATABASE IF EXISTS openfacts;

CREATE DATABASE openfacts CHARACTER SET 'utf8';
CREATE DATABASE IF NOT EXISTS openfacts CHARACTER SET 'utf8';

DROP DATABASE IF EXISTS openfacts;
DROP DATABASE IF EXISTS openfacts;

CREATE DATABASE openfacts CHARACTER SET 'utf8';

USE openfacts;

CREATE TABLE IF NOT EXISTS category (
    id VARCHAR(127) NOT NULL,
    PRIMARY KEY (id)
)
ENGINE = INNODB;

SHOW TABLES;
DESCRIBE category;

DROP TABLE IF EXISTS category;

SHOW TABLES;

CREATE TABLE IF NOT EXISTS category (
    id VARCHAR(127) NOT NULL,
    label VARCHAR(255),
    n_product MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
    url_str VARCHAR(255),
    same_as VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS product (
    code MEDIUMINT UNSIGNED NOT NULL,
    label VARCHAR(255),
    brand VARCHAR(255),
    nova_group TINYINT UNSIGNED,
    nutrition_grades CHAR(1),
    image_url VARCHAR(255),
/*
    "categories_hierarchy": [
                "en:biscuits-and-cakes",
                "en:cakes",
                "fr:financiers",
                "fr:P\u00e2tisseries fondantes \u00e0 la poudre d'amande"
            ],
            "created_t": 1480541444,
            "last_modified_t": 1558712294,
            "name": "P\u00e2tisseries fondantes \u00e0 la poudre d'amande.",
            "nutrient_levels": {
                "fat": "high",
                "salt": "moderate",
                "saturated-fat": "high",
                "sugars": "high"
            },
            "nutrition_score": -1,
            "nutrition_score_beverage": 0,
            "stores": "Bordeaux,Brive,Limoges,Saint-Yrieix",
            "unique_scans_n": -1,
*/
    PRIMARY KEY (code)
);
ALTER TABLE product ADD COLUMN product_url VARCHAR(255);
ALTER TABLE product ADD COLUMN product_test VARCHAR(255);


CREATE TABLE IF NOT EXISTS relation_category_product (
    category_id VARCHAR(127) NOT NULL,
    product_code MEDIUMINT UNSIGNED NOT NULL,
    PRIMARY KEY (category_id)
);

SHOW TABLES;
DESCRIBE category;
DESCRIBE product;
DESCRIBE relation_category_product;


ALTER TABLE product
DROP COLUMN product_test;
DESCRIBE product;

INSERT INTO product VALUES (123456, 'tot', 'tutut', 2, 'a', NULL, NULL);
INSERT INTO product (code, label, brand)
VALUES (1023456, 't', 'tuuti'),
        (103456, 'to', 'tuti'),
        (102456, 'tto', 'ututi'),
        (10456, 'totzo', 'ti'),
        (23456, 'todo', 'ttuti');
SELECT * FROM product;

SELECT * FROM product ORDER BY code, label DESC LIMIT 3 OFFSET 2;

SELECT code, label, brand FROM product;
SELECT * FROM product WHERE code < 103000 AND label!='totzo' ORDER BY label;



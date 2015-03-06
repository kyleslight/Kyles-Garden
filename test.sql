-- create database test CHARACTER SET utf8;
use test;

-- CREATE TABLE book(
-- id INT(11) AUTO_INCREMENT PRIMARY KEY,
-- title VARCHAR(255) NOT NULL,
-- order_id INT(11)
-- );

-- CREATE TABLE collect(
-- id INT(11) AUTO_INCREMENT PRIMARY KEY,
-- title VARCHAR(255) NOT NULL,
-- book_id INT(11),
-- order_id INT(11)
-- );

-- CREATE TABLE article_6 (
-- id INT(11) AUTO_INCREMENT PRIMARY KEY,
-- title VARCHAR(255),
-- description longtext,
-- content longtext,
-- ori_text longtext,
-- collect_id INT(11),
-- order_id INT(11),
-- insert_time DATE
-- );

-- CREATE TABLE user(
-- id INT(11) AUTO_INCREMENT PRIMARY KEY,
-- username VARCHAR(255) NOT NULL,
-- password VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE share(
-- 	id INT(11) AUTO_INCREMENT PRIMARY KEY,
-- 	title VARCHAR(255) NOT NULL,
-- 	content longtext,
-- 	share_id VARCHAR(255) NOT NULL
-- );

-- TRUNCATE TABLE book;
-- TRUNCATE TABLE collect;
-- TRUNCATE TABLE article_6;
TRUNCATE TABLE share;

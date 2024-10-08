CREATE DATABASE blog;
USE blog;
CREATE TABLE authors(
	author_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    user_name VARCHAR(20),
    user_password VARCHAR(80)
);
CREATE TABLE blog_posts(
	post_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    author_id INT,
    post_title VARCHAR(120),
    post_body VARCHAR(500),
    post_tag VARCHAR(30)
);
DELETE FROM blog_posts WHERE post_id = 2;
SELECT * FROM blog_posts;
SELECT * FROM authors;

DB_NAME=taskdb
DB_USER=root
DB_PASSWORD=toortoor
DB_HOST=localhost
DB_PORT=3306

.PHONY: all setup clean

all: install-mariadb setup

install-mariadb:
	sudo apt update
	sudo apt install -y mariadb-server mariadb-client
	sudo systemctl enable mariadb
	sudo systemctl start mariadb
	sudo mysql_secure_installation

setup: create-db create-table insert-data

create-db:
	mysql -u$(DB_USER) -p$(DB_PASSWORD) -h$(DB_HOST) -P$(DB_PORT) -e "CREATE DATABASE IF NOT EXISTS $(DB_NAME);"

create-table:
	mysql -u$(DB_USER) -p$(DB_PASSWORD) -h$(DB_HOST) -P$(DB_PORT) $(DB_NAME) -e "\
	CREATE TABLE IF NOT EXISTS tasks ( \
		id INT AUTO_INCREMENT PRIMARY KEY, \
		image VARCHAR(255), \
		company VARCHAR(255), \
		title VARCHAR(255), \
		description TEXT, \
		badgeType ENUM('Normal', 'Gold', 'Silver', 'Bronze') \
	);"

insert-data:
	mysql -u$(DB_USER) -p$(DB_PASSWORD) -h$(DB_HOST) -P$(DB_PORT) $(DB_NAME) -e "\
	INSERT INTO tasks (image, company, title, description, badgeType) VALUES \
	('https://via.placeholder.com/150', 'Company A', 'Task A', 'Task A Description', 'Normal'), \
	('https://via.placeholder.com/150', 'Company B', 'Task B', 'Task B Description', 'Gold'), \
	('https://via.placeholder.com/150', 'Company C', 'Task C', 'Task C Description', 'Silver'), \
	('https://via.placeholder.com/150', 'Company D', 'Task D', 'Task D Description', 'Bronze'), \
	('https://via.placeholder.com/150', 'Company E', 'Task E', 'Task E Description', 'Gold'), \
	('https://via.placeholder.com/150', 'Company F', 'Task F', 'Task F Description', 'Silver'), \
	('https://via.placeholder.com/150', 'Company G', 'Task G', 'Task G Description', 'Normal'), \
	('https://via.placeholder.com/150', 'Company H', 'Task H', 'Task H Description', 'Bronze'), \
	('https://via.placeholder.com/150', 'Company I', 'Task I', 'Task I Description', 'Gold'), \
	('https://via.placeholder.com/150', 'Company J', 'Task J', 'Task J Description', 'Silver');"

# 실행 방법 : make all

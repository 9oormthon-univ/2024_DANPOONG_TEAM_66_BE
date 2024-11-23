.PHONY: all setup_db start_mysql init_app run_app clean

DB_NAME=mydatabase
DB_USER=user
DB_PASS=user
ROOT_PASS=root

all: setup_db init_app run_app

# Update and install MariaDB server
setup_db:
	sudo apt update
	sudo apt install mariadb-server -y
	sudo service mysql start
	echo $(ROOT_PASS) | sudo mysql_secure_installation

	# MariaDB setup
	echo "CREATE DATABASE $(DB_NAME);" | mariadb -uroot -p$(ROOT_PASS)
	echo "CREATE USER '$(DB_USER)'@'localhost' IDENTIFIED BY '$(DB_PASS)';" | mariadb -uroot -p$(ROOT_PASS)
	echo "GRANT ALL PRIVILEGES ON $(DB_NAME).* TO '$(DB_USER)'@'localhost';" | mariadb -uroot -p$(ROOT_PASS)
	echo "FLUSH PRIVILEGES;" | mariadb -uroot -p$(ROOT_PASS)

start_mysql:
	sudo service mysql start

# Install Python dependencies and initialize database
init_app:
	pip install -r requirements.txt
	python init_db.py

# Run the application
run_app:
	uvicorn main:app --host 0.0.0.0 --port 8000

# Clean up MariaDB server (optional)
clean:
	sudo service mysql stop
	sudo apt remove mariadb-server -y
	sudo apt autoremove -y
	rm -rf /var/lib/mysql

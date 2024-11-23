#!/bin/bash
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld_safe --datadir=/var/lib/mysql &

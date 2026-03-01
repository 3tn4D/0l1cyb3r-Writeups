FROM php:8.1-apache
RUN apt update -y
RUN apt install libsqlite3-dev sqlite3 -y
RUN docker-php-ext-install pdo pdo_sqlite

CMD /var/www/html/init.sh
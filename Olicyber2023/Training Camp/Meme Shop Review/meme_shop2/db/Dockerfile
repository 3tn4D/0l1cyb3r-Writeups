FROM mysql:8

ENV MYSQL_ROOT_PASSWORD=password

ADD ./generate.sql /docker-entrypoint-initdb.d/

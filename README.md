### robot


#### db

    create database yunmall_db CHARACTER SET utf8;
    create user yunmall;
    grant all privileges on yunmall_db.* to 'yunmall'@'%' identified by '!qazxsw@#edc' with grant option;
    grant all privileges on yunmall_db.* to 'yunmall'@'localhost' identified by '!qazxsw@#edc' with grant option;
    flush privileges;

#### code

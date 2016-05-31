drop database if exists eagle;
create database eagle charset=utf8;

use eagle
create table `user` (
    `id` int(11) not null auto_increment,
    `username` varchar(128) not null default '' comment 'username',
    `password` varchar(128) not null default '' comment 'password',
    `email` varchar(128) not null default '' comment 'email',
    `salt` varchar(128) not null default '' comment 'salt',
    `create_time` datetime not null default '0000-00-00 00:00' comment 'create_time',
    `update_time` datetime not null default '0000-00-00 00:00' comment 'update_time',
    `is_deleted` tinyint(3) not null default '0',
    primary key (`id`),
    key `idx_email` (`email`)
)engine=InnoDB DEFAULT CHARSET=utf8;

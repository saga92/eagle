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
    `is_deleted` tinyint(3) not null default '0' comment '1:deleted',
    primary key (`id`),
    key `idx_email` (`email`),
    key `idx_is_deleted` (`is_deleted`)
)engine=InnoDB DEFAULT CHARSET=utf8 comment 'user';

create table `image` (
    `id` int(11) not null auto_increment,
    `image_name` varchar(128) not null default '' comment 'image name',
    `description` varchar(512) not null default '' comment 'image description',
    `create_time` datetime not null default '0000-00-00 00:00' comment 'create_time',
    `update_time` datetime not null default '0000-00-00 00:00' comment 'update_time',
    `is_deleted` tinyint(3) not null default '0' comment '1:deleted',
    primary key (`id`),
    key `idx_hash` (`image_name`),
    key `idx_is_deleted` (`is_deleted`)
)engine=InnoDB DEFAULT CHARSET=utf8 comment 'image';

insert into `image` values (1, 'eagle-ubuntu:14.04', '', now(), now(), 0);
insert into `image` values (2, 'eagle-centos:7', '', now(), now(), 0);
insert into `image` values (3, 'eagle-fedora:23', '', now(), now(), 0);
insert into `image` values (4, 'eagle-debian:8', '', now(), now(), 0);

create table `instance` (
    `id` int(11) not null auto_increment,
    `image_id` int(11) not null default '0' comment 'image id fk of image',
    `user_id` int(11) not null default '0' comment 'user id fk of user',
    `container_name` varchar(128) not null default '' comment 'container name',
    `container_serial` varchar(128) not null default '' comment 'container serial',
    `host` varchar(128) not null default '' comment 'container host ip',
    `port` int(11) not null default '0' comment 'container host port',
    `status` tinyint(3) not null default '0' comment '1:running 2:stop 3:failed 4:pending 5:unknown',
    `create_time` datetime not null default '0000-00-00 00:00' comment 'create_time',
    `update_time` datetime not null default '0000-00-00 00:00' comment 'update_time',
    `is_deleted` tinyint(3) not null default '0' comment '1:deleted',
    primary key (`id`),
    key `idx_container_name` (`container_name`),
    key `idx_container_serial` (`container_serial`),
    key `idx_is_deleted` (`is_deleted`)
)engine=InnoDB DEFAULT CHARSET=utf8 comment 'instance';

CREATE OR REPLACE FUNCTION update_time_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = now() at time zone 'utc';
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username varchar(128) not null default '', -- username
    password varchar(128) not null default '', -- password
    email varchar(128) not null default '',  -- email
    salt varchar(128) not null default '', -- salt
    create_time timestamp without time zone default (now() at time zone 'utc'), --create_time
    update_time timestamp without time zone default (now() at time zone 'utc'), --update_time
    is_deleted smallint not null default 0 -- 1:deleted
); -- users
CREATE INDEX idx_users_name ON users (username);
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_is_deleted ON users (is_deleted);
CREATE TRIGGER update_users_modtime BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE  update_time_column();

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    image_name varchar(128) not null default '', -- image name
    description varchar(512) not null default '', -- comment image description
    create_time timestamp without time zone default (now() at time zone 'utc'), --create_time
    update_time timestamp without time zone default (now() at time zone 'utc'), --update_time
    is_deleted smallint not null default 0 -- 1:deleted
); -- images
CREATE INDEX idx_images_name ON images (image_name);
CREATE INDEX idx_images_is_deleted ON images (is_deleted);
CREATE TRIGGER update_images_modtime BEFORE UPDATE ON images FOR EACH ROW EXECUTE PROCEDURE  update_time_column();


INSERT INTO images ("image_name") VALUES ('eagle-ubuntu:14.04');
INSERT INTO images ("image_name") VALUES ('eagle-centos:7');
INSERT INTO images ("image_name") VALUES ('eagle-fedora:23');
INSERT INTO images ("image_name") VALUES ('eagle-debian:8');

CREATE TABLE instances (
    id SERIAL PRIMARY KEY,
    image_id integer not null default 0, -- image id fk of image
    user_id integer not null default 0, -- user id fk of user
    container_name varchar(128) not null default '', -- container name
    container_serial varchar(128) not null default '', -- container serial
    host varchar(128) not null default '', -- container host ip
    port integer not null default 0, -- container host port
    status smallint not null default 0, -- 1:running 2:stop 3:failed 4:pending 5:unknown
    jump_server varchar(128) not null default '', -- jump server
    create_time timestamp without time zone default (now() at time zone 'utc'), --create_time
    update_time timestamp without time zone default (now() at time zone 'utc'), --update_time
    is_deleted smallint not null default 0 -- 1:deleted
); -- instance
CREATE INDEX idx_container_name ON instances (container_name);
CREATE INDEX idx_container_serial ON instances (container_serial);
CREATE INDEX idx_is_deleted ON instances (is_deleted);
CREATE TRIGGER update_images_modtime BEFORE UPDATE ON instances FOR EACH ROW EXECUTE PROCEDURE  update_time_column();

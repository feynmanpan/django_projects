DROP TABLE IF EXISTS django_migrations;
CREATE TABLE IF NOT EXISTS django_migrations (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, app varchar(255) NOT NULL, name varchar(255) NOT NULL, applied datetime NOT NULL);

INSERT INTO django_migrations VALUES(1,'contenttypes','0001_initial','2019-11-25 14:10:16.166764');

INSERT INTO django_migrations VALUES(2,'auth','0001_initial','2019-11-25 14:10:16.189915');

INSERT INTO django_migrations VALUES(3,'admin','0001_initial','2019-11-25 14:10:16.210198');

INSERT INTO django_migrations VALUES(4,'admin','0002_logentry_remove_auto_add','2019-11-25 14:10:16.262083');

INSERT INTO django_migrations VALUES(5,'admin','0003_logentry_add_action_flag_choices','2019-11-25 14:10:16.278830');

INSERT INTO django_migrations VALUES(6,'contenttypes','0002_remove_content_type_name','2019-11-25 14:10:16.305278');

INSERT INTO django_migrations VALUES(7,'auth','0002_alter_permission_name_max_length','2019-11-25 14:10:16.317752');

INSERT INTO django_migrations VALUES(8,'auth','0003_alter_user_email_max_length','2019-11-25 14:10:16.333305');

INSERT INTO django_migrations VALUES(9,'auth','0004_alter_user_username_opts','2019-11-25 14:10:16.350622');

INSERT INTO django_migrations VALUES(10,'auth','0005_alter_user_last_login_null','2019-11-25 14:10:16.365579');

INSERT INTO django_migrations VALUES(11,'auth','0006_require_contenttypes_0002','2019-11-25 14:10:16.370583');

INSERT INTO django_migrations VALUES(12,'auth','0007_alter_validators_add_error_messages','2019-11-25 14:10:16.386069');

INSERT INTO django_migrations VALUES(13,'auth','0008_alter_user_username_max_length','2019-11-25 14:10:16.401820');

INSERT INTO django_migrations VALUES(14,'auth','0009_alter_user_last_name_max_length','2019-11-25 14:10:16.417372');

INSERT INTO django_migrations VALUES(15,'auth','0010_alter_group_name_max_length','2019-11-25 14:10:16.431312');

INSERT INTO django_migrations VALUES(16,'auth','0011_update_proxy_permissions','2019-11-25 14:10:16.444799');

INSERT INTO django_migrations VALUES(17,'sessions','0001_initial','2019-11-25 14:10:16.451873');

INSERT INTO django_migrations VALUES(18,'mainsite','0001_initial','2019-11-25 14:49:11.141052');

DROP TABLE IF EXISTS auth_group_permissions;
CREATE TABLE IF NOT EXISTS auth_group_permissions (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, group_id integer NOT NULL REFERENCES auth_group (id) , permission_id integer NOT NULL REFERENCES auth_permission (id) );

DROP TABLE IF EXISTS auth_user_groups;
CREATE TABLE IF NOT EXISTS auth_user_groups (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id integer NOT NULL REFERENCES auth_user (id) , group_id integer NOT NULL REFERENCES auth_group (id) );

DROP TABLE IF EXISTS auth_user_user_permissions;
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id integer NOT NULL REFERENCES auth_user (id) , permission_id integer NOT NULL REFERENCES auth_permission (id) );

DROP TABLE IF EXISTS django_admin_log;
CREATE TABLE IF NOT EXISTS django_admin_log (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, action_time datetime NOT NULL, object_id text NULL, object_repr varchar(200) NOT NULL, change_message text NOT NULL, content_type_id integer NULL REFERENCES django_content_type (id) , user_id integer NOT NULL REFERENCES auth_user (id) , action_flag smallint unsigned NOT NULL CHECK (action_flag >= 0));

INSERT INTO django_admin_log VALUES(1,'2019-11-28 14:50:57.144826','1','TTT1','[{"added": {}}]',7,1,1);

INSERT INTO django_admin_log VALUES(2,'2019-11-28 14:51:07.265491','2','T2','[{"added": {}}]',7,1,1);

INSERT INTO django_admin_log VALUES(3,'2019-11-28 14:51:15.801636','3','T3','[{"added": {}}]',7,1,1);

INSERT INTO django_admin_log VALUES(4,'2019-11-28 14:51:23.972468','4','T4','[{"added": {}}]',7,1,1);

INSERT INTO django_admin_log VALUES(5,'2019-11-28 14:51:31.999655','5','T5','[{"added": {}}]',7,1,1);

INSERT INTO django_admin_log VALUES(6,'2019-12-01 13:14:32.636019','1','T1','[{"changed": {"fields": ["title"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(7,'2019-12-01 13:14:45.538951','1','T1','[{"changed": {"fields": ["slug"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(8,'2019-12-01 13:24:30.916565','1','T1','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(9,'2019-12-01 13:53:10.456899','1','T1','[{"changed": {"fields": ["pub_date"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(10,'2019-12-01 13:53:32.233246','3','T3','[{"changed": {"fields": ["pub_date"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(11,'2019-12-01 13:53:45.486602','2','T2','[{"changed": {"fields": ["pub_date"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(12,'2019-12-01 13:54:02.934658','4','T4','[{"changed": {"fields": ["pub_date"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(13,'2019-12-14 22:37:07.540729','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(14,'2019-12-14 22:38:36.016974','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(15,'2019-12-14 22:38:59.134931','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(16,'2019-12-14 22:53:48.722175','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(17,'2019-12-14 22:55:10.137230','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(18,'2019-12-14 23:01:45.446486','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

INSERT INTO django_admin_log VALUES(19,'2019-12-14 23:34:51.973237','5','T5','[{"changed": {"fields": ["body"]}}]',7,1,2);

DROP TABLE IF EXISTS django_content_type;
CREATE TABLE IF NOT EXISTS django_content_type (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, app_label varchar(100) NOT NULL, model varchar(100) NOT NULL);

INSERT INTO django_content_type VALUES(1,'admin','logentry');

INSERT INTO django_content_type VALUES(2,'auth','permission');

INSERT INTO django_content_type VALUES(3,'auth','group');

INSERT INTO django_content_type VALUES(4,'auth','user');

INSERT INTO django_content_type VALUES(5,'contenttypes','contenttype');

INSERT INTO django_content_type VALUES(6,'sessions','session');

INSERT INTO django_content_type VALUES(7,'mainsite','post');

DROP TABLE IF EXISTS auth_permission;
CREATE TABLE IF NOT EXISTS auth_permission (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, content_type_id integer NOT NULL REFERENCES django_content_type (id) , codename varchar(100) NOT NULL, name varchar(255) NOT NULL);

INSERT INTO auth_permission VALUES(1,1,'add_logentry','Can add log entry');

INSERT INTO auth_permission VALUES(2,1,'change_logentry','Can change log entry');

INSERT INTO auth_permission VALUES(3,1,'delete_logentry','Can delete log entry');

INSERT INTO auth_permission VALUES(4,1,'view_logentry','Can view log entry');

INSERT INTO auth_permission VALUES(5,2,'add_permission','Can add permission');

INSERT INTO auth_permission VALUES(6,2,'change_permission','Can change permission');

INSERT INTO auth_permission VALUES(7,2,'delete_permission','Can delete permission');

INSERT INTO auth_permission VALUES(8,2,'view_permission','Can view permission');

INSERT INTO auth_permission VALUES(9,3,'add_group','Can add group');

INSERT INTO auth_permission VALUES(10,3,'change_group','Can change group');

INSERT INTO auth_permission VALUES(11,3,'delete_group','Can delete group');

INSERT INTO auth_permission VALUES(12,3,'view_group','Can view group');

INSERT INTO auth_permission VALUES(13,4,'add_user','Can add user');

INSERT INTO auth_permission VALUES(14,4,'change_user','Can change user');

INSERT INTO auth_permission VALUES(15,4,'delete_user','Can delete user');

INSERT INTO auth_permission VALUES(16,4,'view_user','Can view user');

INSERT INTO auth_permission VALUES(17,5,'add_contenttype','Can add content type');

INSERT INTO auth_permission VALUES(18,5,'change_contenttype','Can change content type');

INSERT INTO auth_permission VALUES(19,5,'delete_contenttype','Can delete content type');

INSERT INTO auth_permission VALUES(20,5,'view_contenttype','Can view content type');

INSERT INTO auth_permission VALUES(21,6,'add_session','Can add session');

INSERT INTO auth_permission VALUES(22,6,'change_session','Can change session');

INSERT INTO auth_permission VALUES(23,6,'delete_session','Can delete session');

INSERT INTO auth_permission VALUES(24,6,'view_session','Can view session');

INSERT INTO auth_permission VALUES(25,7,'add_post','Can add post');

INSERT INTO auth_permission VALUES(26,7,'change_post','Can change post');

INSERT INTO auth_permission VALUES(27,7,'delete_post','Can delete post');

INSERT INTO auth_permission VALUES(28,7,'view_post','Can view post');

DROP TABLE IF EXISTS auth_user;
CREATE TABLE IF NOT EXISTS auth_user (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, password varchar(128) NOT NULL, last_login datetime NULL, is_superuser bool NOT NULL, username varchar(150) NOT NULL UNIQUE, first_name varchar(30) NOT NULL, email varchar(254) NOT NULL, is_staff bool NOT NULL, is_active bool NOT NULL, date_joined datetime NOT NULL, last_name varchar(150) NOT NULL);

INSERT INTO auth_user VALUES(1,'pbkdf2_sha256$150000$aHMxl7EUICza$78Tl/H5Fi61sU74w49THM6OduIL0S/jhHcXw/j41tA0=','2020-01-25 03:06:52.297794',1,'admin','','feynmanpan@gmail.com',1,1,'2019-11-28 13:56:19.621232','');

DROP TABLE IF EXISTS auth_group;
CREATE TABLE IF NOT EXISTS auth_group (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, name varchar(150) NOT NULL UNIQUE);

DROP TABLE IF EXISTS django_session;
CREATE TABLE IF NOT EXISTS django_session (session_key varchar(40) NOT NULL PRIMARY KEY, session_data text NOT NULL, expire_date datetime NOT NULL);

INSERT INTO django_session VALUES('zxvhppnxjuj0zs5y799bn3yms8e41kib','MmQ0NmFjYjQ4ZDc0NGJiYjJjMjIwNWFkNDliZmVjMTFhM2Y1MjEyZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNzM5NTBkNjAyN2NlNWM4OGZlMzYzNjQzN2Y5ZjgwOThhYzE1MjJkIn0=','2019-12-12 14:49:39.435362');

INSERT INTO django_session VALUES('jbvk1dl211cbx4wtkmrbe5eme38nfphu','MmQ0NmFjYjQ4ZDc0NGJiYjJjMjIwNWFkNDliZmVjMTFhM2Y1MjEyZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNzM5NTBkNjAyN2NlNWM4OGZlMzYzNjQzN2Y5ZjgwOThhYzE1MjJkIn0=','2019-12-15 13:11:57.184477');

INSERT INTO django_session VALUES('104dqlv2uxcj8lpgs6b2bw9knb4wjhdw','MmQ0NmFjYjQ4ZDc0NGJiYjJjMjIwNWFkNDliZmVjMTFhM2Y1MjEyZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNzM5NTBkNjAyN2NlNWM4OGZlMzYzNjQzN2Y5ZjgwOThhYzE1MjJkIn0=','2019-12-28 22:36:39.248017');

INSERT INTO django_session VALUES('zvp8s1ks9gjqnpxu9du3w3hdp27dn6vm','MmQ0NmFjYjQ4ZDc0NGJiYjJjMjIwNWFkNDliZmVjMTFhM2Y1MjEyZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNzM5NTBkNjAyN2NlNWM4OGZlMzYzNjQzN2Y5ZjgwOThhYzE1MjJkIn0=','2020-02-08 03:06:52.303268');

DROP TABLE IF EXISTS mainsite_post;
CREATE TABLE IF NOT EXISTS mainsite_post (id integer NOT NULL PRIMARY KEY AUTO_INCREMENT, title varchar(200) NOT NULL, slug varchar(200) NOT NULL, body text NOT NULL, pub_date datetime NOT NULL);

INSERT INTO mainsite_post VALUES(1,'T1','S1','我是第一篇','2019-11-20 14:50:00');

INSERT INTO mainsite_post VALUES(2,'T2','S2','B2','2019-11-21 14:50:00');

INSERT INTO mainsite_post VALUES(3,'T3','S3','B3','2019-11-25 14:51:00');

INSERT INTO mainsite_post VALUES(4,'T4','S4','B4','2019-11-26 14:51:00');

INSERT INTO mainsite_post VALUES(5,'T5','S5',replace(replace('## 22\r\n組組組組組組組組組組是123B5Bootstrap是一組用於網站和網路應用程式開發的開源前端框架，包括HTML、CSS及JavaScript的框架，提供字體排印、表單、按鈕、導航及其他各種元件及Javascript擴充套件，旨在使動態網頁和Web應用的開發更加容易。','\r',char(13)),'\n',char(10)),'2019-11-28 14:51:00');

CREATE INDEX `auth_group_permissions_group_id_b120cbf9` ON `auth_group_permissions` (`group_id`);

CREATE INDEX `auth_group_permissions_permission_id_84c5c92e` ON `auth_group_permissions` (`permission_id`);

CREATE INDEX `auth_user_groups_user_id_6a12ed8b` ON `auth_user_groups` (`user_id`);

CREATE INDEX `auth_user_groups_group_id_97559544` ON `auth_user_groups` (`group_id`);

CREATE INDEX `auth_user_user_permissions_user_id_a95ead1b` ON `auth_user_user_permissions` (`user_id`);

CREATE INDEX `auth_user_user_permissions_permission_id_1fbb5f2c` ON `auth_user_user_permissions` (`permission_id`);

CREATE INDEX `django_admin_log_content_type_id_c4bce8eb` ON `django_admin_log` (`content_type_id`);

CREATE INDEX `django_admin_log_user_id_c564eba6` ON `django_admin_log` (`user_id`);

CREATE INDEX `auth_permission_content_type_id_2f476e4b` ON `auth_permission` (`content_type_id`);

CREATE INDEX `django_session_expire_date_a5c62663` ON `django_session` (`expire_date`);

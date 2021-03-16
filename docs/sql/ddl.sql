DROP SEQUENCE if EXISTS seq_user_id CASCADE;
CREATE SEQUENCE seq_user_id
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
id BIGINT not null default nextval('seq_user_id'),
uid VARCHAR(256) not null,
salt VARCHAR(56) not null default '',
password VARCHAR(256) not null,
birth_year INTEGER NOT NULL DEFAULT 1970,
birth_month INTEGER NOT NULL DEFAULT 01,
birth_day INTEGER NOT NULL DEFAULT 01,
push_token VARCHAR(256) NOT NULL DEFAULT 'T',
receive_push BOOLEAN NOT NULL DEFAULT 'T',
receive_marketing BOOLEAN NOT NULL DEFAULT 'T',
gender VARCHAR(1) NOT NULL DEFAULT 'f',
created_at timestamp with time zone default now()
);
ALTER TABLE users ADD CONSTRAINT pk_users PRIMARY KEY(id);
ALTER TABLE users ADD CONSTRAINT unique_user_uid UNIQUE (uid);
CREATE INDEX idx_users_uid ON users USING HASH(uid);


DROP SEQUENCE seq_session_id CASCADE;
CREATE SEQUENCE seq_session_id
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;

DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions(
id BIGINT NOT NULL DEFAULT NEXTVAL('seq_session_id'),
session VARCHAR(256) NOT NULL DEFAULT '',
ip_address VARCHAR(40) NOT NULL,
platform VARCHAR(64) NOT NULL,
platform_version VARCHAR(64) NOT NULL,
salt VARCHAR(126) NOT NULL,
update_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
create_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_sessions_session on sessions using hash (session);

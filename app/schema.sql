DROP TABLE if exists user;
CREATE TABLE user (
	user_id integer primary key autoincrement,
	username text not null,
	pw_hash text not null
);

DROP TABLE if exists story;
CREATE TABLE story (
	story_id integer primary key autoincrement,
	title text not null,
	text text not null,
	like integer not null default 0,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
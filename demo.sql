--APP table
CREATE TABLE app
  (
    appid    INTEGER PRIMARY KEY AUTOINCREMENT,
    title    VARCHAR2(128) NOT NULL,
    version  VARCHAR2(64)
  );

--AUTHOR table
CREATE TABLE author
  (
    authorid INTEGER PRIMARY KEY AUTOINCREMENT,
    name		VARCHAR2(64),
    email	VARCHAR2(64),
    company	VARCHAR2(64)
  );

--APP to AUTHOR lookup, supports many to many
CREATE TABLE app_author
  (
    appid INTEGER,
    authorid INTEGER
  );

--Populate schema
insert into app (title, version) values ('AlphaBeta', '1.0-alpha');
insert into author (name, email, company) values ('Jones Smith', 'jones@smith.com','Code Smiths');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);
  
insert into app (title, version) values ('Kimmel Demo', '0.1');
insert into author (name, email, company) values ('Ben Hall','ben@greenteadigital.com','Green Tea Digital');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('HobKnobbery', '4.2-ad5f1d');
insert into author (name, email, company) values ('Bob Robertson','bob@bobsknobs.zone','Bob''s Knobs');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('The New Hotness', '2.0-Final');
insert into author (name, email, company) values ('Hakan Hakkansen', 'sigsev@hackr.io','hackr.io');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('Zebra Tracker', '0.9-RELEASE');
insert into author (name, email, company) values ('Zevariah Zevallos','stripey@zeebraz.com','Zeebraz.com');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);
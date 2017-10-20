--APP
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
    email    VARCHAR2(64),
    company  VARCHAR2(64)
  );

--APP to AUTHOR lookup, support many to many
CREATE TABLE app_author
  (
  	appid INTEGER,
    authorid INTEGER
  );

insert into app (title, version) values ('AlphaBeta', '1.0-alpha');
insert into author (email, company) values ('jones@smith.com','Code Smiths');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);
  
insert into app (title, version) values ('Kimmel Demo', '0.1');
insert into author (email, company) values ('ben@greenteadigital.com','Green Tea Digital');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('HobKnobbery', '4.2-ad5f1d');
insert into author (email, company) values ('bob@bobsknobs','Bob''s Knobs');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('The New Hotness', '2.0');
insert into author (email, company) values ('sigsev@hackr.io','hackr.io');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);

insert into app (title, version) values ('Zebra Tracker', '0.9-RELEASE');
insert into author (email, company) values ('stripey@zeebraz.com','Zeebraz.com');
insert into app_author (appid, authorid) values (
	(SELECT last_insert_rowid() FROM app),
	(SELECT last_insert_rowid() FROM author)
);
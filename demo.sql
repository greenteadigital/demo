--TASK table
CREATE TABLE task
  (
    taskid    		INTEGER PRIMARY KEY AUTOINCREMENT,
    title    		VARCHAR(256) NOT NULL,
    description 		VARCHAR(65536),
    duedate			DATE,
    collaborators	VARCHAR(384),
    progressnotes	VARCHAR(65536),
    completiondate	DATE
  );

--AUTHOR table
CREATE TABLE author
  (
    authorid INTEGER PRIMARY KEY AUTOINCREMENT,
    name    VARCHAR(64),
    email   VARCHAR(64)
  );

--TASK to AUTHOR lookup, supports many to many
CREATE TABLE task_author
  (
    taskid INTEGER,
    authorid INTEGER
  );

--Populate schema
BEGIN TRANSACTION;
insert into task (title, description, duedate, collaborators) values (
	'Send offer to Ben Hall',
	'Candidate shows promise, would be good fit for team. Says commute is not a problem. ',
	'2018-01-29 17:00:00',
	'Ty-Lerr Parrmelhee');
insert into author (name, email) values ('Juan Beauhannon', 'juan@example.com');
insert into task_author (taskid, authorid) values (
	(SELECT last_insert_rowid() FROM task),
	(SELECT last_insert_rowid() FROM author)
);
COMMIT;

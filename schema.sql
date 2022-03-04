CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name TEXT UNIQUE,
	password TEXT,
	role INTEGER
);

CREATE TABLE profile_text (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	profile_text TEXT,
	visible INTEGER
);

CREATE TABLE job_experience (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	employer TEXT,
	role TEXT,
	description TEXT,
	beginning DATE,
	ended DATE
);

CREATE TABLE education (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	school TEXT,
	level TEXT,
	description TEXT,
	beginning DATE,
	graduation DATE
);

CREATE TABLE application_forms (
        id SERIAL PRIMARY KEY,
        question_1 TEXT,
        question_2 TEXT,
        question_3 TEXT,
        question_4 TEXT,
        question_5 TEXT
);


CREATE TABLE jobs (
	id SERIAL PRIMARY KEY,
	employer_id INTEGER REFERENCES users,
	opened DATE,
	closing DATE,
	role TEXT,
	description TEXT,
	beginning DATE,
	ends DATE,
	status INTEGER,
	visible INTEGER,
	form INTEGER REFERENCES application_forms
);


CREATE TABLE applications (
	id SERIAL PRIMARY KEY,
	form_id INTEGER REFERENCES application_forms,
	job_id INTEGER REFERENCES jobs,
	answer_1 TEXT,
	answer_2 TEXT,
	answer_3 TEXT,
	answer_4 TEXT,
	answer_5 TEXT,
	sent_at TIMESTAMP,
	user_id INTEGER REFERENCES users,
	status INTEGER,
	CONSTRAINT unique_application UNIQUE(job_id, user_id)
);

CREATE TABLE employers (
	id SERIAL PRIMARY KEY,
	name TEXT,
	password TEXT,
	profile_text TEXT
);

CREATE TABLE employees (
	id SERIAL PRIMARY KEY,
	name TEXT,
	password TEXT,
	profile_text TEXT
);

CREATE TABLE job_experience (
	id SERIAL PRIMARY KEY,
	employee_id INTEGER REFERENCES employees,
	employer TEXT,
	role TEXT,
	description TEXT,
	beginning DATE,
	ended DATE
);

CREATE TABLE education (
	id SERIAL PRIMARY KEY,
	employee_id INTEGER REFERENCES employees,
	school TEXT,
	level TEXT,
	description TEXT,
	beginning DATE,
	graduation DATE
);

CREATE TABLE application_forms (
        id SERIAL PRIMARY KEY,
        opened TIMESTAMP,
        closing DATE,
        question_1 TEXT,
        question_2 TEXT,
        question_3 TEXT,
        question_4 TEXT,
        question_5 TEXT
);


CREATE TABLE jobs (
	id SERIAL PRIMARY KEY,
	employer_id INTEGER REFERENCES employers,
	employee_id INTEGER REFERENCES employees,
	role TEXT,
	description TEXT,
	beginning DATE,
	ends DATE,
	status INTEGER,
	visible INTEGER,
	form INTEGER REFERENCES application_forms,
	visible_in_profile INTEGER
);


CREATE TABLE applications (
	form_id INTEGER REFERENCES application_forms,
	job_id INTEGER REFERENCES jobs,
	answer_1 TEXT,
	answer_2 TEXT,
	answer_3 TEXT,
	amswer_4 TEXT,
	answer_5 TEXT,
	sent_at TIMESTAMP,
	employee_id INTEGER REFERENCES employees
);

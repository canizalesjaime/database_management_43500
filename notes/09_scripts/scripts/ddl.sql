CREATE DATABASE employees2;

\c employees2

CREATE TABLE employees
(
emp_no integer NOT NULL,
birth_date date NOT NULL,
first_name character varying(14) NOT NULL,
last_name character varying(16) NOT NULL,
gender character varying NOT NULL,
hire_date date NOT NULL,
PRIMARY KEY (emp_no)
);


CREATE TABLE departments (
dept_no CHAR(4) NOT NULL,
dept_name VARCHAR(40) NOT NULL,
PRIMARY KEY (dept_no)
);

-- DROP TABLE departments;
DROP TABLE IF EXISTS departments;


CREATE TABLE departments (
dept_no CHAR(4) NOT NULL,
dept_name VARCHAR(40) NOT NULL,
PRIMARY KEY (dept_no)
);



-- ALTER TABLE: DROP COLUMN
ALTER TABLE departments
DROP COLUMN dept_name;


-- ALTER TABLE: ADD COLUMN
ALTER TABLE departments
ADD COLUMN dept_name varchar(40);


-- ALTER TABLE: RENAME COLUMN
ALTER TABLE departments
RENAME COLUMN dept_no TO department_no;


-- ALTER TABLE: drop constraint (e.g. primary key)
-- find the constraint name using \d departments in PSQL tool
ALTER TABLE departments
DROP CONSTRAINT departments_pkey;


-- ALTER TABLE: add constraint (e.g. primary key)
ALTER TABLE departments
ADD PRIMARY KEY (department_no);


ALTER TABLE departments
ALTER COLUMN dept_name TYPE VARCHAR(43);


ALTER TABLE departments
ALTER COLUMN dept_name DROP NOT NULL;


ALTER TABLE departments
ALTER COLUMN dept_name SET NOT NULL;


TRUNCATE TABLE departments;
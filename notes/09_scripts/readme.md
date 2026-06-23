# Our first sql script
Lets consider our docker case, where the database management system we use is ephemeral. It would be annoying to 
have to run each individual command to create the database, tables, and fill out the tables each time we open a container.
To solve this problem(and many others), we can use an sql script that will run all our commands.

## How to run a script
There are many ways to run a script, here we will go over a few(Note sql script should include extension .sql)

### Method 1
```psql -U username -d database_name -f file.sql``` <br>

runs the script without logging you into psql.

### Method 2
```\i /path/to/file.sql```<br>

Runs a SQL file from inside the psql interactive shell.

### Using \! 
Runs bash (shell) commands from inside psql(Temporary escape from PostgreSQL to the operating system shell).

Example:
```
\! ls
```

This will list files in the current directory.

```
\! pwd
```
Shows current directory.

## Our Scripts
create_school_database.sql:
```sql
CREATE DATABASE school;

\c school

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(50),
    age INTEGER
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    department VARCHAR(50),
    credits INTEGER
);

CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INTEGER
);

INSERT INTO students (name, major, age)
VALUES
('Alice', 'Computer Science', 21),
('Bob', 'Mathematics', 22),
('Charlie', 'Physics', 20),
('Diana', 'Biology', 23);

INSERT INTO courses (course_name, department, credits)
VALUES
('Database Systems', 'Computer Science', 3),
('Calculus II', 'Mathematics', 4),
('Quantum Mechanics', 'Physics', 4),
('Organic Chemistry', 'Chemistry', 3);

INSERT INTO professors (name, department, salary)
VALUES
('Dr. Smith', 'Computer Science', 90000),
('Dr. Johnson', 'Mathematics', 85000),
('Dr. Lee', 'Physics', 92000),
('Dr. Brown', 'Chemistry', 88000);
```

delete_school_database.sql(Make sure you are not logged into the database you want to delete):
```sql
DROP TABLE students;
DROP TABLE courses;
DROP TABLE professors;

DROP DATABASE school;
```

### Do it!
Now you can try both methods for running a script by running the two scripts above!

To Consider:
* Some environments (Docker, hosted DBs, school servers) do NOT allow CREATE DATABASE inside scripts. So you have to manually add the database yourself, then run the script.


# DDL vs DML

SQL commands are often divided into categories.

## DDL = Data Definition Language

DDL changes the **structure** of the database.

Think:

> "What tables, columns, and indexes exist?"

### Common DDL commands

```sql
CREATE TABLE employees (
    emp_no INTEGER PRIMARY KEY,
    first_name TEXT
);
```

```sql
ALTER TABLE employees
ADD COLUMN salary INTEGER;
```

```sql
DROP TABLE employees;
```


### DDL Keywords

- `CREATE`
- `ALTER`
- `DROP`
- `TRUNCATE`

---

## DML = Data Manipulation Language

DML changes the **data inside** tables.

Think:

> "What rows exist?"

### Insert data

```sql
INSERT INTO employees
VALUES (1, 'John');
```

### Read data

```sql
SELECT *
FROM employees;
```

### Update data

```sql
UPDATE employees
SET first_name = 'Jane'
WHERE emp_no = 1;
```

### Delete data

```sql
DELETE FROM employees
WHERE emp_no = 1;
```

### DML Keywords

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`

---

## Example

### DDL

```sql
CREATE TABLE employees (
    emp_no INTEGER PRIMARY KEY,
    first_name TEXT
);
```

Creates the table.

### DML

```sql
INSERT INTO employees
VALUES (1, 'John');
```

Adds a row.

---

# Exporting Data to CSV

A CSV file looks like:

```csv
emp_no,first_name
1,John
2,Jane
3,Bob
```

CSV files are useful because they work with:

- Excel
- Python
- Pandas
- Data analysis tools

---

## Export an entire table

```sql
\COPY employees
TO './employees.csv'
WITH CSV HEADER
```

Result:

```csv
emp_no,first_name
1,John
2,Jane
3,Bob
```

---

## Export a query

Often you don't want the whole table.

```sql
\COPY (
    SELECT emp_no, first_name
    FROM employees
    WHERE emp_no < 100
)
TO './small_employees.csv'
WITH CSV HEADER
```

Only matching rows are exported.

---

## Why `\COPY` instead of `COPY`?

### Server-side COPY

```sql
COPY employees
TO '/tmp/employees.csv'
WITH CSV HEADER;
```

The PostgreSQL server writes the file.

This often requires special permissions.

---

### Client-side \COPY

```sql
\COPY employees
TO './employees.csv'
WITH CSV HEADER
```

`psql` writes the file.

This is what most users want.

---

# Part 3: Importing CSV Files

Suppose we have:

```csv
emp_no,first_name
1,John
2,Jane
3,Bob
```

---

## Create the destination table

```sql
CREATE TABLE employees (
    emp_no INTEGER,
    first_name TEXT
);
```

---

## Import the CSV

```sql
\COPY employees
FROM './employees.csv'
WITH CSV HEADER
```

PostgreSQL reads the file and inserts rows.

Result:

```sql
SELECT * FROM employees;
```

```text
 emp_no | first_name
--------+-----------
      1 | John
      2 | Jane
      3 | Bob
```

---

## What does `HEADER` do?

Without:

```sql
\COPY employees
FROM './employees.csv'
WITH CSV
```

PostgreSQL tries to import:

```text
emp_no
first_name
```

as actual data.

With:

```sql
WITH CSV HEADER
```

the first row is skipped.

---

# Part 4: The `\o` Command

`\o` means:

> Send query output somewhere else.

Normally:

```sql
SELECT * FROM employees;
```

appears on screen.

---

## Redirect output to a file

```sql
\o report.txt
```

Now:

```sql
SELECT * FROM employees;
```

writes the results to:

```text
report.txt
```

instead of your terminal.

---

## Turn output redirection off

```sql
\o
```

Output returns to the screen.

---

## Example

```sql
\o employees_report.txt

SELECT * FROM employees;

\o
```

Creates a text report.

---


# Common Workflow

Explore data:

```sql
SELECT * FROM employees LIMIT 10;
```

Export it:

```sql
\COPY (
    SELECT *
    FROM employees
    WHERE emp_no < 1000
)
TO './employees.csv'
WITH CSV HEADER
```

Open in Excel.

Make edits.

Import back:

```sql
\COPY employees
FROM './employees.csv'
WITH CSV HEADER
```

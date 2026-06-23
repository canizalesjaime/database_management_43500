# Creating a Database in PostgreSQL (psql)

## Introduction

In this lecture, we will learn how to:

- Primary, Composite, Compound Keys
- Serial and Constraints
- Create a database
- Connect to a database
- Create tables
- Insert and query data
- Modify and delete data
- Delete tables and databases
- Basics to writing a script and running an sql script

Unfortunately, we do not have write access in the csci232-server at Hunter. To get around this, you can either install psql on your local computer or use docker.

# Primary Keys

A primary key is a column (or group of columns) in a database table that uniquely identifies each row in the table. Think of it as an ID number for every record.

A primary key ensures that:

- Every row is unique
- No duplicate records exist
- Each row can be easily referenced

Example:

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(50)
);
```

In this example:

- `student_id` is the primary key
- Every student must have a unique ID
- PostgreSQL automatically generates IDs because of `SERIAL`


# Compound and Composite Keys
- Composite key: A key made up of two or more columns.
- Compound key: A composite key where all the columns are foreign keys.

### Example of a composite key that is not a compound key:

```sql
CREATE TABLE orders (
    order_number INT,
    order_date DATE,
    PRIMARY KEY (order_number, order_date)
);
```
The primary key (order_number, order_date) uses multiple columns, so it's composite, but the columns are not foreign keys.

### Example of a compound key:

```sql
CREATE TABLE enrollments (
    student_id INT REFERENCES students(id),
    course_id INT REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);
```

The primary key (student_id, course_id):
- uses multiple columns → composite key
- both columns are foreign keys → compound key


# Important Table Concepts: SERIAL and Constraints

## 1. SERIAL (Auto-Incrementing Primary Keys)

In PostgreSQL, `SERIAL` is used to automatically generate unique integer values for a column. It is commonly used for primary keys.

### Example:

```sql
student_id SERIAL PRIMARY KEY
```

### What it does:

* Automatically assigns a unique number to each new row
* Increases the value automatically (1, 2, 3, 4, ...)
* Saves you from manually entering IDs

### Important Note:

`SERIAL` is not a true data type. It is shorthand for:

* Creating an integer column
* Creating a sequence (counter)
* Setting the default value of the column to the next value in the sequence

### Example behavior:

```sql
INSERT INTO students (name, major)
VALUES ('Alice', 'Computer Science');
```

PostgreSQL automatically assigns:

```
student_id = 1
```

Next insert:

```
student_id = 2
```

---

## 2. Table Constraints

Constraints are rules applied to columns to ensure data integrity. They restrict what data can be stored in a table.

---

### a) NOT NULL

Ensures a column cannot be empty.

```sql
name VARCHAR(100) NOT NULL
```

Meaning:

* Every row must have a value for `name`

---

### b) UNIQUE

Ensures all values in a column are different.

```sql
email VARCHAR(255) UNIQUE
```

Meaning:

* No two rows can have the same email

---

### c) PRIMARY KEY

A combination of:

* NOT NULL
* UNIQUE

Used to uniquely identify each row.

```sql
student_id SERIAL PRIMARY KEY
```

Meaning:

* Each student has a unique ID
* Cannot be NULL

---

### d) FOREIGN KEY

Links a column to a primary key in another table.

```sql
student_id INT REFERENCES students(student_id)
```

Meaning:

* Value must exist in the referenced table
* Maintains relationships between tables

---

### e) CHECK (Optional Advanced Constraint)

Ensures values satisfy a condition.

```sql
age INT CHECK (age >= 0)
```

Meaning:

* Age cannot be negative



# Creating a New Database

Use the `CREATE DATABASE` command.

```sql
CREATE DATABASE school;
```

If successful:

```text
CREATE DATABASE
```

# Connecting to the Database

To switch into the new database:

```sql
\c school
```

Output:

```text
You are now connected to database 'school'.
```

# Creating Tables

A database stores information inside tables.

In this example, we will create three tables:

- students
- courses
- professors

## Students Table

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(50),
    age INTEGER
);
```

## Courses Table

```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    department VARCHAR(50),
    credits INTEGER
);
```

## Professors Table

```sql
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INTEGER
);
```

# Viewing Tables

To list tables:

```sql
\dt
```

You should see:

```text
students
courses
professors
```

# Inserting Data

## Insert Rows into Students

```sql
INSERT INTO students (name, major, age)
VALUES
('Alice', 'Computer Science', 21),
('Bob', 'Mathematics', 22),
('Charlie', 'Physics', 20),
('Diana', 'Biology', 23);
```

## Insert Rows into Courses

```sql
INSERT INTO courses (course_name, department, credits)
VALUES
('Database Systems', 'Computer Science', 3),
('Calculus II', 'Mathematics', 4),
('Quantum Mechanics', 'Physics', 4),
('Organic Chemistry', 'Chemistry', 3);
```

## Insert Rows into Professors

```sql
INSERT INTO professors (name, department, salary)
VALUES
('Dr. Smith', 'Computer Science', 90000),
('Dr. Johnson', 'Mathematics', 85000),
('Dr. Lee', 'Physics', 92000),
('Dr. Brown', 'Chemistry', 88000);
```

# Querying Data

## View All Students

```sql
SELECT * FROM students;
```

## View All Courses

```sql
SELECT * FROM courses;
```

## View All Professors

```sql
SELECT * FROM professors;
```

## Example Output

```text
 student_id |  name   |        major        | age
------------+---------+---------------------+-----
 1          | Alice   | Computer Science    | 21
 2          | Bob     | Mathematics         | 22
 3          | Charlie | Physics             | 20
 4          | Diana   | Biology             | 23
```

# Modifying and Deleting Data

## Updating a Row

Suppose Alice changes her major.

```sql
UPDATE students
SET major = 'Software Engineering'
WHERE name = 'Alice';
```

Check the result:

```sql
SELECT * FROM students;
```

## Deleting a Row

Delete the course `Organic Chemistry`.

```sql
DELETE FROM courses
WHERE course_name = 'Organic Chemistry';
```

View remaining rows:

```sql
SELECT * FROM courses;
```

## Deleting a Column

Remove the `salary` column from the professors table.

```sql
ALTER TABLE professors
DROP COLUMN salary;
```

Check the updated table structure:

```sql
\d professors
```

# Deleting Tables and Database

## Delete All Tables

```sql
DROP TABLE students;
DROP TABLE courses;
DROP TABLE professors;
```

Verify they are gone:

```sql
\dt
```

## Delete the Database

First connect back to the default postgres database:

```sql
\c postgres
```

Now delete the `school` database:

```sql
DROP DATABASE school;
```


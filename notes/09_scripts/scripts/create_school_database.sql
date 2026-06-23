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
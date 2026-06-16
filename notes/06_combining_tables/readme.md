# UNION

`UNION` combines the results of multiple `SELECT` statements into one result set.
Think of stacking tables on top of each other.

---

# Basic Syntax

```sql
SELECT column_name
FROM table1

UNION

SELECT column_name
FROM table2;
```

Rules:
- same number of columns
- compatible data types
- columns in the same order
- duplicates removed automatically

---

# Example 1 — Employee Numbers

Combine employee numbers from:
- department employees
- department managers

```sql
SELECT emp_no
FROM dept_emp

UNION

SELECT emp_no
FROM dept_manager;
```

Result:
- one combined list of employee numbers
- duplicates removed

---

# Example 2 — UNION ALL

Keep duplicates instead of removing them.

```sql
SELECT emp_no
FROM dept_emp

UNION ALL

SELECT emp_no
FROM dept_manager;
```

Managers may appear twice because duplicates are preserved.

---

# Example 3 — Employee First Names

```sql
SELECT first_name
FROM employees
WHERE gender = 'M'

UNION

SELECT first_name
FROM employees
WHERE gender = 'F';
```

Result:
- one combined list of first names
- repeated names appear only once

---

# Example 4 — Combining Titles

```sql
SELECT title
FROM titles
WHERE title LIKE '%Engineer%'

UNION

SELECT title
FROM titles
WHERE title LIKE '%Manager%';
```

Example result:

| title |
|---|
| Engineer |
| Senior Engineer |
| Manager |
| Technique Leader |

---

# Example 5 — Multiple Columns

```sql
SELECT emp_no, from_date
FROM dept_emp

UNION

SELECT emp_no, from_date
FROM dept_manager;
```

Duplicates are checked using the entire row.

---

# Example 6 — ORDER BY with UNION

```sql
SELECT first_name
FROM employees
WHERE hire_date < '1990-01-01'

UNION

SELECT first_name
FROM employees
WHERE hire_date >= '1990-01-01'

ORDER BY first_name;
```

`ORDER BY` must go at the end, and sorts the table after union is applied.

---


# Example 7 - Column naming in UNION

Column names come from FIRST SELECT only.

Example:
```sql
SELECT emp_no, salary FROM salaries_current
UNION
SELECT emp_no, salary FROM salaries_old;

Output columns:
emp_no | salary
```
---

# Best practice: alias columns

```sql
SELECT emp_no AS employee_id,
       salary AS amount
FROM salaries_current

UNION

SELECT emp_no,
       salary 
FROM salaries_old;
```

---

# Example 8 - Tracking source table in UNION

UNION does NOT preserve origin.

So you must manually add it.

Example:
```sql
SELECT emp_no,
       salary,
       'current' AS source
FROM salaries
WHERE to_date = '9999-01-01'

UNION ALL

SELECT emp_no,
       salary,
       'historical' AS source
FROM salaries
WHERE to_date != '9999-01-01';
```
---

# Result:

emp_no | salary | source

10001  | 70000  | current
10001  | 60000  | historical


**Another Example:** 
```sql
SELECT emp_no,
       'Department Employee' AS category
FROM dept_emp

UNION

SELECT emp_no,
       'Department Manager' AS category
FROM dept_manager;
```

Example result:

| emp_no | category |
|---|---|
| 10001 | Department Employee |
| 110022 | Department Manager |

---

# Common Error — Different Number of Columns

Wrong:

```sql
SELECT emp_no, first_name
FROM employees

UNION

SELECT dept_no
FROM departments;
```

Why?
- first query returns 2 columns
- second query returns 1 column

---

# Common Error — Incompatible Data Types

Wrong:

```sql
SELECT emp_no
FROM employees

UNION

SELECT dept_name
FROM departments;
```

Why?
- `emp_no` is an integer
- `dept_name` is text

---

# Performance Note

- `UNION` removes duplicates
- removing duplicates takes extra work
- `UNION ALL` is usually faster

Use `UNION ALL` when duplicate removal is not needed.


# SQL JOIN
**Intuition:** Think of combining tables by placing them side by side, then using a condition to solve for the tables not having the same number of rows.

## Syntax
```sql
SELECT t1.column1,...,t2.column1,...
FROM table1 t1
JOIN table2 t2
ON t1.join_key_column = t12.join_key_column;
```

# 0. The most important concept: JOIN KEYS

A JOIN works because two tables share related columns.

These columns are called:

- join keys
- relationship columns
- sometimes primary/foreign keys

---

# Core join keys in this database

| Table | Key Column | Meaning |
|---|---|---|
| employees | emp_no | unique employee ID |
| salaries | emp_no | employee this salary belongs to |
| dept_emp | emp_no | employee assigned to department |
| dept_emp | dept_no | department assignment |
| departments | dept_no | unique department ID |

---

# Primary Key vs Foreign Key

## Primary Key

A column that uniquely identifies a row.

Example:

```sql
employees.emp_no
```

Every employee has:
- one unique employee number
- no duplicates

Example:

| emp_no | first_name |
|---|---|
| 10001 | Georgi |
| 10002 | Bezalel |

---

## Foreign Key

A column that references another table’s primary key.

Example:

```sql
salaries.emp_no
```

Meaning:

```text
"this salary belongs to employee X"
```

---

# Important: JOIN columns do NOT have to be primary or foreign keys

This is a major misconception.

SQL can JOIN on:
- primary keys
- foreign keys
- normal columns
- expressions
- ranges
- arbitrary boolean conditions

The database does NOT require:

```text
PRIMARY KEY ↔ FOREIGN KEY
```

for a JOIN to work.

---

# Example: joining on first name

```sql
SELECT *
FROM employees e
JOIN employees e2
ON e.first_name = e2.first_name;
```

No PK/FK relationship.

Still valid SQL.

---

# Example: joining on salary amount

```sql
SELECT *
FROM salaries s1
JOIN salaries s2
ON s1.salary = s2.salary;
```

Groups employees with equal salaries.

---

# Example: joining on an expression

```sql
SELECT *
FROM employees e
JOIN salaries s
ON e.emp_no + 100 = s.emp_no;
```

Weird, but legal.

---

# Key insight

A JOIN is fundamentally:

```text
a row matching operation
```

The ON clause is just a boolean condition.

If condition evaluates TRUE:

```text
rows combine
```

---

# Why PK/FK joins are preferred

| Benefit | Reason |
|---|---|
| correctness | relationships are meaningful |
| uniqueness | avoids accidental duplication |
| indexing | fast lookups |
| integrity | constraints can be enforced |
| readability | easier to understand |

---

# 1. INNER JOIN — only matching rows survive

## Query

```sql
SELECT e.emp_no,
       e.first_name,
       s.salary
FROM employees e
INNER JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Join key used

```sql
e.emp_no = s.emp_no
```

| Table | Column | Role |
|---|---|---|
| employees | emp_no | primary key |
| salaries | emp_no | foreign key |

---

# What PostgreSQL actually does

## Step 1: Read employee row

Example:

| emp_no | first_name |
|---|---|
| 10001 | Georgi |

---

## Step 2: Search salaries table

Find rows where:

```text
salaries.emp_no = 10001
```

Example matches:

| emp_no | salary |
|---|---|
| 10001 | 60117 |
| 10001 | 62102 |

---

## Step 3: Combine rows

Result:

| emp_no | first_name | salary |
|---|---|---|
| 10001 | Georgi | 60117 |
| 10001 | Georgi | 62102 |

---

# Key insight

INNER JOIN keeps:

```text
only rows where join keys match
```

Rows with no match disappear.

---
**Another Example:**
We simulate two tables from the Employees database style:

---

# Table 1: employees (PRIMARY KEY = emp_no)

| emp_no | name    |
|--------|---------|
| 10001  | Alice   |
| 10002  | Bob     |
| 10003  | Carol   |
| 10004  | David   |

- emp_no is the PRIMARY KEY
- every value is unique

---

# Table 2: salaries (FOREIGN KEY = emp_no)

| emp_no | salary |
|--------|--------|
| 10002  | 70000  |
| 10003  | 80000  |
| 10005  | 90000  |

- emp_no references employees.emp_no (foreign key conceptually)
- BUT 10005 does NOT exist in employees

---

# INNER JOIN query

```sql
SELECT e.emp_no,
       e.name,
       s.salary
FROM employees e
INNER JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Step-by-step matching logic

INNER JOIN keeps ONLY rows where keys match.

We compare:

employees.emp_no  ↔  salaries.emp_no

---

## Match results

### 10001
- exists in employees
- NOT in salaries
→ removed

---

### 10002
- exists in employees
- exists in salaries
→ KEEP

---

### 10003
- exists in employees
- exists in salaries
→ KEEP

---

### 10004
- exists in employees
- NOT in salaries
→ removed

---

### 10005
- exists in salaries
- NOT in employees
→ removed

---

# Final INNER JOIN output

| emp_no | name  | salary |
|--------|-------|--------|
| 10002  | Bob   | 70000  |
| 10003  | Carol | 80000  |

---

# Key insight

INNER JOIN only keeps:

```
intersection of both tables on join key
```

INNER JOIN = only rows where BOTH tables agree on emp_no

---


# 2. LEFT JOIN — preserve everything on the left

## Query

```sql
SELECT e.emp_no,
       e.first_name,
       s.salary
FROM employees e
LEFT JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Join key used

```sql
employees.emp_no = salaries.emp_no
```

---

# Internal logic

## PostgreSQL first tries matching rows

Same as INNER JOIN.

---

## If no salary exists

The employee row still survives:

| emp_no | first_name |
|---|---|
| 10099 | Alice |

Missing salary columns become:

| salary |
|---|
| NULL |

---

# Key insight

LEFT JOIN means:

```text
"never discard rows from the left table"
```

---

# 3. RIGHT JOIN — preserve everything on the right

## Query

```sql
SELECT e.emp_no,
       e.first_name,
       s.salary
FROM employees e
RIGHT JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Join key used

```sql
employees.emp_no = salaries.emp_no
```

---

# Internal logic

Now PostgreSQL treats:

```text
salaries as the guaranteed table
```

Every salary row survives.

If employee missing:

| emp_no | first_name |
|---|---|
| NULL | NULL |

---

# Key insight

RIGHT JOIN is basically:

```text
LEFT JOIN with reversed table order
```

---

# 4. FULL OUTER JOIN — preserve everything

## Query

```sql
SELECT e.emp_no,
       e.first_name,
       s.salary
FROM employees e
FULL OUTER JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Join key used

```sql
employees.emp_no = salaries.emp_no
```

---

# Internal logic

PostgreSQL outputs:

## A. Matching rows
Employee + salary

## B. Left-only rows
Employee + NULL salary

## C. Right-only rows
NULL employee + salary

---

# Key insight

FULL OUTER JOIN means:

```text
"preserve both tables even if unmatched"
```

---

# 5. CROSS JOIN — no join key at all

## Query

```sql
SELECT e.first_name,
       d.dept_name
FROM employees e
CROSS JOIN departments d;
```

---

# Join key used

```text
NONE
```

No:
- ON
- relationship
- matching condition

---

# Internal logic

PostgreSQL literally does:

```text
every employee
paired with
every department
```

---

# Example

If:
- 300,000 employees
- 9 departments

Then:

```text
300,000 × 9 = 2,700,000 rows
```

---

# Key insight

CROSS JOIN creates:

```text
all possible combinations
```

---

# 6. Multi-table JOIN — chaining relationships

## Query

```sql
SELECT e.emp_no,
       e.first_name,
       d.dept_name
FROM employees e
JOIN dept_emp de
ON e.emp_no = de.emp_no
JOIN departments d
ON de.dept_no = d.dept_no;
```

---

# Join keys used

## First JOIN

```sql
e.emp_no = de.emp_no
```

| Table | Column | Role |
|---|---|---|
| employees | emp_no | primary key |
| dept_emp | emp_no | foreign key |

---

## Second JOIN

```sql
de.dept_no = d.dept_no
```

| Table | Column | Role |
|---|---|---|
| dept_emp | dept_no | foreign key |
| departments | dept_no | primary key |

---

# Internal logic

## Step 1

Connect employees → department assignments

```text
employee 10001 belongs to department d005
```

---

## Step 2

Translate department ID into department name

```text
d005 → Development
```

---

# Key insight

This is relational database design:

```text
IDs connect tables
```

not names.

Because IDs are:
- unique
- compact
- stable
- index-friendly

---

# 7. Relationship Types — Using the Employees Database

JOINs usually represent one of three relationship types.

Understanding these relationships is critical because they determine:
- how rows multiply
- how JOINs behave
- why bridge tables exist
- how databases are designed

---

# 7.1 One-to-One (1:1)

## Meaning

One row in table A matches:

```text
exactly one row
```

in table B.

And vice versa.

---

# Closest example in the Employees database

The Employees dataset does not have a perfect one-to-one table, but conceptually:

```text
employees ↔ current department assignment
```

can behave like one-to-one if:
- each employee currently belongs to only one department

---

# Example query

```sql
SELECT e.emp_no,
       d.dept_name
FROM employees e
JOIN dept_emp de
ON e.emp_no = de.emp_no
JOIN departments d
ON de.dept_no = d.dept_no
WHERE de.to_date = '9999-01-01';
```

---

# Key insight

One-to-one relationships usually:

```text
do not multiply rows
```

because one row matches only one other row.

---

# 7.2 One-to-Many (1:N)

This is the MOST common relationship type.

---

# Meaning

One row in table A can match:

```text
many rows
```

in table B.

But each row in B belongs to only one row in A.

---

# Example in Employees database

```text
employees → salaries
```

One employee:
- can have many salary records over time

Each salary row:
- belongs to only one employee

---

# JOIN example

```sql
SELECT e.emp_no,
       e.first_name,
       s.salary
FROM employees e
JOIN salaries s
ON e.emp_no = s.emp_no;
```

---

# Internal behavior

Employee row:

| emp_no | first_name |
|---|---|
| 10001 | Georgi |

Matching salary rows:

| emp_no | salary |
|---|---|
| 10001 | 60117 |
| 10001 | 62102 |
| 10001 | 66074 |

---

# Output

| emp_no | first_name | salary |
|---|---|---|
| 10001 | Georgi | 60117 |
| 10001 | Georgi | 62102 |
| 10001 | Georgi | 66074 |

---

# Important insight

One-to-many JOINs:

```text
duplicate the left-side row
```

for every matching right-side row.

This is one of the biggest sources of accidental duplicates in SQL.

---

# Another one-to-many example

```text
departments → dept_emp
```

One department:
- contains many employees

Each department assignment row:
- references one department

---

# 7.3 Many-to-Many (M:N)

## Meaning

Many rows in table A can match:

```text
many rows
```

in table B.

---

# Real example in Employees database

```text
employees ↔ departments
```

---

# Why this is many-to-many

Over time:
- one employee may work in multiple departments
- one department contains many employees

So:

```text
many employees ↔ many departments
```

---

# Problem

Relational databases cannot represent many-to-many directly with a single foreign key.

So they use a:

```text
bridge table / junction table
```

---

# In this database, the bridge table is:

```text
dept_emp
```

---

# Relationship structure

```text
employees ←→ dept_emp ←→ departments
```

---

# What each row in dept_emp means

Example:

| emp_no | dept_no |
|---|---|
| 10001 | d005 |

Meaning:

```text
employee 10001 belongs to department d005
```

---

# JOIN example

```sql
SELECT e.first_name,
       d.dept_name
FROM employees e
JOIN dept_emp de
ON e.emp_no = de.emp_no
JOIN departments d
ON de.dept_no = d.dept_no;
```

---

# Internal logic

## Step 1

```text
employees ↔ dept_emp
```

Find department assignments.

---

## Step 2

```text
dept_emp ↔ departments
```

Translate department IDs into names.


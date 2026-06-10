# UNION in PostgreSQL Using the Employees Database

`UNION` combines the results of multiple `SELECT` statements into one result set.

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

`ORDER BY` must go at the end.

---

# Example 7 — Using Labels

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


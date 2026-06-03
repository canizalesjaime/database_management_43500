# Data Types and Conditionals in PostgreSQL Queries

When reading data from a PostgreSQL database, it is important to understand:

1. **Data Types** — the kind of data stored in each column
2. **Conditionals** — how to filter and categorize data in queries

In this lesson, we will focus entirely on using `SELECT` statements to retrieve and analyze information from a database.

---

# Part 1: Understanding Data Types When Reading Data

Every column in a database table has a data type.  
The data type determines:
- what values are stored
- how the data is displayed
- what operations can be performed

---

# Example Table: employees

Assume the database already contains this table:

| employee_id | first_name | salary | full_time | hire_date |
|---|---|---|---|---|
| 1 | Alice | 65000.50 | true | 2025-01-15 |
| 2 | Bob | 82000.00 | true | 2023-07-01 |
| 3 | Carol | 42000.25 | false | 2026-03-10 |

---

## Viewing Data Types in a Table (\d command)

In PostgreSQL's interactive terminal (`psql`), you can inspect a table's structure using:

```sql
\d employees
```

This command shows:
- column names
- data types
- indexes
- constraints (like primary keys)

### Example Output (conceptual)

```
Column     | Type          | Modifiers
-----------+---------------+-----------
employee_id| integer       |
first_name | varchar(50)   |
salary     | numeric(8,2)  |
full_time  | boolean       |
hire_date  | date          |
```

---


# Integer Data Types

Integer columns store whole numbers.

Example:
- `employee_id`

## Query Example

```sql
SELECT employee_id
FROM employees;
```

Output:

| employee_id |
|---|
| 1 |
| 2 |
| 3 |

---

# Decimal Data Types

Decimal columns store numbers with fractions.

Example:
- `salary`

## Query Example

```sql
SELECT salary
FROM employees;
```

Output:

| salary |
|---|
| 65000.50 |
| 82000.00 |
| 42000.25 |

---

# Character Data Types

Text columns store words and strings.

Example:
- `first_name`

## Query Example

```sql
SELECT first_name
FROM employees;
```

Output:

| first_name |
|---|
| Alice |
| Bob |
| Carol |

---

# Boolean Data Types

Boolean columns store:
- TRUE
- FALSE

Example:
- `full_time`

## Query Example

```sql
SELECT first_name, full_time
FROM employees;
```

Output:

| first_name | full_time |
|---|---|
| Alice | true |
| Bob | true |
| Carol | false |

---

# Date and Time Data Types

PostgreSQL provides several data types for storing dates and times.

Common examples include:
- `DATE`
- `TIME`
- `TIMESTAMP`

| Data Type | Example Value |
|---|---|
| DATE | 2025-01-15 |
| TIME | 14:30:00 |
| TIMESTAMP | 2025-01-15 14:30:00 |

These data types are commonly used for:
- tracking events
- recording login times
- storing appointment schedules
- saving transaction timestamps

---

## DATE Data Type

The `DATE` type stores calendar dates.

Example column:
- `hire_date`

### Query Example

```sql
SELECT first_name, hire_date
FROM employees;
```

Output:

| first_name | hire_date |
|---|---|
| Alice | 2025-01-15 |
| Bob | 2023-07-01 |
| Carol | 2026-03-10 |

---

## TIME Data Type

The `TIME` type stores a time of day without a date.

Example column:
- `shift_start`

### Query Example

```sql
SELECT first_name, shift_start
FROM employees;
```

Output:

| first_name | shift_start |
|---|---|
| Alice | 09:00:00 |
| Bob | 08:30:00 |
| Carol | 12:00:00 |

---

## TIMESTAMP Data Type

The `TIMESTAMP` type stores both a date and a time together.

Example column:
- `last_login`

### Query Example

```sql
SELECT first_name, last_login
FROM employees;
```

Output:

| first_name | last_login |
|---|---|
| Alice | 2026-06-03 09:15:22 |
| Bob | 2026-06-02 18:40:10 |
| Carol | 2026-06-01 12:05:55 |

---

## Filtering Dates and Times

Date and time values can be filtered using conditional operators.

### Example: Filtering Dates

```sql
SELECT *
FROM employees
WHERE hire_date > '2024-01-01';
```

---

### Example: Filtering Times

```sql
SELECT *
FROM employees
WHERE shift_start < '10:00:00';
```

---

### Example: Filtering Timestamps

```sql
SELECT *
FROM employees
WHERE last_login > '2026-06-01 00:00:00';
```

# Part 2: Conditionals in Queries

Conditionals allow queries to:
- filter rows
- compare values
- classify data

---

# Filtering Text Data

## Example

```sql
SELECT *
FROM employees
WHERE first_name = 'Alice';
```

---

# Filtering Boolean Data

## Example

```sql
SELECT *
FROM employees
WHERE full_time = true;
```

Output:

| first_name |
|---|
| Alice |
| Bob |

---

# Filtering Dates

## Example

```sql
SELECT *
FROM employees
WHERE hire_date > '2024-01-01';
```

---

# Using AND

`AND` requires both conditions to be true.

## Example

```sql
SELECT *
FROM employees
WHERE salary > 50000
AND full_time = true;
```

---

# Using OR

`OR` requires at least one condition to be true.

## Example

```sql
SELECT *
FROM employees
WHERE salary > 80000
OR full_time = false;
```

---

# Using NOT

`NOT` reverses a condition.

## Example

```sql
SELECT *
FROM employees
WHERE NOT full_time;
```

Equivalent to:

```sql
SELECT *
FROM employees
WHERE full_time = false;
```

---

# The CASE Statement

`CASE` adds conditional logic to query results.

It works similarly to:
- if
- else if
- else

in programming languages.

---

# Example: Salary Categories

```sql
SELECT
    first_name,
    salary,
    CASE
        WHEN salary >= 80000 THEN 'High Salary'
        WHEN salary >= 50000 THEN 'Medium Salary'
        ELSE 'Low Salary'
    END AS salary_level
FROM employees;
```

Output:

| first_name | salary | salary_level |
|---|---|---|
| Alice | 65000.50 | Medium Salary |
| Bob | 82000.00 | High Salary |
| Carol | 42000.25 | Low Salary |

---

# Using CASE with Boolean Data

```sql
SELECT
    first_name,
    CASE
        WHEN full_time = true THEN 'Full-Time Employee'
        ELSE 'Part-Time Employee'
    END AS employment_type
FROM employees;
```

---

# Handling NULL Values

`NULL` means missing or unknown data.

## Finding NULL Values

```sql
SELECT *
FROM employees
WHERE hire_date IS NULL;
```

---

# Finding Non-NULL Values

```sql
SELECT *
FROM employees
WHERE hire_date IS NOT NULL;
```

---

# Combining Multiple Conditions

## Example

```sql
SELECT *
FROM employees
WHERE salary > 50000
AND hire_date > '2024-01-01'
AND full_time = true;
```

---

# Practice Exercises

## Exercise 1

Write a query that returns:
- all employees with salary greater than 70000

---

## Exercise 2

Write a query that returns:
- employees who only worked at the compnay between 1990 and 2000

---

## Exercise 3

Use a `CASE` statement to classify employees as:
- Senior
- Junior

based on salary.

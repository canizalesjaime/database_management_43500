# Intro grouping

We focus only on SQL read/query operations involving in this lecture:

- `IN`
- `DISTINCT`
- `GROUP BY`
- `HAVING`
- `ORDER BY`

---

# 1. `IN` — Matching Multiple Values

The `IN` operator is used inside a `WHERE` clause to match a column against multiple possible values.

Instead of writing many `OR` conditions, `IN` provides cleaner and more readable SQL.

---

# Basic Syntax

```sql
WHERE column_name IN (value1, value2, value3)
```

---

# Example: Find Employees Named Georgi or Parto

```sql
SELECT emp_no, first_name, last_name
FROM employees
WHERE first_name IN ('Georgi', 'Parto');
```

This query returns all employees whose first name is:
- Georgi
- Parto

Equivalent query using `OR`:

```sql
SELECT emp_no, first_name, last_name
FROM employees
WHERE first_name = 'Georgi'
   OR first_name = 'Parto';
```

Using `IN` becomes much more useful when the list grows larger.

---

# Example: Filter Multiple Departments

```sql
SELECT emp_no, dept_no
FROM dept_emp
WHERE dept_no IN ('d001', 'd002', 'd003');
```

This returns employees assigned to:
- Marketing (`d001`)
- Finance (`d002`)
- Human Resources (`d003`)

---

# Important Notes About `IN`

`IN` works with:
- strings
- numbers
- dates

Example with employee numbers:

```sql
SELECT emp_no, first_name
FROM employees
WHERE emp_no IN (10001, 10005, 10010);
```

---

# Why `IN` Improves Readability

Compare:

```sql
WHERE dept_no = 'd001'
   OR dept_no = 'd002'
   OR dept_no = 'd003'
```

vs.

```sql
WHERE dept_no IN ('d001', 'd002', 'd003')
```

The second query is shorter and easier to maintain.

---

# 2. `DISTINCT` — Removing Duplicate Results

`DISTINCT` removes duplicate rows from the result set.

This is useful because many employees may share:
- the same first name
- the same last name
- the same department
- the same title

---

# Why DISTINCT Matters

Without `DISTINCT`, SQL returns every matching row.

Example:

```sql
SELECT first_name
FROM employees;
```

Possible output:

```text
Georgi
Parto
Georgi
Bezalel
Georgi
```

Duplicate names appear many times.

---

# Using DISTINCT

```sql
SELECT DISTINCT first_name
FROM employees
ORDER BY first_name;
```

Now each first name appears only once.

---

# Example: Unique Department Numbers

```sql
SELECT DISTINCT dept_no
FROM dept_emp;
```

Possible output:

```text
d001
d002
d003
d004
...
```

---

# DISTINCT with Multiple Columns

`DISTINCT` applies to the entire selected row combination.

Example:

```sql
SELECT DISTINCT first_name, gender
FROM employees;
```

This removes duplicate combinations of:
- first name
- gender

---

# Important Difference

These queries are different:

## Query A

```sql
SELECT DISTINCT first_name
FROM employees;
```

Returns unique names only.

---

## Query B

```sql
SELECT DISTINCT first_name, last_name
FROM employees;
```

Returns unique full-name combinations.

---

# DISTINCT with Aggregate Functions

`DISTINCT` is commonly used inside aggregate functions, especially `COUNT()`.

This allows PostgreSQL to count only unique values instead of counting every row.

---

# COUNT(*) vs COUNT(column)

| Function | Meaning |
|---|---|
| `COUNT(*)` | counts all rows |
| `COUNT(column)` | counts non-NULL values |

---

# Example: Count All Employees

```sql
SELECT COUNT(*)
FROM employees;
```

Returns the total number of employee rows.

---

# COUNT(DISTINCT column)

```sql
SELECT COUNT(DISTINCT first_name)
FROM employees;
```

This counts how many unique first names exist in the table.

---

# Example Explanation

Suppose the table contains:

```text
Georgi
Georgi
Parto
Bezalel
Parto
```

Regular count:

```sql
COUNT(first_name)
```

Result:

```text
5
```

Distinct count:

```sql
COUNT(DISTINCT first_name)
```

Result:

```text
3
```

because only these unique names exist:
- Georgi
- Parto
- Bezalel

---

# Example: Count Unique Departments

```sql
SELECT COUNT(DISTINCT dept_no)
FROM dept_emp;
```

This counts only unique department IDs.

---

# Comparing COUNT and DISTINCT COUNT

## Count Total Department Assignments

```sql
SELECT COUNT(dept_no)
FROM dept_emp;
```

Counts every department assignment row.

---

## Count Unique Departments

```sql
SELECT COUNT(DISTINCT dept_no)
FROM dept_emp;
```

Possible result:

```text
9
```

because the company has 9 departments.

---


# Important Concept

```sql
COUNT(emp_no)
```

counts all rows.

But:

```sql
COUNT(DISTINCT emp_no)
```

removes duplicates first, then counts.

---

# 3. `GROUP BY` — Grouping Rows for Aggregation

`GROUP BY` organizes rows into groups so aggregate functions can operate on each group.

Common aggregate functions:

| Function | Purpose |
|---|---|
| `COUNT()` | counts rows |
| `AVG()` | average value |
| `MIN()` | minimum value |
| `MAX()` | maximum value |

---

# How GROUP BY Works

Suppose many employees share the same gender.

`GROUP BY gender` creates:
- one group for `M`
- one group for `F`

Then aggregate functions calculate values for each group.

---

# Example: Count Employees by Gender

```sql
SELECT gender, COUNT(*)
FROM employees
GROUP BY gender;
```

Possible output:

```text
 gender | count
--------+--------
 M      | 179973
 F      | 120051
```

---

# Understanding the Query

```sql
SELECT gender, COUNT(*)
```

We want:
- the gender
- the number of rows in that gender group

---

```sql
GROUP BY gender;
```

Tells PostgreSQL:
> “Create one group for each gender.”

---

# Important GROUP BY Rule

Every selected column must either:
1. appear in `GROUP BY`
2. or be used inside an aggregate function

---

# Correct Example

```sql
SELECT gender, COUNT(*)
FROM employees
GROUP BY gender;
```

---

# Incorrect Example

```sql
SELECT first_name, gender, COUNT(*)
FROM employees
GROUP BY gender;
```

This causes an error because:
- `first_name` is neither grouped nor aggregated.

---

# Example: Count Employees Per Department

```sql
SELECT dept_no, COUNT(*) AS total_employees
FROM dept_emp
GROUP BY dept_no
ORDER BY dept_no;
```

---

# Example: Most Common First Names

```sql
SELECT first_name, COUNT(*) AS occurrences
FROM employees
GROUP BY first_name
ORDER BY occurrences DESC;
```

This:
1. groups employees by first name
2. counts rows in each group
3. sorts from most common to least common

---

# 4. `HAVING` — Filtering Groups

`HAVING` filters grouped data after `GROUP BY` is complete.

---

# WHERE vs HAVING

| Clause | Operates On |
|---|---|
| `WHERE` | individual rows |
| `HAVING` | grouped rows |

---

# SQL Processing Order

SQL logically processes queries in this order:

1. `FROM`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`

Because `HAVING` happens after grouping, it can use aggregate functions like:
- `COUNT()`
- `AVG()`
- `MAX()`

`WHERE` cannot.

---

# Example: First Names Appearing More Than 250 Times

```sql
SELECT first_name, COUNT(*) AS total
FROM employees
GROUP BY first_name
HAVING COUNT(*) > 250
ORDER BY total DESC;
```

---

# Step-by-Step Interpretation

## Step 1 — Group Rows

```sql
GROUP BY first_name
```

Create one group for each unique first name.

---

## Step 2 — Count Rows

```sql
COUNT(*)
```

Count employees in each group.

---

## Step 3 — Filter Groups

```sql
HAVING COUNT(*) > 250
```

Keep only groups larger than 250 employees.

---

# Example: Departments with Large Employee Counts

```sql
SELECT dept_no, COUNT(*) AS total
FROM dept_emp
GROUP BY dept_no
HAVING COUNT(*) > 40000;
```

Only departments with more than 40,000 employee assignments are shown.

---

# 5. `ORDER BY` — Sorting Results

`ORDER BY` sorts query results.

Without it, PostgreSQL does not guarantee row order.

---

# Sorting Directions

| Keyword | Meaning |
|---|---|
| `ASC` | ascending |
| `DESC` | descending |

Default:

```sql
ORDER BY column_name
```

means ascending order.

---

# Example: Sort Employees by Hire Date

```sql
SELECT emp_no, first_name, hire_date
FROM employees
ORDER BY hire_date;
```

Oldest hires appear first.

---

# Descending Order

```sql
SELECT emp_no, first_name, hire_date
FROM employees
ORDER BY hire_date DESC;
```

Newest hires appear first.

---

# Sorting by Multiple Columns

SQL sorts left-to-right.

---

# Example

```sql
SELECT emp_no, first_name, last_name
FROM employees
ORDER BY last_name ASC, first_name ASC;
```

SQL:
1. sorts by last name
2. if last names match, sorts by first name

---

# Example: Sorting Aggregated Results

```sql
SELECT first_name, COUNT(*) AS total
FROM employees
GROUP BY first_name
ORDER BY total DESC;
```

This is very common in analytics queries.

---

# Complete Example Combining Everything

```sql
SELECT dept_no,
       COUNT(DISTINCT emp_no) AS total_employees
FROM dept_emp
WHERE dept_no IN ('d001', 'd002', 'd003')
GROUP BY dept_no
HAVING COUNT(DISTINCT emp_no) > 30000
ORDER BY total_employees DESC;
```

---

# How PostgreSQL Processes This Query

## Step 1 — WHERE

```sql
WHERE dept_no IN ('d001', 'd002', 'd003')
```

Keep only rows for those departments.

---

## Step 2 — GROUP BY

```sql
GROUP BY dept_no
```

Create groups by department.

---

## Step 3 — DISTINCT Inside COUNT

```sql
COUNT(DISTINCT emp_no)
```

Remove duplicate employee numbers inside each group.

---

## Step 4 — HAVING

```sql
HAVING COUNT(DISTINCT emp_no) > 30000
```

Remove smaller department groups.

---

## Step 5 — ORDER BY

```sql
ORDER BY total_employees DESC
```

Sort largest departments first.
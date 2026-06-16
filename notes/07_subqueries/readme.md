# SQL SUBQUERIES
A subquery is:

```text
a query inside another query
```

Example:

```sql
SELECT *
FROM salaries
WHERE salary > (
    SELECT AVG(salary)
    FROM salaries
);
```

The inner query runs first.

---
Consider the problem, ```show all employees who make more than the average salary?```
without subqueries, we would: 
```sql
    SELECT AVG(salary)
    FROM salaries;
``` 
Write down the result(63810), then:

```sql
SELECT *
FROM salaries
WHERE salary > 63810;
```
This is inefficient because you have to manually write down the result, and the second query is dependent on the first, so if the table updates, your second query may become invalid. Subqueries solve this problem. 

# 1. Scalar subqueries

A scalar subquery returns:

```text
exactly one value
```

Example:

```sql
SELECT emp_no,
       salary
FROM salaries
WHERE salary > (
    SELECT AVG(salary)
    FROM salaries
);
```

---

# Step-by-step execution

## Step 1

Inner query runs:

```sql
SELECT AVG(salary)
FROM salaries;
```

Suppose result:

```text
63810
```

---

## Step 2

Outer query becomes conceptually:

```sql
SELECT emp_no,
       salary
FROM salaries
WHERE salary > 63810;
```

---


# 2. Subqueries in SELECT

Subqueries can appear inside SELECT columns.

Example:

```sql
SELECT emp_no,
       salary,
       (
           SELECT AVG(salary)
           FROM salaries
       ) AS average_salary
FROM salaries;
```

---

# Result idea

| emp_no | salary | average_salary |
|--------|--------|----------------|
| 10001  | 70000  | 63810 |
| 10002  | 80000  | 63810 |


The subquery becomes:

```text
a computed column
```

---

# 3. Correlated subqueries

A correlated subquery depends on the outer query.

This is VERY important.

---

# Example

Find employees earning above THEIR OWN average salary history.

```sql
SELECT s1.emp_no,
       s1.salary
FROM salaries s1
WHERE s1.salary > (
    SELECT AVG(s2.salary)
    FROM salaries s2
    WHERE s2.emp_no = s1.emp_no
);
```

---

# Why this is correlated

Inner query references:

```sql
s1.emp_no
```

from outer query.

So the subquery changes for EACH row.

---

# Execution idea

For each salary row:
- calculate employee's average salary
- compare current salary to that average

Correlated subqueries act like:

```text
row-by-row mini queries
```

**Another Example:**
```sql
SELECT
emp_no, first_name, last_name,
(SELECT MAX(salary) FROM salaries WHERE employees.emp_no = salaries.emp_no) AS max_salary
FROM employees;
```

This query computes the max salary for each employees in the subquery.
---

# 4. EXISTS subqueries

EXISTS checks whether rows exist.

Returns:
- TRUE
- FALSE

---

# Example

Find employees that have salary records.

```sql
SELECT e.emp_no,
       e.first_name
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM salaries s
    WHERE s.emp_no = e.emp_no
);
```

PostgreSQL only cares whether:

```text
at least one row exists
```

The actual value `1` is irrelevant.

```text
"Does this employee have matching salary rows?"
```

---

# 5. IN subqueries

IN compares against a list.

---

# Example

```sql
SELECT emp_no,
       first_name
FROM employees
WHERE emp_no IN (
    SELECT emp_no
    FROM salaries
    WHERE salary > 100000
);
```

---

# Execution idea

## Step 1

Inner query returns:

```text
{10002, 10005, 10010}
```

---

## Step 2

Outer query checks:

```text
is emp_no inside this set?
```

---

# Key insight

IN subqueries behave like:

```text
membership tests
```

---

# 6. FROM subqueries (derived tables)

A subquery can act like a temporary table.

---

# Example

```sql
SELECT avg_table.emp_no,
       avg_table.avg_salary
FROM (
    SELECT emp_no,
           AVG(salary) AS avg_salary
    FROM salaries
    GROUP BY emp_no
) AS avg_table;
```

---

# Key insight

The inner query creates:

```text
temporary virtual table
```

called:

```text
avg_table
```

---

# Why this is useful

Lets you:
- break complex queries into stages
- aggregate first
- filter later
- simplify logic

---

# 7. CTEs (Common Table Expressions)

CTEs are named temporary query blocks.

Syntax:

```sql
WITH cte_name AS (
    query
)
SELECT *
FROM cte_name;
```

---

# Why CTEs exist

CTEs improve:
- readability
- organization
- debugging
- multi-stage transformations

---

# Basic CTE example

```sql
WITH average_salaries AS (
    SELECT emp_no,
           AVG(salary) AS avg_salary
    FROM salaries
    GROUP BY emp_no
)
SELECT *
FROM average_salaries;
```

---

# Mental model

CTE =

```text
temporary named result set
```

---

# Comparing FROM subquery vs CTE

---

# FROM subquery

```sql
SELECT *
FROM (
    SELECT emp_no,
           AVG(salary) AS avg_salary
    FROM salaries
    GROUP BY emp_no
) avg_table;
```

---

# Same thing as CTE

```sql
WITH avg_table AS (
    SELECT emp_no,
           AVG(salary) AS avg_salary
    FROM salaries
    GROUP BY emp_no
)
SELECT *
FROM avg_table;
```

---

# Why CTEs are preferred

Because deeply nested subqueries become unreadable.

CTEs flatten query structure.

---

# 8. Multi-CTE pipelines

You can chain multiple CTEs together.

---

# Example

```sql
WITH avg_salary AS (
    SELECT emp_no,
           AVG(salary) AS avg_salary
    FROM salaries
    GROUP BY emp_no
),

high_earners AS (
    SELECT emp_no,
           avg_salary
    FROM avg_salary
    WHERE avg_salary > 80000
)

SELECT *
FROM high_earners;
```

---

# Execution flow

## Step 1

Create:

```text
avg_salary
```

---

## Step 2

Use it to create:

```text
high_earners
```

---

## Step 3

Final SELECT reads from high_earners.


CTEs create:

```text
step-by-step query pipelines
```

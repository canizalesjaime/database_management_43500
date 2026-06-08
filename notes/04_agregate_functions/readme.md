# Aggregate Functions in PostgreSQL

Aggregate functions take many rows and return one result.

For example:
- adding salaries together
- finding the average salary
- finding the highest salary
- counting employees

Using the classic employees database (Georgi Facello, Bezalel Spertus, etc.).

---

# Main Aggregate Functions

| Function | Purpose |
|---|---|
| `SUM()` | Adds values |
| `AVG()` | Finds average |
| `MIN()` | Finds smallest value |
| `MAX()` | Finds largest value |
| `COUNT()` | Counts rows |

---

# 1. COUNT()

Counts rows.

## Count all employees

```sql
SELECT COUNT(*)
FROM employees;
```

### What happens
- PostgreSQL looks at every row in `employees`
- Counts them
- Returns one number

---

## Count employees with a first name

```sql
SELECT COUNT(first_name)
FROM employees;
```

### Difference from `COUNT(*)`
- `COUNT(*)` counts all rows
- `COUNT(column)` counts only non-NULL values

Since `first_name` is never NULL in this database, both are usually the same.

---

# 2. SUM()

Adds numeric values together.

## Total of all salaries

```sql
SELECT SUM(salary)
FROM salaries;
```

### What happens
PostgreSQL adds every salary value together.

Example idea:

```text
50000 + 60000 + 70000 + ...
```

Result:
- one total number

---

# 3. AVG()

Finds the average.

## Average salary

```sql
SELECT AVG(salary)
FROM salaries;
```

### Internally

PostgreSQL essentially does:

```text
SUM(salary) / COUNT(salary)
```

---

# 4. MIN()

Finds the smallest value.

## Lowest salary

```sql
SELECT MIN(salary)
FROM salaries;
```

PostgreSQL checks all salaries and keeps the smallest one found.

---

# 5. MAX()

Finds the largest value.

## Highest salary

```sql
SELECT MAX(salary)
FROM salaries;
```

PostgreSQL checks all salaries and keeps the largest value found.

---

# Aggregate Functions with WHERE

Usually you combine aggregates with filtering.

---

## Count female employees

```sql
SELECT COUNT(*)
FROM employees
WHERE gender = 'F';
```

### Flow
1. Look through employees
2. Keep only females
3. Count remaining rows

---

## Find the highest salary over 100000

```sql
SELECT MAX(salary)
FROM salaries
WHERE salary > 100000;
```

---

## Find the average salary over 70000

```sql
SELECT AVG(salary)
FROM salaries
WHERE salary > 70000;
```

---

## Count employees born before 1960

```sql
SELECT COUNT(*)
FROM employees
WHERE birth_date < '1960-01-01';
```

---

# Aggregate Functions with CASE

Now we combine aggregates with `CASE`.

This is called conditional aggregation.

---

# What CASE Does

`CASE` works like an if-statement.

Example:

```sql
CASE
    WHEN gender = 'M' THEN 1
    ELSE 0
END
```

Meaning:
- if employee is male → return 1
- otherwise → return 0

---

# SUM with CASE

## Count males using SUM

```sql
SELECT
    SUM(
        CASE
            WHEN gender = 'M'
            THEN 1
            ELSE 0
        END
    ) AS male_count
FROM employees;
```

### How it works

For each row:

```text
Male   -> 1
Female -> 0
```

Then `SUM()` adds them:

```text
1 + 1 + 0 + 1 + 0 ...
```

---

# COUNT with CASE

## Count males and females separately

```sql
SELECT
    COUNT(
        CASE
            WHEN gender = 'M'
            THEN 1
        END
    ) AS males,

    COUNT(
        CASE
            WHEN gender = 'F'
            THEN 1
        END
    ) AS females

FROM employees;
```

### Why this works

`COUNT()` counts non-NULL values.

So:

```text
Male row   -> 1
Female row -> NULL
```

Only the `1`s get counted.

---

# AVG with CASE

## Average salary above and below 80000

```sql
SELECT
    AVG(
        CASE
            WHEN salary >= 80000
            THEN salary
        END
    ) AS high_salary_avg,

    AVG(
        CASE
            WHEN salary < 80000
            THEN salary
        END
    ) AS low_salary_avg

FROM salaries;
```

### Important
No `ELSE` means:
- unmatched rows become `NULL`
- `AVG()` ignores NULL values

---

# MAX with CASE

## Highest salary in two ranges

```sql
SELECT
    MAX(
        CASE
            WHEN salary >= 100000
            THEN salary
        END
    ) AS high_range_max,

    MAX(
        CASE
            WHEN salary < 100000
            THEN salary
        END
    ) AS low_range_max

FROM salaries;
```

---

# MIN with CASE

## Lowest salary in two ranges

```sql
SELECT
    MIN(
        CASE
            WHEN salary >= 100000
            THEN salary
        END
    ) AS high_range_min,

    MIN(
        CASE
            WHEN salary < 100000
            THEN salary
        END
    ) AS low_range_min

FROM salaries;
```

---

# Why CASE Aggregates Are Important

This pattern is extremely common:

```sql
SUM(CASE WHEN condition THEN value ELSE 0 END)
```

Used for:
- dashboards
- analytics
- reports
- business intelligence
- grouped statistics


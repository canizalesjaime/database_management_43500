# PostgreSQL Functions and Expressions

PostgreSQL includes many built-in functions and operators that allow queries to:
- manipulate text
- perform calculations
- work with dates and times
- generate temporary values
- transform data

These functions are commonly used inside `SELECT` statements when reading data from a database.

Assume the database contains an `employees` table with columns such as:
- `first_name`
- `last_name`
- `salary`
- `hire_date`
- `email`

---

# Temporary Columns with Literals

A query can create temporary columns using literal values.

These values:
- are displayed in query results
- are not permanently stored
- can be combined with existing columns

---

## Numeric Literal Example

```sql
SELECT
    first_name,
    1 AS department_number
FROM employees;
```

---

## String Literal Example

```sql
SELECT
    first_name,
    'Employee' AS role
FROM employees;
```

---

## Multiple Temporary Columns

```sql
SELECT
    first_name,
    1 AS building_number,
    'Full-Time Staff' AS employee_type
FROM employees;
```

---

# UPPER Function

`UPPER()` converts text to uppercase letters.

## Example

```sql
SELECT
    first_name,
    UPPER(first_name) AS uppercase_name
FROM employees;
```

---

# LOWER Function

`LOWER()` converts text to lowercase letters.

## Example

```sql
SELECT
    first_name,
    LOWER(first_name) AS lowercase_name
FROM employees;
```

---

# Operators

Operators perform mathematical calculations.

| Operator | Purpose |
|---|---|
| + | Addition |
| - | Subtraction |
| * | Multiplication |
| / | Division |
| % | Modulus |

---

## Arithmetic Example

```sql
SELECT
    first_name,
    salary,
    salary + 1000 AS increased_salary,
    salary - 500 AS reduced_salary
FROM employees;
```

---

# SQRT Function

`SQRT()` calculates the square root of a number.

## Example

```sql
SELECT
    first_name,
    salary,
    SQRT(salary) AS salary_square_root
FROM employees;
```

---

# ROUND Function

`ROUND()` rounds decimal numbers to a specified number of decimal places.

This is useful when:
- displaying cleaner numeric output
- formatting currency values
- reducing long decimal values
- simplifying calculations

---

# Basic ROUND Example

When `ROUND()` is used with only one argument, PostgreSQL rounds the number to the nearest whole number.

## Example

```sql
SELECT
    first_name,
    salary,
    ROUND(salary) AS rounded_salary
FROM employees;
```

Example Output:

| first_name | salary | rounded_salary |
|---|---|---|
| Alice | 65000.50 | 65001 |
| Bob | 82000.25 | 82000 |
| Carol | 42000.75 | 42001 |

---

# Understanding Decimal Places

Decimal places refer to the digits to the right of the decimal point.

Example number:

``` id="ryjlwm"
123.4567
```

| Decimal Place | Value |
|---|---|
| 1st decimal place | 4 |
| 2nd decimal place | 5 |
| 3rd decimal place | 6 |
| 4th decimal place | 7 |

---

# Rounding to 1 Decimal Place

Using `ROUND(number, 1)` keeps one digit after the decimal point.

## Example

```sql
SELECT
    first_name,
    salary,
    ROUND(salary, 1) AS rounded_salary
FROM employees;
```

Example Output:

| first_name | salary | rounded_salary |
|---|---|---|
| Alice | 65000.56 | 65000.6 |
| Bob | 82000.24 | 82000.2 |
| Carol | 42000.78 | 42000.8 |

---

# Rounding to 2 Decimal Places

Using `ROUND(number, 2)` keeps two digits after the decimal point.

This is common for:
- currency
- financial data
- prices

## Example

```sql
SELECT
    first_name,
    salary,
    ROUND(salary, 2) AS rounded_salary
FROM employees;
```

Example Output:

| first_name | salary | rounded_salary |
|---|---|---|
| Alice | 65000.567 | 65000.57 |
| Bob | 82000.234 | 82000.23 |
| Carol | 42000.789 | 42000.79 |

---

# Practical Example

```sql
SELECT
    first_name,
    salary,
    ROUND(salary) AS nearest_whole,
    ROUND(salary, 1) AS one_decimal_place,
    ROUND(salary, 2) AS two_decimal_places
FROM employees;
```

This query demonstrates how the same number can be rounded differently depending on the number of decimal places requested.
---

# RANDOM Function

`RANDOM()` generates a pseudo-random decimal value between **0 and 1**.

This means every result will be:
- greater than or equal to 0
- less than 1

Example output values:
- 0.1234
- 0.9876
- 0.5021

Each row gets a different random number.

---

# Basic Example

```sql
SELECT
    first_name,
    RANDOM() AS random_value
FROM employees;
```

---

# Understanding the 0 to 1 Range

The output of `RANDOM()` is always in this range:

```
0.0 ≤ RANDOM() < 1.0
```

Think of it like a percentage scale:
- 0.0 = 0%
- 0.5 = 50%
- 1.0 = 100% (never actually reached)

---

# Scaling RANDOM() to Different Ranges

On its own, `RANDOM()` is not very useful for real-world data because most values are small decimals.

We usually scale it to create useful ranges.

---

# Random Numbers from 1 to 10

To generate values between **1 and 10**, we multiply by 10 and shift the range.

## Formula

```sql
FLOOR(RANDOM() * 10) + 1
```

## Example

```sql
SELECT
    first_name,
    FLOOR(RANDOM() * 10) + 1 AS random_1_to_10
FROM employees;
```

## Explanation

| Step | Meaning |
|---|---|
| `RANDOM()` | gives 0 to 1 |
| `* 10` | changes range to 0 to 10 |
| `FLOOR()` | removes decimals (0–9) |
| `+ 1` | shifts range to 1–10 |

---

# Random Numbers from 1 to 100

## Formula

```sql
FLOOR(RANDOM() * 100) + 1
```

## Example

```sql
SELECT
    first_name,
    FLOOR(RANDOM() * 100) + 1 AS random_1_to_100
FROM employees;
```

## Result Range

- Minimum: 1
- Maximum: 100

---

# Random Decimal Range (No Rounding)

If you want decimals within a range, you do NOT use `FLOOR()`.

## Example: 0 to 50 (decimal values allowed)

```sql
SELECT
    first_name,
    RANDOM() * 50 AS random_0_to_50
FROM employees;
```

---

# Random Numbers Between Any Two Values

To generate a range between **min and max**, use this formula:

## Formula

```sql
FLOOR(RANDOM() * (max - min + 1)) + min
```

---

## Example: 20 to 30

```sql
SELECT
    first_name,
    FLOOR(RANDOM() * (30 - 20 + 1)) + 20 AS random_20_to_30
FROM employees;
```

## Breakdown

| Part | Meaning |
|---|---|
| `30 - 20 + 1` | size of range (11 numbers) |
| `RANDOM() * 11` | produces 0–10.999... |
| `FLOOR()` | converts to 0–10 |
| `+ 20` | shifts range to 20–30 |

---

# Random Salary Simulation Example

You can use `RANDOM()` to simulate data changes.

## Example: 0% to 20% bonus

```sql
SELECT
    first_name,
    salary,
    salary * (1 + RANDOM() * 0.20) AS salary_with_bonus
FROM employees;
```

---

# Concatenation

Concatenation joins strings together using the `||` operator.

## Example

```sql
SELECT
    first_name || ' ' || last_name AS full_name
FROM employees;
```

---

## Concatenating Text with Literals

```sql
SELECT
    first_name || ' works here' AS employee_message
FROM employees;
```

---

# SUBSTR Function

`SUBSTR()` extracts part of a string.

## Syntax

```sql
SUBSTR(string, start, length)
```

---

## Example

```sql
SELECT
    first_name,
    SUBSTR(first_name, 1, 3) AS first_three_letters
FROM employees;
```

---

# SPLIT_PART Function

`SPLIT_PART()` separates text using a delimiter.

This is commonly used with emails or formatted strings.

## Example

```sql
SELECT
    email,
    SPLIT_PART(email, '@', 1) AS username
FROM employees;
```

---

## Extracting Email Domains

```sql
SELECT
    email,
    SPLIT_PART(email, '@', 2) AS domain
FROM employees;
```

---

# EXTRACT Function

`EXTRACT()` retrieves parts of dates or timestamps.

Examples include:
- year
- month
- day

---

## Extracting Year

```sql
SELECT
    first_name,
    hire_date,
    EXTRACT(YEAR FROM hire_date) AS hire_year
FROM employees;
```

---

## Extracting Month

```sql
SELECT
    first_name,
    hire_date,
    EXTRACT(MONTH FROM hire_date) AS hire_month
FROM employees;
```

---

# AGE Function

`AGE()` calculates the difference between dates.

## Example

```sql
SELECT
    first_name,
    to_date,
    from_date,
    AGE(to_date, from_date) AS time_worked
FROM titles;
```

---

# Casting

Casting converts one data type into another.

PostgreSQL supports:
- `CAST()`
- `::`

---

## CAST Example

```sql
SELECT
    first_name,
    CAST(salary AS INTEGER) AS integer_salary
FROM employees;
```

---

## Double-Colon Casting

```sql
SELECT
    first_name,
    salary::INTEGER AS integer_salary
FROM employees;
```

---

# NOW Function

`NOW()` returns the current date and time.

## Example

```sql
SELECT
    first_name,
    NOW() AS current_time
FROM employees;
```

---

# Combining Functions

Functions can be combined together in a single query.

## Example

```sql
SELECT
    first_name,
    UPPER(SUBSTR(first_name, 1, 3)) AS formatted_name
FROM employees;
```

---

# Practical Example

```sql
SELECT
    first_name,
    last_name,
    UPPER(first_name) AS uppercase_name,
    LENGTH(first_name) AS name_length,
    ROUND(salary) AS rounded_salary,
    EXTRACT(YEAR FROM hire_date) AS hire_year
FROM employees;
```

---

# Practice Exercises

## Exercise 1

Write a query that:
- converts employee names to uppercase

---

## Exercise 2

Write a query that:
- calculates the square root of employee salaries

---

## Exercise 3

Write a query that:
- extracts the first 3 letters of employee names

---

## Exercise 4

Write a query that:
- combines first and last names into a single column

---

## Exercise 5

Write a query that:
- extracts the hire year from `hire_date`

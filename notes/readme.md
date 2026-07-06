## Learning Path

relational algebra/calculus, writing your own dbs(sql compiler(frontend) and a database execution and storage engine (backend))

1. learn relational algebra/calculus
2. Build a SQL lexer
3. Build a SQL parser that creates an AST
4. Convert AST to relational algebra
5. Implement a few simple optimization rules on the relational algebra tree
6. Build an execution engine that evaluates the optimized plan against in-memory tables.
7. Finally, add persistence, indexes, transactions, and other database features.


# Introduction to Relational Algebra
### Database Systems Learning Path – Phase 1 (Python)
**Course Goal:** Learn the mathematical foundation of SQL and relational databases.

---

# Learning Objectives

By the end of this lecture, you should be able to:

- Explain what relational algebra is.
- Understand why every database engineer should know it.
- Understand relations, tuples, and attributes.
- Perform the six fundamental relational algebra operations.
- Translate simple SQL queries into relational algebra.
- See how relational algebra becomes the internal language of an SQL compiler.

---

# 1. Motivation

When you write SQL like

```sql
SELECT name
FROM Student
WHERE major = 'CS';
```

the database **does not execute SQL directly**.

Instead, it performs something like

```
SQL
 ↓
Parser
 ↓
Relational Algebra
 ↓
Query Optimizer
 ↓
Execution Plan
 ↓
Database Engine
```

Relational algebra is the mathematical language used to describe **what data should be produced**.

It is **not** concerned with how data is physically stored.

Relational algebra is essentially the **intermediate representation (IR)** for SQL.

---

# 2. What is a Relation?

A relation is simply a table.

Example:

Student

| SID | Name | Major |
|-----|------|-------|
|1|Alice|CS|
|2|Bob|Math|
|3|Charlie|CS|

Mathematically,

```
Relation = Set of Tuples
```

where

- relation = table
- tuple = row
- attribute = column

Example:

Tuple

```
(1, Alice, CS)
```

Attribute names

```
SID
Name
Major
```

---

# 3. Why is it called "Relational"?

Because data is represented as **relations between values**, not because it is "related" in the everyday sense.

For example

Student

| SID | Name |
|----|------|
|1|Alice|
|2|Bob|

Course

| CID | Title |
|----|------|
|10|Databases|
|20|AI|

Enrollment

| SID | CID |
|----|----|
|1|10|
|1|20|
|2|20|

Enrollment represents the relationship

```
Student
     ↕
Course
```

---

# 4. Closure Property

One of the most important ideas.

Every relational algebra operation

takes relations

↓

returns another relation.

Example

```
Student
        ↓ Selection
New Relation
        ↓ Projection
Another Relation
        ↓ Join
Another Relation
```

This allows operations to be chained together.

---

# 5. The Six Fundamental Operators

These six operations are enough to express nearly every SQL query.

---

## Operator 1: Selection (σ)

Selection filters rows.

Notation

```
σ(condition)(Relation)
```

Example

Student

|SID|Name|Major|
|---|----|-----|
|1|Alice|CS|
|2|Bob|Math|
|3|Charlie|CS|

Operation

```
σ(Major='CS')(Student)
```

Result

|SID|Name|Major|
|---|----|-----|
|1|Alice|CS|
|3|Charlie|CS|

Equivalent SQL

```sql
SELECT *
FROM Student
WHERE Major='CS';
```

Think of it as

> Select rows.

---

## Operator 2: Projection (π)

Projection chooses columns.

Notation

```
π(columns)(Relation)
```

Example

```
π(Name)(Student)
```

Result

|Name|
|----|
|Alice|
|Bob|
|Charlie|

Equivalent SQL

```sql
SELECT Name
FROM Student;
```

Think

> Pick columns.

---

## Operator 3: Union (∪)

Combines two compatible relations.

Example

CSStudents

|Name|
|----|
|Alice|

MathStudents

|Name|
|----|
|Bob|

Operation

```
CSStudents
      ∪
MathStudents
```

Result

|Name|
|----|
|Alice|
|Bob|

Equivalent SQL

```sql
SELECT ...
UNION
SELECT ...
```

---

## Operator 4: Difference (−)

Subtract one relation from another.

Example

AllStudents

|Name|
|----|
|Alice|
|Bob|
|Charlie|

CSStudents

|Name|
|----|
|Alice|
|Charlie|

Operation

```
AllStudents
      −
CSStudents
```

Result

|Name|
|----|
|Bob|

Equivalent SQL

```sql
EXCEPT
```

---

## Operator 5: Cartesian Product (×)

Produces every possible pair.

Example

Students

|Name|
|----|
|Alice|
|Bob|

Courses

|Course|
|------|
|DB|
|AI|

Operation

```
Students × Courses
```

Result

|Name|Course|
|----|------|
|Alice|DB|
|Alice|AI|
|Bob|DB|
|Bob|AI|

If there are

```
m students
n courses
```

the result has

```
m × n
```

rows.

Cartesian products are usually intermediate steps before joins.

---

## Operator 6: Rename (ρ)

Changes table or attribute names.

Notation

```
ρ(NewName)(Relation)
```

Example

```
ρ(S)(Student)
```

Now we can write

```
S.Name
```

instead of

```
Student.Name
```

Renaming becomes especially important in self-joins.

---

# 6. Combining Operations

Suppose we want

> Names of all CS students.

First

Select CS students

```
σ(Major='CS')(Student)
```

Then

Project names

```
π(Name)(
    σ(Major='CS')(Student)
)
```

Equivalent SQL

```sql
SELECT Name
FROM Student
WHERE Major='CS';
```

Notice

Selection happens

↓

Projection happens

↓

Final result

Operations compose like functions.

---

# 7. Example Translation

SQL

```sql
SELECT Name
FROM Student
WHERE GPA > 3.5;
```

Relational Algebra

```
π(Name)
(
    σ(GPA>3.5)
    (
        Student
    )
)
```

Read from inside out.

```
Student

↓

Select GPA>3.5

↓

Keep Name

↓

Result
```

---

# 8. Why Database Engineers Care

Every SQL compiler eventually produces a relational algebra tree.

Example

```
SELECT Name
FROM Student
WHERE Major='CS';
```

becomes

```
Projection(Name)

        |

Selection(Major='CS')

        |

Student
```

The optimizer now transforms that tree.

For example,

```
Projection

↓

Selection
```

might become

```
Selection

↓

Projection
```

if doing so reduces the amount of data processed.

This is why relational algebra is the foundation of **query optimization**.

---

# 9. SQL vs. Relational Algebra

| SQL | Relational Algebra |
|------|--------------------|
| User language | Internal mathematical language |
| Declarative | Formal mathematical notation |
| Executed by users | Executed by the optimizer |
| Friendly | Precise |



# 10. Joins

In a relational database, information is usually spread across multiple relations.

Consider the following two relations.

## Students

| sid | name |
|----:|------|
| 1 | Alice |
| 2 | Bob |
| 3 | Charlie |

## Enrollments

| sid | course |
|----:|--------|
| 1 | Database Systems |
| 2 | Operating Systems |
| 2 | Computer Networks |
| 3 | Artificial Intelligence |

Suppose we want to answer:

> Which student is enrolled in which course?

Notice that neither table contains all the required information.

Students contains names.

Enrollments contains courses.

We must combine them.

---

# 11. The Cartesian Product Approach

The most basic way to combine two relations is the Cartesian Product.

Relational Algebra:

```text
Students × Enrollments
```

Result:

| sid | name | sid | course |
|----:|------|----:|--------|
|1|Alice|1|Database Systems|
|1|Alice|2|Operating Systems|
|1|Alice|2|Computer Networks|
|1|Alice|3|Artificial Intelligence|
|2|Bob|1|Database Systems|
|2|Bob|2|Operating Systems|
|2|Bob|2|Computer Networks|
|2|Bob|3|Artificial Intelligence|
|3|Charlie|1|Database Systems|
|3|Charlie|2|Operating Systems|
|3|Charlie|2|Computer Networks|
|3|Charlie|3|Artificial Intelligence|

There are many rows that clearly don't belong together.

---

# 12. Applying Selection

Now keep only rows where the student IDs match.

Relational Algebra:

```text
σ Students.sid = Enrollments.sid
(
    Students × Enrollments
)
```

Result:

| sid | name | sid | course |
|----:|------|----:|--------|
|1|Alice|1|Database Systems|
|2|Bob|2|Operating Systems|
|2|Bob|2|Computer Networks|
|3|Charlie|3|Artificial Intelligence|

Now the result is meaningful.

---

# 13. Defining the Join Operator

Since this pattern appears constantly, relational algebra defines a new operator.

Instead of writing

```text
σ condition (A × B)
```

we write

```text
A ⨝condition B
```

This is called the **Theta Join**.

General definition:

```text
A ⨝condition B

≡

σ condition (A × B)
```

The join operator is therefore a shorthand notation.

It is **not** one of the primitive operators.

---

# 17. Theta Join (⨝θ)

Definition:

Join two relations using any comparison operator.

Possible conditions:

```text
=

≠

<

>

≤

≥
```

Example:

```text
Employees ⨝ Employees.salary > Departments.budget Departments
```

Although equality joins are most common, theta joins allow any comparison.

---

# 18. Equijoin

An Equijoin is simply a theta join where the comparison is equality.

Example:

```text
Students ⨝ Students.sid = Enrollments.sid Enrollments
```

Equivalent SQL:

```sql
SELECT *
FROM Students
JOIN Enrollments
ON Students.sid = Enrollments.sid;
```

---

# 19. Natural Join (⨝)

A Natural Join is even simpler.

It automatically joins attributes that

- have the same name
- represent the same domain

Example:

Students

| sid | name |
|----:|------|
|1|Alice|
|2|Bob|

Enrollments

| sid | course |
|----:|--------|
|1|Database Systems|
|2|Operating Systems|

Natural Join:

```text
Students ⨝ Enrollments
```

Result:

| sid | name | course |
|----:|------|--------|
|1|Alice|Database Systems|
|2|Bob|Operating Systems|

Notice something important.

The duplicate sid column disappears automatically.


# 10. Join Algorithms

Real databases rarely compute

```text
A × B
```

first.

Instead they use algorithms like

- Nested Loop Join
- Hash Join
- Merge Join

These algorithms produce exactly the same result while avoiding the enormous intermediate Cartesian Product.

Eventually your execution engine might contain a class like

```cpp
class Join : public Operator
{
};
```

Possible implementations

```text
NestedLoopJoin

HashJoin

MergeJoin
```

The query planner chooses which implementation to use.

This is one of the optimizer's most important decisions.

---

# 20. Relationship to SQL

SQL

```sql
SELECT s.name, e.course
FROM Students s
JOIN Enrollments e
ON s.sid = e.sid;
```

Parser

↓

AST

↓

Relational Algebra

```text
π name, course
(
    Students ⨝ Students.sid = Enrollments.sid Enrollments
)
```

↓

Optimizer

↓

Execution Plan

↓

Hash Join (for example)

↓

Result

This is the pipeline followed by virtually every relational database system.

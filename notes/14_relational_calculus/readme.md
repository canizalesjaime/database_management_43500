# Lecture: Relational Calculus

## Learning Objectives

By the end of this lecture, you should understand:

- What relational calculus is
- The difference between relational algebra and relational calculus
- Tuple Relational Calculus (TRC)
- Domain Relational Calculus (DRC)
- How SQL relates more closely to relational calculus than relational algebra
- Why relational calculus is important even though databases implement relational algebra internally
- The connection between relational calculus and Codd's Theorem

---

# 1. Motivation

So far, we've learned relational algebra.

Example

```text
πname(σage>18(Users))
```

This tells the database:

1. Read Users
2. Select rows where age > 18
3. Project the name column

This is procedural.

It describes **how** to obtain the answer.

Relational calculus takes a completely different approach.

Instead of describing how to compute the result, it describes **what the result should satisfy**.

---

# 2. Procedural vs Declarative

Suppose we ask

"Find the names of users older than 18."

Relational Algebra

```text
πname(σage>18(Users))
```

This describes a sequence of operations.

Relational Calculus

```text
{ t.name |
    Users(t)
    AND t.age > 18
}
```

This says

> Return every name belonging to a tuple t such that
>
> - t belongs to Users
> - age > 18

There is no mention of

- Selection
- Projection
- Execution order
- Join algorithms

Only the desired result.

---

# 3. Why Is SQL Declarative?

Consider

```sql
SELECT name
FROM Users
WHERE age > 18;
```

Notice what SQL does **not** say.

It never says

- Scan the table
- Filter rows
- Project columns

It simply specifies

"I want the names of users older than 18."

The database decides how to compute the answer.

This is exactly the philosophy behind relational calculus.

---

# 4. Two Types of Relational Calculus

There are two major forms.

1. Tuple Relational Calculus (TRC)

2. Domain Relational Calculus (DRC)

They are mathematically equivalent.

---

# 5. Tuple Relational Calculus (TRC)

TRC works with tuples.

General form

```text
{ t | P(t) }
```

Read this as

"Return every tuple t such that predicate P is true."

---

Example

Relation

Users

| id | name | age |
|---:|------|----:|
|1|Alice|21|
|2|Bob|16|
|3|Carol|35|

Query

```text
{ t |
    Users(t)
    AND t.age >18
}
```

Result

| id | name | age |
|---:|------|----:|
|1|Alice|21|
|3|Carol|35|

---

# 6. Returning Only Certain Attributes

Suppose we only want names.

```text
{ t.name |
    Users(t)
    AND t.age >18
}
```

Result

```text
Alice

Carol
```

Notice that this corresponds to

Relational Algebra

```text
πname(σage>18(Users))
```

---

# 7. Domain Relational Calculus (DRC)

Instead of variables representing entire tuples,

variables represent individual attribute values.

General form

```text
{ <x,y,z> | Predicate }
```

Example

```text
{
    <n> |

    ∃id

    ∃age

    Users(id,n,age)

    AND age >18
}
```

Read

"There exists an id and an age such that

(id,n,age)

belongs to Users

and

age >18."

Result

```text
Alice

Carol
```

---

# 8. Logical Symbols

Relational calculus borrows notation from first-order logic.

| Symbol | Meaning |
|--------|---------|
| ∧ | AND |
| ∨ | OR |
| ¬ | NOT |
| → | Implies |
| ∃ | There exists |
| ∀ | For every |

---

Example

```text
Users(t)

AND

t.age >18

AND

t.salary >50000
```

can be written

```text
Users(t)

∧

t.age >18

∧

t.salary >50000
```

---

# 9. Existential Quantifier

The symbol

```text
∃
```

means

"There exists..."

Example

```text
∃t

Users(t)

AND

t.name = "Alice"
```

Read

"There exists a tuple t in Users whose name is Alice."

---

# 10. Universal Quantifier

The symbol

```text
∀
```

means

"For every..."

Example

```text
∀t

Users(t)

→

t.age >0
```

Read

"For every tuple in Users,

its age is greater than zero."

Universal quantifiers are much less common in SQL.

---

# 11. Example Join

SQL

```sql
SELECT Users.name
FROM Users
JOIN Orders
ON Users.id = Orders.user_id;
```

TRC

```text
{
    u.name |

    Users(u)

    AND

    Orders(o)

    AND

    u.id = o.user_id
}
```

Notice

We never say

Join.

We only specify the relationship that must hold.

---

# 12. Compare SQL, Algebra, and Calculus

SQL

```sql
SELECT name
FROM Users
WHERE age >18;
```

Relational Algebra

```text
πname(σage>18(Users))
```

Tuple Relational Calculus

```text
{
    t.name |

    Users(t)

    AND

    t.age >18
}
```

All three describe the same query.

---

# 13. Why Doesn't PostgreSQL Execute Calculus?

Because relational calculus is not an algorithm.

It simply describes the desired result.

The optimizer needs something procedural.

Therefore

```text
SQL

↓

Parser

↓

AST

↓

Relational Algebra Tree

↓

Optimization

↓

Physical Plan
```

Notice

Relational calculus never appears in the implementation.

Instead,

SQL is interpreted as having relational-calculus semantics and is translated into relational algebra.

---

# 14. Safe Relational Calculus

Consider

```text
{
    x |

    x is not in Users
}
```

What should the answer be?

Every possible value in the universe except those in Users.

That set is infinite.

This is not computable.

To avoid queries like this,

database theory defines **safe relational calculus**.

Safe queries always produce finite results.

SQL is designed so that its queries correspond to safe relational calculus.

---

# 15. Codd's Theorem

One of the most important theorems in database theory states:

Safe Relational Calculus

=

Relational Algebra

They have exactly the same expressive power.

This means

Every relational algebra query

↓

can be written as

↓

relational calculus

and

Every safe relational calculus query

↓

can be translated into

↓

relational algebra.

This is why SQL can be declarative while the database internally uses relational algebra.

---

# 16. Where Relational Calculus Fits

Think of the complete picture.

```text
User Thinks

↓

SQL

↓

Declarative Meaning

(Relational Calculus)

↓

Compiler

↓

Relational Algebra Tree

↓

Optimization

↓

Physical Plan

↓

Execution Engine
```

The user thinks declaratively.

The compiler thinks procedurally.

---

# Homework

For each SQL query below:

1. Write the equivalent relational algebra expression.
2. Write the equivalent Tuple Relational Calculus expression.

Query 1

```sql
SELECT name
FROM Users
WHERE age > 18;
```

Query 2

```sql
SELECT Users.name
FROM Users
JOIN Orders
ON Users.id = Orders.user_id;
```

Query 3

```sql
SELECT course
FROM Enrollments
WHERE grade = 'A';
```
# Query Optimization Basics

## Learning Objectives

By the end of this lecture, you should understand:

- What query optimization is
- Why relational algebra is optimized before execution
- The difference between logical optimization and physical optimization
- The most common relational algebra rewrite rules
- How a logical query becomes a physical execution plan

---

# 1. Where Does Query Optimization Fit?

Recall the architecture of a relational database system.

```text
SQL Query
    │
    ▼
Lexer
    │
    ▼
Parser
    │
    ▼
AST
    │
    ▼
Semantic Analyzer
    │
    ▼
Relational Algebra (Logical Plan)
    │
    ▼
Logical Query Optimizer
    │
    ▼
Physical Query Planner
    │
    ▼
Execution Plan
    │
    ▼
Execution Engine
```

Notice that optimization occurs **before** the query is executed.

No data has been read from disk yet.

The optimizer is simply transforming one relational algebra tree into another equivalent tree.

---

# 2. Why Optimize?

Suppose a user writes

```sql
SELECT name
FROM Users
WHERE age > 18;
```

The parser might generate

```text
Projection(name)
        │
Selection(age > 18)
        │
Users
```

This already works.

So why optimize?

Because many different relational algebra trees compute exactly the same answer, but some require much less work.

The optimizer's goal is to find one of the cheaper alternatives.

---

# 3. Logical vs Physical Optimization

This distinction is extremely important.

## Logical Optimization

Logical optimization changes the relational algebra tree.

Example:

```text
Projection
        │
Selection
        │
Join
```

↓

```text
Projection
        │
Join
     /      \
Selection    B
     │
A
```

The meaning of the query has not changed.

Only the logical organization has changed.

---

## Physical Optimization

Physical optimization chooses implementations.

Example

Logical operator

```text
Join
```

↓

Physical operator

```text
HashJoin
```

or

```text
MergeJoin
```

or

```text
NestedLoopJoin
```

Likewise,

```text
Users
```

might become

```text
TableScan
```

or

```text
IndexScan
```

---

# 4. Rule-Based Optimization

The simplest optimizer repeatedly applies rewrite rules.

Each rule preserves the meaning of the query.

Example

Before

```text
Selection
        │
Cartesian Product
```

After

```text
Join
```

Same result.

Better execution.

---

# 5. Rule 1 — Selection Pushdown

Suppose

```sql
SELECT *
FROM Users
JOIN Orders
ON Users.id = Orders.user_id
WHERE Users.age > 18;
```

Parser output

```text
Selection(age >18)
        │
Join
     /      \
Users      Orders
```

Notice

The selection only depends on Users.

Move it downward.

Optimized

```text
Join
     /      \
Selection    Orders
(age >18)
     │
Users
```

Now the join processes fewer tuples.

This is one of the most important optimization rules.

---

# 6. Rule 2 — Projection Pushdown

Suppose

```sql
SELECT Users.name
FROM Users
JOIN Orders
ON Users.id = Orders.user_id;
```

Users contains

```text
id
name
email
address
phone
salary
...
```

The join only needs

```text
id

name
```

Everything else is unnecessary.

Optimized tree

```text
Join
     /      \
Projection   Projection
(id,name)    (user_id)
     │            │
Users        Orders
```

Less data moves through the execution engine.

---

# 7. Rule 3 — Replace Product + Selection with Join

Parser output

```text
Selection(A.id = B.id)
        │
Cartesian Product
     /          \
A              B
```

Optimizer

↓

```text
Join(A.id = B.id)
     /          \
A              B
```

Now the physical planner can choose

- Hash Join
- Merge Join
- Nested Loop Join

---

# 8. Rule 4 — Join Reordering

Suppose

```sql
SELECT *
FROM A
JOIN B
ON A.id = B.id
JOIN C
ON B.id = C.id;
```

Parser

```text
(A ⋈ B)

↓

Join with C
```

Suppose

| Relation | Rows |
|----------|------|
| A | 10,000,000 |
| B | 100 |
| C | 50 |

Joining A first is expensive.

Instead

```text
B ⋈ C

↓

Join with A
```

The final answer is identical.

The intermediate results are much smaller.

---

# 9. Rule 5 — Remove Redundant Operations

Suppose

```text
Projection(*)
```

Keeping every attribute changes nothing.

Remove it.

Suppose

```text
Selection(TRUE)
```

Always true.

Remove it.

Optimizers eliminate unnecessary operators whenever possible.

---

# 10. Rule 6 — Predicate Simplification

Suppose

```sql
WHERE age > 18
AND age > 10
```

The second condition is redundant.

Simplify

```text
age > 18
```

Likewise

```sql
WHERE TRUE AND age > 18
```

becomes

```sql
WHERE age > 18
```

---

# 11. Cost-Based Optimization

Eventually rewrite rules are not enough.

Suppose two equivalent plans exist.

Plan A

```text
Hash Join
```

Plan B

```text
Merge Join
```

Which is better?

It depends.

The optimizer estimates

- number of rows
- available memory
- indexes
- sort order
- selectivity

Then computes an estimated cost.

Example

| Plan | Estimated Cost |
|------|----------------|
| Nested Loop | 2,500 |
| Hash Join | 180 |
| Merge Join | 230 |

Choose

```text
Hash Join
```

This is called **Cost-Based Optimization (CBO).**

Modern databases such as PostgreSQL rely heavily on cost-based optimization.

---

# 12. Example Optimization

User Query

```sql
SELECT Users.name
FROM Users
JOIN Orders
ON Users.id = Orders.user_id
WHERE Users.age > 18;
```

Initial Logical Plan

```text
Projection(name)
        │
Selection(age >18)
        │
Join
     /      \
Users      Orders
```

Apply Selection Pushdown

```text
Projection(name)
        │
Join
     /      \
Selection    Orders
(age >18)
     │
Users
```

Apply Projection Pushdown

```text
Projection(name)
        │
Join
     /      \
Projection   Projection
(id,name)    (user_id)
     │            │
Selection      Orders
     │
Users
```

Physical Planner

↓

```text
Projection
        │
HashJoin
     /        \
TableScan   IndexScan
```

Execution Engine

↓

Results

---

# 13. The Optimizer Never Changes the Meaning

This is the optimizer's fundamental rule.

Every transformation must preserve correctness.

For every rewrite

```text
Old Plan

↓

New Plan
```

both plans must produce exactly the same tuples.

Only the execution cost may change.

---

# Homework

Given the query

```sql
SELECT Employees.name
FROM Employees
JOIN Departments
ON Employees.did = Departments.did
WHERE Employees.salary > 90000;
```

1. Draw the initial relational algebra tree produced by the parser.

2. Apply Selection Pushdown.

3. Apply Projection Pushdown.

4. Identify where the physical planner would decide between:
   - TableScan vs IndexScan
   - Nested Loop vs Hash Join vs Merge Join

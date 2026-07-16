# Physical Planning: Where the Compiler Ends and the Database Begins

## Objectives

By the end of this lecture, you should be able to:

- Understand the difference between logical and physical query plans.
- Understand where the SQL compiler frontend ends.
- Understand what a physical planner does.
- Recognize the major physical operators used by real databases.
- Appreciate why physical planning belongs to the backend rather than the compiler frontend.
- Understand how every compiler phase fits together.
- Build a complete compilation pipeline.
- Organize the project into clean modules.
- Design a robust `main.py`.
- Understand how real compilers orchestrate compilation.
- Review the complete compiler pipeline.
- Understand how each module contributes to compilation.
- Compare your compiler to industrial database systems.
- Identify natural directions for future work.

---

# Where We Are

Our compiler now produces an optimized logical query plan.

```text
SQL
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
Semantic Analysis
 │
 ▼
Relational Algebra Generation
 │
 ▼
Logical Optimization
 │
 ▼
Optimized Logical Plan
```

For our compiler, this is the final output.

A real database, however, has more work to do.

---

# Logical vs Physical Plans

Consider

```sql
SELECT name
FROM Users
WHERE age > 18;
```

Our compiler produces

```text
Projection(name)
        │
Selection(age > 18)
        │
TableScan(Users)
```

Notice something interesting.

The tree never says **how** the table should be read.

It only says

```
Read Users.
```

This is called a **logical operator**.

---

# Physical Operators

A backend replaces logical operators with physical ones.

Instead of

```text
TableScan
```

the planner might choose

```text
SequentialScan
```

or

```text
IndexScan
```

Both satisfy the meaning of TableScan.

One may simply be faster.

---

# Why Multiple Physical Operators Exist

Imagine a table with

```
10 rows
```

Reading the entire table is trivial.

Now imagine

```
100 million rows
```

Reading every row could be extremely expensive.

If an index exists on

```
age
```

the planner might choose

```text
IndexScan
```

instead.

The logical plan never changes.

Only the implementation changes.

---

# Another Example

Logical plan

```text
Selection(age > 18)

        │

TableScan(Users)
```

Possible physical plan

```text
Selection(age > 18)

        │

IndexScan(Users, age_index)
```

The result is identical.

The execution strategy is different.

---

# JOINs Introduce More Choices

Suppose we had

```sql
SELECT *
FROM Users
JOIN Orders
ON Users.id = Orders.user_id;
```

Logical plan

```text
Join

 /   \

Users Orders
```

A physical planner now has choices.

---

Nested Loop Join

```text
NestedLoopJoin
```

Hash Join

```text
HashJoin
```

Merge Join

```text
MergeJoin
```

All compute the same result.

Some are dramatically faster depending on the data.

---

# Cost-Based Optimization

How does the planner choose?

It estimates

- number of rows
- selectivity
- index availability
- memory usage
- CPU cost
- disk I/O

Then it estimates the cost of every possible plan.

Finally it chooses the cheapest one.

This is called **cost-based optimization**.

---

# Where Execution Begins

Eventually the backend produces

```text
Projection

      │

Selection

      │

IndexScan
```

An execution engine walks this tree.

Each operator produces tuples.

Eventually the Projection operator returns the final result to the user.

---

# Why We Stop Here

Our project focuses on compiler design.

Everything we've implemented belongs to the compiler frontend.

Physical planning depends on

- indexes,
- statistics,
- storage,
- execution,
- disk pages,
- buffer pools.

Those belong to the database backend.

Understanding that boundary is enough to understand how real systems are organized.


# Integrating the SQL Compiler Frontend Pipeline
## The Big Picture

Over the course of this project we implemented the following modules.

```text
lexer.py

parser.py

ast.py

visitor.py

semantic.py

relational_algebra.py

rel_visitor.py

algebra.py

optimizer.py
```

Each module performs exactly one job.

Together they form the compiler.

---

# The Compilation Pipeline

```text
SQL Query

↓

Lexer

↓

Tokens

↓

Parser

↓

AST

↓

Semantic Analyzer

↓

Annotated AST

↓

Algebra Generator

↓

Relational Algebra Tree

↓

Optimizer

↓

Optimized Logical Plan
```

Every phase consumes the output of the previous phase.

This is one of the defining characteristics of compiler architecture.

---

# The Driver Program

The compiler itself should not contain business logic.

Instead,

`main.py`

coordinates every phase.

Conceptually

```python
query

↓

Lexer

↓

Parser

↓

SemanticAnalyzer

↓

AlgebraGenerator

↓

Optimizer

↓

print(result)
```

Each module remains independent.

---

# Error Handling

Compilation should stop immediately when an error occurs.

Examples

Lexer

```
Unexpected character
```

Parser

```
Expected FROM
```

Semantic Analyzer

```
Unknown column agee
```

Each phase either

- succeeds,
- or reports an error.

Later phases should never execute after a failure.

---

# Printing Intermediate Representations

One of the easiest debugging techniques is to print every representation.

```text
SQL

↓

Tokens

↓

AST

↓

Annotated AST

↓

Relational Algebra

↓

Optimized Algebra
```

This allows you to isolate problems quickly.

---

# Module Responsibilities

Every module should have one responsibility.

Lexer

```
characters → tokens
```

Parser

```
tokens → AST
```

Semantic Analyzer

```
AST validation
```

Algebra Generator

```
AST → Relational Algebra
```

Optimizer

```
Relational Algebra → Better Relational Algebra
```

Notice that every phase has a very clear input and output.

---

# Testing

Each module should be tested independently.

Lexer

Input

```sql
SELECT name
FROM Users;
```

Output

```
SELECT
IDENTIFIER(name)
FROM
IDENTIFIER(Users)
...
```

Parser

Verify the AST.

Semantic Analyzer

Verify errors.

Optimizer

Verify tree rewrites.

Small isolated tests are much easier to debug than one enormous integration test.

---

# Future Extensions

The architecture now makes future additions straightforward.

Adding

```
ORDER BY
```

requires changes to

- lexer
- parser
- AST
- semantic analyzer
- algebra generator
- optimizer

No existing architecture must change.

This is the advantage of a modular compiler.

# SQL Compiler Frontend Review and Future Directions
## The Complete Pipeline

Our finished frontend performs

```text
SQL Query
    │
Lexer
    │
Parser
    │
AST
    │
Semantic Analysis
    │
Relational Algebra Generation
    │
Logical Optimization
    │
Optimized Logical Plan
```

This is a complete SQL compiler frontend.

---

# Module Review

## lexer.py

Input

```
characters
```

Output

```
tokens
```

---

## parser.py

Input

```
tokens
```

Output

```
AST
```

---

## semantic.py

Input

```
AST
```

Output

```
Annotated AST
```

Responsibilities

- symbol resolution
- table validation
- column validation
- type checking

---

## algebra.py

Input

```
Annotated AST
```

Output

```
Relational Algebra Tree
```

---

## optimizer.py

Input

```
Relational Algebra Tree
```

Output

```
Optimized Logical Plan
```

---

# The Two Trees

During the project we built two different tree representations.

## AST

Represents

```
SQL syntax
```

Examples

- SelectStatement
- Identifier
- Literal
- BinaryExpression

---

## Relational Algebra Tree

Represents

```
database operations
```

Examples

- Projection
- Selection
- TableScan
- Join

The optimizer operates exclusively on this tree.

---

# The Two Visitor Hierarchies

AST

```text
ASTVisitor

│

├── SemanticAnalyzer

└── AlgebraGenerator
```

Relational Algebra

```text
RelVisitor

│

└── Optimizer
```

This separation keeps each compilation stage focused on the representation it understands.

---

# What We Did Not Build

Industrial SQL databases contain many additional features.

Examples

- JOIN
- GROUP BY
- HAVING
- ORDER BY
- DISTINCT
- Aggregate functions
- Subqueries
- Window functions
- Views
- Common Table Expressions (CTEs)

Adding these features would extend the same architecture rather than replace it.

---

# What the Backend Would Add

If this project continued into a backend,

the next components would include

```text
Physical Planner

↓

Execution Engine

↓

Storage Manager

↓

Buffer Pool

↓

Disk
```

Notice that none of these components require changing the frontend pipeline.

The frontend and backend are cleanly separated.

---

# Comparison with PostgreSQL

Although PostgreSQL is vastly more sophisticated, its high-level architecture is remarkably similar.

```text
SQL

↓

Lexer

↓

Parser

↓

Parse Tree

↓

Semantic Analysis

↓

Query Rewrite

↓

Relational Algebra / Query Tree

↓

Optimizer

↓

Physical Planner

↓

Executor
```

Many of the concepts you implemented mirror those used in production systems.

The main differences are scale, complexity, and decades of additional engineering.

---

# Lessons Learned

Throughout this project you encountered several fundamental compiler concepts.

- Lexical analysis
- Context-free grammars
- Recursive-descent parsing
- Abstract Syntax Trees
- Visitor pattern
- Semantic analysis
- Symbol tables
- Intermediate representations
- Tree rewriting
- Rule-based optimization

These concepts extend far beyond SQL and appear throughout compiler construction.

---

# Possible Future Projects

If you choose to continue this compiler, natural next milestones include

- Support JOIN
- Add logical Join nodes
- Add AND and OR expressions
- Add ORDER BY
- Add GROUP BY
- Support aggregate functions
- Implement predicate pushdown
- Build a Graphviz AST visualizer
- Build a relational algebra visualizer
- Add unit tests for every compiler phase
- Implement a simple REPL
- Add source locations and improved error messages

Each enhancement builds naturally on the architecture you've already established.

---

# Final Thoughts

At the beginning of this course, a SQL query was simply a string.

By the end, you can follow that string through every stage of compilation:

```text
Characters

↓

Tokens

↓

Grammar

↓

AST

↓

Semantically Valid AST

↓

Relational Algebra

↓

Optimized Logical Plan
```

This transformation—from raw text to a structured, optimized representation—is the essence of compiler design.

Whether you later extend this project into a full database system or move on to other compiler projects, the architectural principles you've learned here are widely applicable.
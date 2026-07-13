# Semantic Analysis

## Objectives

By the end of this lecture, you should be able to:

- Understand the purpose of semantic analysis.
- Distinguish between syntax errors and semantic errors.
- Understand the role of a database catalog.
- Understand symbol tables in the context of SQL.
- Learn how compiler passes traverse an AST.
- Prepare the AST for relational algebra generation.
- Understand why the Visitor Pattern is used in compilers.
- Understand how visitors traverse an AST.
- Understand the concept of double dispatch.
- Implement a generic AST visitor.
- Prepare the compiler for semantic analysis and future compiler passes.

---
# Where We Are in the Compiler

So far, we have built the frontend of our SQL compiler up through parsing.

```
SQL Query
    │
    ▼
Lexer
    │
    ▼
Tokens
    │
    ▼
Parser
    │
    ▼
AST
```

The parser guarantees that the SQL query is **syntactically correct**.

However, syntax alone is not enough.

Consider the following query.

```sql
SELECT salary
FROM Users;
```

The parser accepts this query because it follows the SQL grammar.

But what if the `Users` table does not contain a `salary` column?

The query is still incorrect.

This is where semantic analysis begins.

---

# What is Semantic Analysis?

## Definition

Semantic analysis is the compiler phase that verifies the **meaning** of a program or query.

The semantic analyzer asks questions that cannot be answered by the grammar alone.

Examples include:

- Does the referenced table exist?
- Does the referenced column exist?
- Is the expression type-correct?
- Are identifiers unambiguous?
- Are SQL rules being followed?

---

# Syntax vs Semantics

Consider three different SQL queries.

## Lexical Error

```sql
SELECT @name
FROM Users;
```

The lexer rejects this query because `@` is not a valid token.

---

## Syntax Error

```sql
FROM Users
SELECT name;
```

The lexer succeeds.

The parser rejects the query because the tokens do not match the SQL grammar.

---

## Semantic Error

```sql
SELECT salary
FROM Users;
```

Suppose the table is

```
Users

id
name
age
```

The parser accepts the query.

The semantic analyzer rejects it because `salary` does not exist.

---

# The Compiler Pipeline

The compiler now becomes

```
SQL Query
    │
    ▼
Lexer
    │
    ▼
Tokens
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
Validated AST
```

Notice that semantic analysis works entirely on the AST.

It never reads the SQL text.

---

# What Information Does the Semantic Analyzer Need?

Unlike the parser,

the semantic analyzer cannot determine correctness from the query alone.

It needs information about the database.

This information is called the **catalog**.

---

# The Database Catalog

The catalog contains metadata describing the database.

For example,

```
Users

id      INTEGER
name    TEXT
age     INTEGER
```

can be represented as

```python
catalog = {
    "Users": {
        "id": "INTEGER",
        "name": "TEXT",
        "age": "INTEGER"
    }
}
```

Think of the catalog as the compiler's knowledge of the database schema.

---

# What Does the Semantic Analyzer Check?

Our first semantic analyzer will perform five checks.

---

## 1. Table Exists

Query

```sql
SELECT id
FROM Customers;
```

Catalog

```
Users
Orders
Products
```

Result

```
Semantic Error

Unknown table "Customers"
```

---

## 2. Column Exists

Query

```sql
SELECT salary
FROM Users;
```

Catalog

```
Users

id
name
age
```

Result

```
Semantic Error

Unknown column "salary"
```

---

## 3. WHERE Clause Validation

Query

```sql
SELECT id
FROM Users
WHERE height > 180;
```

Result

```
Semantic Error

Unknown column "height"
```

---

## 4. Type Checking

Suppose

```
age : INTEGER
```

Then

```sql
WHERE age > 'hello'
```

is invalid.

The semantic analyzer verifies that operators are applied to compatible types.

---

## 5. Name Resolution

Suppose

```sql
SELECT id
FROM Users
JOIN Orders ...
```

Both tables contain an `id` column.

Which one does

```
id
```

refer to?

The semantic analyzer resolves these ambiguities.

---

# Symbol Tables

Almost every compiler uses symbol tables.

A symbol table stores information about identifiers.

For SQL,

the current table acts as a scope.

Example

```
Users

id
name
age
```

becomes

```python
symbol_table = {
    "id": "INTEGER",
    "name": "TEXT",
    "age": "INTEGER"
}
```

Whenever the compiler encounters

```
Identifier(age)
```

it consults the symbol table.

---

# Traversing the AST

The semantic analyzer walks the AST.

Example

```
SelectStatement
├── Column
│   └── Identifier(id)
├── Column
│   └── Identifier(name)
├── Table
│   └── Identifier(Users)
└── BinaryExpression (>)
    ├── Identifier(age)
    └── Literal(18)
```

Each node is visited exactly once.

---

# The Visitor Pattern

Rather than putting semantic logic inside every AST node,

we separate operations from the data structure.

Instead of

```
SelectStatement.check_semantics()
```

we create

```
SemanticAnalyzer
```

containing methods such as

```
visit_SelectStatement()

visit_Table()

visit_Column()

visit_BinaryExpression()

visit_Identifier()

visit_Literal()
```

Each method knows how to process one type of AST node.

---

# Why Use Visitors?

Many compiler passes need to traverse the AST.

Examples include

```
Pretty Printer

Semantic Analyzer

Relational Algebra Builder

Logical Optimizer

SQL Formatter
```

Rather than modifying the AST for every new feature,

each feature becomes another visitor.

This keeps the compiler modular and extensible.

---

# Semantic Analysis Example

Suppose the query is

```sql
SELECT name
FROM Users
WHERE age > 18;
```

The analyzer performs roughly the following steps.

```
Visit SelectStatement

↓

Visit Table

↓

Does Users exist?

↓

Yes

↓

Build symbol table

↓

Visit Columns

↓

Does name exist?

↓

Yes

↓

Visit BinaryExpression

↓

Does age exist?

↓

Yes

↓

Is INTEGER > INTEGER valid?

↓

Yes

↓

Semantic analysis succeeds
```

The validated AST is then passed to the next compiler phase.

---

# Semantic Errors vs Runtime Errors

Semantic errors occur **before execution**.

Example

```sql
SELECT salary
FROM Users;
```

No query is executed.

The compiler rejects it immediately.

Runtime errors occur later during execution.

Examples include

- disk failures
- deadlocks
- division by zero
- insufficient memory

Semantic analysis prevents many invalid queries from ever reaching the execution engine.

---

# Relation to Compiler Theory

Semantic analysis is common to nearly every compiler.

Programming language compilers perform tasks such as

- variable lookup
- scope resolution
- type checking
- function overload resolution

SQL compilers perform similar tasks

- table lookup
- column lookup
- alias resolution
- type checking
- aggregate validation

Although the languages differ, the compiler concepts are nearly identical.



# The Visitor Pattern

# Where We Are

Our SQL compiler currently looks like this.

```
SQL Query
    │
    ▼
Lexer
    │
    ▼
Tokens
    │
    ▼
Parser
    │
    ▼
AST
```

The parser's job is finished.

From now on, every compiler phase will operate on the AST.

For example,

```
AST
 │
 ├── Semantic Analyzer
 │
 ├── Relational Algebra Builder
 │
 ├── Logical Optimizer
 │
 └── Pretty Printer
```

Notice that every phase needs to traverse the exact same tree.

---

# The Problem

Suppose our AST node looks like this.

```python
class Identifier(Expression):

    def __init__(self, name):
        self.name = name
```

Now suppose we want to

- print the tree
- check semantics
- build relational algebra
- optimize queries

One approach is to place every operation inside the class.

```python
class Identifier(Expression):

    ...

    def print(self):
        ...

    def check_semantics(self):
        ...

    def build_relational_algebra(self):
        ...

    def optimize(self):
        ...
```

This quickly becomes a mess.

Every time we invent a new compiler phase,

we have to edit every AST class.

---

# The Better Solution

Instead,

keep the AST as simple as possible.

```
AST

contains only data
```

Move all compiler logic into separate objects called visitors.

```
AST
 │
 ├── SemanticAnalyzer
 │
 ├── PrettyPrinter
 │
 ├── RelationalAlgebraBuilder
 │
 └── Optimizer
```

The AST never changes.

Only the visitors change.

---

# The Visitor Pattern

A visitor is simply an object that knows how to process every kind of AST node.

Example

```
SemanticAnalyzer:

visit_SelectStatement()

visit_Table()

visit_Column()

visit_BinaryExpression()

visit_Identifier()

visit_Literal()
```

Each method handles one node type.

---

# Walking the Tree

Suppose the AST is

```
SelectStatement
├── Column
│   └── Identifier(id)
├── Column
│   └── Identifier(name)
├── Table
│   └── Identifier(Users)
└── BinaryExpression (>)
    ├── Identifier(age)
    └── Literal(18)
```

A visitor walks the tree.

```
Visit SelectStatement

↓

Visit Column

↓

Visit Identifier(id)

↓

Visit Column

↓

Visit Identifier(name)

↓

Visit Table

↓

Visit Identifier(Users)

↓

Visit BinaryExpression

↓

Visit Identifier(age)

↓

Visit Literal(18)
```

Every node is visited once.

---

# Generic Tree Traversal

Notice something.

Every compiler pass walks the tree in almost exactly the same order.

Only the work performed at each node changes.

For example,

Semantic Analyzer

```
Visit Identifier(age)

↓

Does age exist?
```

Pretty Printer

```
Visit Identifier(age)

↓

Print "age"
```

Relational Algebra Builder

```
Visit Identifier(age)

↓

Create Identifier node in relational algebra tree
```

Same traversal.

Different work.

---

# The Visitor Interface

A generic visitor usually has one method.

```python
visit(node)
```

The visitor examines the node's type and calls the correct method.

Example

```
visit()

↓

visit_SelectStatement()

or

visit_Table()

or

visit_Literal()
```

---

# Double Dispatch

The Visitor Pattern relies on a concept called **double dispatch**.

Instead of asking

```
Who am I?
```

the node asks

```
Who is visiting me?
```

Conceptually,

```
visitor.visit(node)

↓

node.accept(visitor)

↓

visitor.visit_SelectStatement(node)
```

The correct method is selected based on

- the visitor
- the node type

This is called double dispatch.

---

# Why Not Use Lots of if Statements?

We could write

```python
if isinstance(node, SelectStatement):
    ...

elif isinstance(node, Table):
    ...

elif isinstance(node, Identifier):
    ...
```

This works.

But every new node requires editing this giant function.

Visitors avoid this problem.

Each node type gets its own method.

---

# A Typical Visitor

Imagine a visitor that counts nodes.

```
visit_SelectStatement()

↓

count += 1

↓

visit children
```

```
visit_Table()

↓

count += 1
```

```
visit_Identifier()

↓

count += 1
```

The traversal remains identical.

Only the operation changes.

---

# Recursive Traversal

Most visitors are recursive.

Suppose we visit

```
BinaryExpression
```

The visitor naturally visits its children.

```
BinaryExpression

↓

left child

↓

right child
```

For

```
age > 18
```

the traversal becomes

```
BinaryExpression

↓

Identifier(age)

↓

Literal(18)
```

Recursive traversal mirrors the recursive structure of the AST.

---

# Why the Visitor Pattern is Ideal for Compilers

Imagine that six months from now we add

```
Query Cost Estimator
```

Without visitors,

every AST node must be modified.

With visitors,

we simply create

```
CostEstimatorVisitor
```

No AST classes change.

The compiler is therefore

- modular
- extensible
- easier to maintain

This is why visitors are common in compiler implementations.

---

# Our SQL Compiler

After introducing visitors,

our architecture becomes

```
SQL Query

↓

Lexer

↓

Parser

↓

AST

↓

Visitors

├── SemanticAnalyzer
├── RelationalAlgebraBuilder
├── LogicalOptimizer
└── PrettyPrinter
```

Notice that every remaining compiler phase is simply another visitor.

---

# What Will Our First Visitor Do?

Our first visitor will be

```
SemanticAnalyzer
```

It will

- verify the table exists
- verify columns exist
- build a symbol table
- check types
- validate expressions

If semantic analysis succeeds,

the AST is considered valid.

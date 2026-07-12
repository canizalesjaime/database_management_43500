# Compilers for SQL

## Objectives

By the end of this lecture, you should be able to:

- Explain the role of a lexer and parser in a SQL compiler.
- Distinguish between lexical analysis, syntax analysis, and semantic analysis.
- Understand why lexers are based on regular languages.
- Understand why parsers are based on context-free grammars (CFGs).
- Explain how an Abstract Syntax Tree (AST) is constructed.
- Understand the frontend architecture of a SQL compiler.
- Understand the purpose of semantic analysis.
- Distinguish between syntax errors and semantic errors.
- Understand the role of a database catalog.
- Understand symbol tables in the context of SQL.
- Learn how compiler passes traverse an AST.
- Understand why the Visitor Pattern is commonly used.
- Prepare the AST for relational algebra generation.

---

# The Frontend of a SQL Compiler

When a user submits a SQL query, the database cannot execute the text directly.

For example,

```sql
SELECT id, name
FROM Users
WHERE age > 18;
```

is simply a sequence of characters.

The frontend compiler transforms those characters into an internal representation that the rest of the database understands.

The frontend pipeline is

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
Abstract Syntax Tree (AST)
```

Each stage has a single responsibility.

---

# Stage 1 — Lexical Analysis (Lexer)

## Definition

A lexer (also called a lexical analyzer or scanner) reads a stream of characters and groups them into meaningful units called **tokens**.

The lexer answers the question:

> "What are the words of this language?"

---

## Input

```
SELECT id, name
FROM Users
WHERE age > 18;
```

---

## Output

```
SELECT
IDENTIFIER(id)
COMMA
IDENTIFIER(name)
FROM
IDENTIFIER(Users)
WHERE
IDENTIFIER(age)
GREATER_THAN
NUMBER(18)
SEMICOLON
EOF
```

Notice that whitespace has disappeared.

The lexer does not care about formatting.

---

# What is a Token?

A token has two parts:

- Token type
- Optional value

Example

```
Token(
    type = IDENTIFIER,
    value = "Users"
)
```

Another example

```
Token(
    type = NUMBER,
    value = 18
)
```

Keywords such as SELECT or FROM usually do not need a value because the token type already contains the information.

---

# Tokens in Our SQL Compiler

Our lexer currently recognizes

```
SELECT
FROM
WHERE

IDENTIFIER

NUMBER
STRING

EQUAL
GREATER_THAN
LESS_THAN

COMMA
SEMICOLON

EOF
```

Every SQL query is converted into a sequence of these tokens.

---

# Why Regular Expressions?

The patterns for SQL tokens are regular languages.

For example,

Identifier

```
[a-zA-Z_][a-zA-Z0-9_]*
```

Integer

```
[0-9]+
```

These patterns can be recognized by finite automata.

This is why lexers are traditionally implemented using regular expressions or finite-state machines.

---

# Our Lexer Implementation

Our identifier scanner

```python
while (
    self.peek() is not None
    and (self.peek().isalnum() or self.peek() == "_")
):
    self.advance()
```

implements the same language as

```
[a-zA-Z_][a-zA-Z0-9_]*
```

Likewise,

```python
while self.peek() is not None and self.peek().isdigit():
    self.advance()
```

implements

```
[0-9]+
```

The lexer is therefore an implementation of a collection of regular languages.

---

# What the Lexer Does NOT Do

The lexer does not know SQL grammar.

For example,

```
FROM Users SELECT id;
```

The lexer happily produces

```
FROM
IDENTIFIER(Users)
SELECT
IDENTIFIER(id)
SEMICOLON
```

It is not the lexer's job to determine whether the tokens appear in the correct order.

---

# Stage 2 — Syntax Analysis (Parser)

The parser receives the token stream from the lexer.

Input

```
SELECT
IDENTIFIER(id)
FROM
IDENTIFIER(Users)
WHERE
IDENTIFIER(age)
GREATER_THAN
NUMBER(18)
```

The parser asks

> "Do these tokens satisfy the SQL grammar?"

If the answer is yes,

the parser constructs an Abstract Syntax Tree.

---

# Context-Free Grammars (CFGs)

Parsers are driven by context-free grammars.

Our simplified SQL grammar is

```
query
    := SELECT select_list
       FROM table
       where_clause?
       SEMICOLON
       EOF

select_list
    := identifier
       (COMMA identifier)*

table
    := identifier

where_clause
    := WHERE comparison

comparison
    := identifier
       operator
       value

operator
    := EQUAL
     | GREATER_THAN
     | LESS_THAN

value
    := NUMBER
     | STRING
     | identifier

identifier
    := IDENTIFIER
```

The parser simply follows these production rules.

---

# Recursive-Descent Parsing

Our parser is a recursive-descent parser.

Each grammar rule corresponds almost exactly to one parser function.

Grammar

```
query
```

↓

Parser

```python
parse()
```

Grammar

```
select_list
```

↓

Parser

```python
parse_select_list()
```

Grammar

```
table
```

↓

Parser

```python
parse_table()
```

Grammar

```
where_clause
```

↓

Parser

```python
parse_where()
```

This one-to-one correspondence is one of the defining characteristics of recursive-descent parsing.

---

# The Abstract Syntax Tree (AST)

The parser does not merely verify correctness.

It also constructs an internal tree representation of the query.

For

```sql
SELECT id, name
FROM Users
WHERE age > 18;
```

our AST is

```
SelectStatement
├── Columns
│   ├── Column
│   │   └── Identifier(id)
│   └── Column
│       └── Identifier(name)
├── Table
│   └── Identifier(Users)
└── BinaryExpression (>)
    ├── Identifier(age)
    └── Literal(18)
```

Notice that every meaningful language construct is represented as a node.

---

# Why is it Called a Tree?

Each node points to its children.

For example,

```
SelectStatement
```

has three children

- Columns
- Table
- Where clause

The where clause is itself another node.

```
BinaryExpression
├── Identifier(age)
└── Literal(18)
```

The tree naturally captures the hierarchical structure of the SQL query.

---

# Parse Tree vs AST

The parser conceptually recognizes a parse tree based directly on the grammar.

A parse tree includes every grammar symbol.

Example

```
query
├── SELECT
├── select_list
├── FROM
├── table
├── where_clause
└── SEMICOLON
```

The AST removes unnecessary syntax.

```
SelectStatement
├── Columns
├── Table
└── BinaryExpression
```

The AST is therefore a simplified representation that is easier for later compiler stages to manipulate.

---

# What the Parser Does NOT Do

The parser checks syntax only.

It does not know whether

```
Users
```

is an actual table.

Nor does it know whether

```
salary
```

is a valid column.

The following query has correct syntax

```sql
SELECT salary
FROM Users;
```

but may still be incorrect if the Users table does not contain a salary column.

Those checks belong to semantic analysis.

---

# Lexical Analysis vs Syntax Analysis vs Semantic Analysis

The frontend consists of three logically distinct stages.

```
Characters
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
```

Responsibilities

Lexer

- Groups characters into tokens.
- Recognizes identifiers, keywords, numbers, strings, and punctuation.
- Based on regular languages.

Parser

- Verifies the token sequence satisfies the SQL grammar.
- Builds the AST.
- Based on context-free grammars.

Semantic Analyzer

- Validates the meaning of the query.
- Verifies tables exist.
- Verifies columns exist.
- Performs type checking.
- Resolves names and scopes.



# Semantic Analysis

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

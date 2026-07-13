# Compilers for SQL

## Objectives

By the end of this lecture, you should be able to:

- Explain the role of a lexer and parser in a SQL compiler.
- Distinguish between lexical analysis, syntax analysis, and semantic analysis.
- Understand why lexers are based on regular languages.
- Understand why parsers are based on context-free grammars (CFGs).
- Explain how an Abstract Syntax Tree (AST) is constructed.

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


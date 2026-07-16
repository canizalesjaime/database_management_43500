# Implementing the Relational Algebra Tree (`algebra.py`)

## Objectives

By the end of this lecture, you should be able to:

- Design a hierarchy of relational algebra nodes.
- Understand how the relational algebra tree parallels the AST.
- Implement the `AlgebraGenerator` visitor.
- Translate an annotated AST into a relational algebra tree.
- Understand why this tree becomes the compiler's primary representation.
- Understand why the first relational algebra tree is usually not the best one.
- Understand what it means for two query plans to be equivalent.
- Learn the classical rule-based optimization rules.
- Understand how an optimizer rewrites relational algebra trees.
- Prepare to implement `optimizer.py`.
- Implement your first optimizer.
- Traverse a relational algebra tree using `RelVisitor`.
- Apply rewrite rules recursively.
- Understand bottom-up optimization.
- Produce an optimized logical query plan.

---

# Where We Left Off

Our compiler currently performs:

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
Annotated AST
```

In the previous lecture we learned that the AST is no longer the ideal representation after semantic analysis.

Instead, we generate a new tree.

```text
Annotated AST
        │
        ▼
Relational Algebra Tree
```

Today's goal is to implement that transformation.

---

# A Familiar Pattern

When we built the AST, we designed a class hierarchy.

```text
ASTNode
│
├── Statement
├── Expression
├── Identifier
├── Literal
└── BinaryExpression
```

Now we will do exactly the same thing for relational algebra.

```text
RelNode
│
├── TableScan
├── Selection
├── Projection
└── Join
```

Notice the similarity.

Both are trees.

Both use inheritance.

Both represent information about the query.

The difference is **what** they represent.

---

# Designing the Base Class

Every relational operator is a RelNode.

```python
class RelNode:
    pass
```

Nothing special yet.

Its purpose is simply to give every relational operator a common parent.

Exactly like ASTNode.

---

# Unary vs Binary Operators

Notice something interesting.

Some relational operators have one child.

Example:

```text
Projection
      │
Selection
```

Projection has exactly one input.

Selection also has exactly one input.

These are **unary operators**.

---

Other operators have two children.

Example:

```text
        Join
       /    \
 Users      Orders
```

Join combines two relations.

It is a **binary operator**.

Our current compiler only supports unary operators.

Later, when we implement JOIN, we'll introduce binary operators.

---

# TableScan

The simplest operator.

```text
TableScan(Users)
```

It has no children.

It simply represents:

> Read the Users relation.

Conceptually:

```python
class TableScan(RelNode):

    def __init__(self, table):
        self.table = table
```

---

# Selection

Selection filters rows.

```text
Selection(age > 18)
        │
TableScan
```

Notice it stores two things.

- the condition
- its child

Conceptually:

```python
class Selection(RelNode):

    def __init__(self, condition, child):
        self.condition = condition
        self.child = child
```

The child is another RelNode.

---

# Projection

Projection removes columns.

```text
Projection(name)
        │
Selection(...)
```

Again, it stores

- columns
- child

```python
class Projection(RelNode):

    def __init__(self, columns, child):
        self.columns = columns
        self.child = child
```

---

# The Shape of the Tree

Notice that relational algebra nodes point to other relational algebra nodes.

Example:

```text
Projection
      │
Selection
      │
TableScan
```

This is exactly how our AST worked.

```text
BinaryExpression
    │
   / \
Expr Expr
```

The design philosophy is identical.

---

# Reusing the Visitor Pattern

Earlier we built

```python
SemanticAnalyzer(ASTVisitor)
```

Now we build

```python
AlgebraGenerator(ASTVisitor)
```

It walks the AST.

Instead of checking correctness,

it **returns RelNodes**.

---

# Visiting the Table

Suppose the AST contains

```text
Table(Users)
```

The visitor executes

```python
visit_Table(node)
```

and returns

```text
TableScan(Users)
```

This is the easiest translation.

---

# Visiting the WHERE Clause

The AST contains

```text
BinaryExpression
```

representing

```text
age > 18
```

We don't need to change this expression.

Selection simply stores it.

Result:

```text
Selection(age > 18)
```

Notice that the BinaryExpression remains an AST node.

Only the **operator tree** changes.

This is perfectly acceptable because the condition is already semantically valid.

---

# Visiting the SELECT Statement

This is where everything comes together.

Suppose the AST is

```text
SelectStatement
├── columns
├── table
└── where_clause
```

The algorithm is:

1. Visit the table.
2. Build a TableScan.
3. If there is a WHERE clause,
   wrap the scan in a Selection.
4. Wrap everything in a Projection.
5. Return the Projection.

Conceptually:

```text
scan

↓

selection

↓

projection
```

---

# Building the Tree Bottom-Up

Let's walk through the construction.

Start:

```text
TableScan(Users)
```

If there is a WHERE clause:

```text
Selection(age > 18)
        │
TableScan(Users)
```

Finally:

```text
Projection(name)
        │
Selection(age > 18)
        │
TableScan(Users)
```

Each new operator becomes the parent of the previous one.

---

# Why Bottom-Up Construction Works

Every operator consumes the output of another operator.

Projection cannot project rows until Selection has produced them.

Selection cannot filter rows until TableScan has produced them.

Therefore each operator naturally wraps the previous one.

This produces a pipeline.

---

# The Translation Algorithm

Conceptually, our visitor looks like this.

Input:

```text
SelectStatement
```

↓

Visit Table

↓

```text
TableScan
```

↓

Visit WHERE

↓

```text
Selection
```

↓

Visit SELECT

↓

```text
Projection
```

↓

Return the Projection node.

---

# Example

SQL

```sql
SELECT id, name
FROM Users
WHERE age > 18;
```

Annotated AST

```text
SelectStatement
├── Column(id)
├── Column(name)
├── Table(Users)
└── BinaryExpression(>)
```

Generated Relational Algebra Tree

```text
Projection(id,name)
        │
Selection(age > 18)
        │
TableScan(Users)
```

Notice how the SQL syntax has disappeared.

Only logical operations remain.

---

# Verifying the Translation

A useful debugging technique is to print both trees.

AST

```text
SelectStatement
├── ...
```

↓

Relational Algebra

```text
Projection
      │
Selection
      │
TableScan
```

Being able to compare these two trees makes debugging much easier.

---

# Why This Matters

From this point forward, every compiler phase operates on the relational algebra tree.

Future optimizations will transform

```text
Projection
      │
Selection
      │
TableScan
```

instead of

```text
SelectStatement
```

The SQL syntax has already served its purpose.

# Logical Query Optimization
## Where We Are

Our compiler now performs the following phases.

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
Logical Query Plan
```

For the first time, our compiler has produced an **intermediate representation** that is independent of SQL syntax.

For example,

```sql
SELECT name
FROM Users
WHERE age > 18;
```

becomes

```text
Projection(name)
        │
Selection(age > 18)
        │
TableScan(Users)
```

This tree correctly describes the operations required to answer the query.

The question now becomes:

> Is this the best logical plan?

Usually not.

---

# Correct Does Not Mean Efficient

The compiler's first responsibility is correctness.

Our relational algebra tree is correct.

However,

there are often many different relational algebra trees that produce exactly the same result.

Some require fewer operators.

Some perform less work.

Some expose additional optimization opportunities.

The optimizer's job is to transform a correct plan into a better one.

---

# Equivalent Query Plans

Consider these two plans.

Plan A

```text
Projection(name)
        │
Selection(age > 18)
        │
TableScan(Users)
```

Plan B

```text
Selection(age > 18)
        │
Projection(name, age)
        │
TableScan(Users)
```

Although the trees are different,

they can produce the same result.

These trees are **logically equivalent**.

Optimization simply replaces one equivalent tree with another.

---

# The Optimizer Never Changes the Answer

This is the most important rule of query optimization.

The optimizer is **not allowed** to change the query's meaning.

It may only change **how** the answer is computed.

Mathematically,

```text
Old Plan

≡

New Plan
```

where

```
≡
```

means

> "Produces exactly the same relation."

---

# Tree Rewriting

Notice that the optimizer never manipulates SQL text.

Instead,

it manipulates relational algebra trees.

Input

```text
Projection
      │
Selection
      │
TableScan
```

Output

```text
Projection
      │
TableScan
```

or perhaps

```text
Selection
      │
Projection
      │
TableScan
```

Every optimization is a tree transformation.

---

# Rule-Based Optimization

Our optimizer is a collection of rewrite rules.

Each rule has two parts.

1. Recognize a particular tree pattern.

2. Replace it with an equivalent—but simpler—tree.

Think of them as compiler rewrite rules.

---

# Rule 1 — Remove Empty Selection

Suppose we have

```text
Selection(TRUE)

      │

TableScan
```

Filtering with TRUE changes nothing.

Therefore,

rewrite the tree as

```text
TableScan
```

The Selection node disappears.

---

# Rule 2 — Merge Consecutive Selections

Suppose we encounter

```text
Selection(A)

      │

Selection(B)

      │

Child
```

Instead of filtering twice,

combine the predicates.

```text
Selection(A AND B)

         │

      Child
```

The tree becomes smaller.

---

# Rule 3 — Merge Consecutive Projections

Suppose we have

```text
Projection(A)

      │

Projection(B)

      │

Child
```

The lower Projection is unnecessary.

Rewrite

```text
Projection(A)

      │

Child
```

One operator disappears.

---

# Rule 4 — Remove Identity Projection

Suppose

```text
Projection(all columns)

        │

TableScan
```

If the Projection keeps every column,

it performs no work.

Remove it.

---

# Pattern Matching

Every optimization begins by recognizing a tree pattern.

Example

```text
Projection

      │

Projection
```

Pattern found.

↓

Rewrite.

↓

```text
Projection
```

The optimizer is essentially a collection of pattern-matching functions.

---

# The Optimizer Is Another Visitor

By now,

the visitor pattern should feel familiar.

We already have

```python
SemanticAnalyzer(ASTVisitor)
```

and

```python
AlgebraGenerator(ASTVisitor)
```

Now we introduce

```python
Optimizer(RelVisitor)
```

The only difference is that it traverses a relational algebra tree instead of an AST.

---

# The Optimization Algorithm

Every visit method follows exactly the same algorithm.

```text
Visit child

↓

Optimize child

↓

Apply optimization rules

↓

Return optimized subtree
```

Notice the order.

Children are always optimized before parents.

---

# Why Bottom-Up?

Consider

```text
Projection(name)

        │

Projection(name, age)

        │

TableScan
```

If we optimize the top Projection first,

we don't yet know whether the child can be simplified.

Instead,

we optimize

```text
Projection(name, age)
```

first.

Then the parent sees the simplest possible subtree.

This is why optimization proceeds from the leaves upward.

---

# Implementing the Visitor

Conceptually,

every visit method looks like

```python
visit_Projection(node):

    optimize child

    apply projection rules

    return node
```

Selection is similar.

```python
visit_Selection(node):

    optimize child

    apply selection rules

    return node
```

This should look familiar.

It is the same recursive structure used throughout the compiler.

---

# Returning New Nodes

An optimizer is allowed to return an entirely different node.

Example

Input

```text
Selection(TRUE)

      │

TableScan
```

Output

```text
TableScan
```

Notice

```
Selection
```

has disappeared completely.

The parent simply receives a different child.

---

# Example Walkthrough

Initial tree

```text
Projection(name)

        │

Projection(name, age)

        │

Selection(TRUE)

        │

TableScan
```

The visitor first reaches

```text
TableScan
```

Nothing changes.

Returning upward,

it sees

```text
Selection(TRUE)
```

Pattern recognized.

Rewrite

```text
Projection(name)

        │

Projection(name, age)

        │

TableScan
```

Returning upward again,

it sees

```text
Projection

↓

Projection
```

Pattern recognized.

Rewrite.

Final tree

```text
Projection(name)

        │

TableScan
```

The query produces exactly the same result,

but the logical plan is simpler.

---

# Recursive Rewriting

Optimization is recursive.

Each subtree is optimized independently.

```text
Optimize children

↓

Rewrite current node

↓

Return rewritten subtree
```

The optimizer never rewrites the entire tree at once.

It transforms one subtree at a time.

---

# Multiple Optimization Passes

Some optimizations expose additional opportunities.

Example

```text
Projection

      │

Projection

      │

Selection(TRUE)
```

Removing

```
Selection(TRUE)
```

creates another optimization opportunity.

Real database systems often perform multiple optimization passes until the tree stops changing.

For our compiler,

one recursive pass is sufficient.

The architecture easily supports additional passes later.

---

# Debugging the Optimizer

One of the best debugging techniques is printing the tree before and after optimization.

Before

```text
Projection

      │

Projection

      │

Selection(TRUE)

      │

TableScan
```

After

```text
Projection

      │

TableScan
```

Visualizing tree transformations makes optimization bugs much easier to understand.

---

# Why This Is Called Logical Optimization

Notice that our optimizer still produces

```text
Projection

      │

Selection

      │

TableScan
```

It never chooses

- Sequential Scan
- Index Scan
- Hash Join
- Merge Join

Those are **physical operators**.

Our optimizer works exclusively with **logical operators**.

That is why it belongs entirely to the compiler frontend.

---

# Complete Frontend Pipeline

At this point,

our compiler performs

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
Optimized Logical Query Plan
```

This is the complete logical SQL compiler frontend.

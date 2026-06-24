# Database Normalization

Before we learn **how** to normalize a database, we need to understand **why** normalization exists.

Imagine you're designing a database for a company. You want to store employee information, department information, phone numbers, job titles, and more.

One approach would be to put everything into a single large table:

| EmployeeID | EmployeeName | Phone | Department | Manager |
|------------|-------------|--------|------------|----------|
| 1001 | Gloria | 555-1111 | Sales | Jay |
| 1002 | Manny | 555-2222 | Sales | Jay |
| 1003 | Alex | 555-3333 | IT | Mitchell |

At first this seems simple. However, as the database grows, problems begin to appear:

- Information gets duplicated.
- Updating data becomes difficult.
- Deleting data may accidentally remove important information.
- Inserting new information may become impossible without entering unrelated data.

Database normalization was developed to solve these problems.

---

## What is Database Normalization?

**Database normalization is the process of organizing data into well-structured tables so that each piece of information is stored in the most appropriate place and unnecessary duplication is minimized.**

The goal is not simply to create more tables.

The goal is to create a database that:

- Stores data efficiently
- Maintains consistency
- Reduces duplication
- Prevents data integrity problems
- Makes future updates easier

---

## Goals of Normalization

Normalization has two primary goals:

### 1. Reduce Redundancy

Redundancy means storing the same information multiple times.

Example:

| Employee | Phone |
|----------|--------|
| Gloria | 555-1111 |
| Gloria | 555-1111 |
| Gloria | 555-1111 |

The phone number is duplicated three times.

If Gloria changes her phone number, every copy must be updated.

---

### 2. Prevent Data Anomalies

Normalization helps prevent:

- Insertion anomalies
- Deletion anomalies
- Update anomalies

These anomalies are a major motivation for normalization and are covered extensively in your notes.
---

## Normal Forms

Normalization is performed through a series of stages called **Normal Forms**.

The stages covered in your course are:

| Normal Form | Purpose |
|-------------|---------|
| 1NF | Eliminate non-atomic values |
| 2NF | Eliminate partial dependencies |
| 3NF | Eliminate transitive dependencies |
| 4NF | Eliminate multivalued dependencies |

Each level builds upon the previous one.

```text
Unnormalized Data
        ↓
      1NF
        ↓
      2NF
        ↓
      3NF
        ↓
      4NF
```


# Insertion, Deletion, and Update Anomalies

Now that we understand why normalization exists, we can examine the specific problems that normalization is designed to prevent.

These problems are called **anomalies**.

An anomaly is an undesirable side effect that occurs when data is poorly organized within a database.

The three most common anomalies are:

1. Insertion Anomaly
2. Deletion Anomaly
3. Update Anomaly

To understand them, consider the following table:

| EmployeeID | EmployeeName | Phone | Title |
|------------|-------------|---------|----------|
| 1001 | Gloria | 555-1111 | Manager |
| 1002 | Manny | 555-2222 | Engineer |
| 1003 | Cameron | 555-3333 | Associate |

At first glance, this table seems reasonable. However, it can create several problems.

---

# Insertion Anomaly

An insertion anomaly occurs when we cannot add information to the database without also adding unrelated information.

Suppose the company creates a new job title:

```text
Senior Engineer
```

However, no employee currently holds that title.

Where would we store it?

Our table only stores titles as part of employee records.

This means we cannot add the title unless we first create an employee.

In other words:

```text
Cannot insert title information
without employee information.
```

This is an insertion anomaly.

---

## Another Example

Suppose Claire has been hired.

| EmployeeID | EmployeeName | Phone | Title |
|------------|-------------|---------|----------|
| 1004 | Claire | 555-4444 | ? |

Claire is still in training and has not yet been assigned a title.

If the Title column cannot contain NULL values, we cannot insert Claire into the table.

Again, we are forced to provide information that we do not yet have.

---

# Deletion Anomaly

A deletion anomaly occurs when deleting one piece of data unintentionally deletes other valuable information.

Consider this table:

| EmployeeID | EmployeeName | Title |
|------------|-------------|----------|
| 1001 | Gloria | Manager |
| 1002 | Manny | Engineer |
| 1003 | Cameron | Associate |

Suppose Cameron leaves the company.

We delete his record:

```sql
DELETE FROM Employees
WHERE EmployeeID = 1003;
```

Now the table becomes:

| EmployeeID | EmployeeName | Title |
|------------|-------------|----------|
| 1001 | Gloria | Manager |
| 1002 | Manny | Engineer |

What happened?

The title:

```text
Associate
```

has completely disappeared from the database.

Even though the company may still recognize Associate as a valid title, we no longer have any record of it.

Deleting an employee caused us to lose title information.

This is a deletion anomaly.

---

# Update Anomaly

An update anomaly occurs when the same piece of information appears multiple times and must be updated in several places.

Consider this table:

| EmployeeID | EmployeeName | Phone |
|------------|-------------|---------|
| 1001 | Gloria | 555-1111 |
| 1001 | Gloria | 555-1111 |
| 1001 | Gloria | 555-1111 |

Suppose Gloria changes her phone number:

```text
555-1111 → 555-9999
```

Every occurrence must be updated.

If we update only two rows:

| EmployeeID | EmployeeName | Phone |
|------------|-------------|---------|
| 1001 | Gloria | 555-9999 |
| 1001 | Gloria | 555-9999 |
| 1001 | Gloria | 555-1111 |

The database now contains conflicting information.

Which phone number is correct?

We cannot tell.

This inconsistency is an update anomaly.

---

# Why Do These Anomalies Occur?

All three anomalies are usually caused by the same underlying problem:

```text
Too much information is stored
in the same table.
```

When unrelated facts are combined together:

- Inserting becomes difficult.
- Deleting causes data loss.
- Updating causes inconsistencies.

---

# Functional, Partial, Transitive, and Multivalued Dependencies

Before learning the Normal Forms, we need to understand the types of dependencies that each Normal Form is designed to eliminate.

Think of normalization as a sequence of improvements:

```text
1NF → Atomic Values
2NF → Remove Partial Dependencies
3NF → Remove Transitive Dependencies
4NF → Remove Multivalued Dependencies
```

Each Normal Form builds upon the previous one.

---

# Functional Dependency

A functional dependency exists when one attribute uniquely determines another attribute.

Notation:

```text
A → B
```

Read as:

```text
A determines B
```

---

## Example

Consider the table:

| StudentID | StudentName |
|------------|-------------|
| 1001 | Alice |
| 1002 | Bob |
| 1003 | Charlie |

Knowing a student's ID tells us exactly one student name.

```text
StudentID → StudentName
```

This is a functional dependency.

---

## Important Idea

The left side must uniquely determine the right side.

Valid:

```text
StudentID → StudentName
```

Not Valid:

```text
StudentName → StudentID
```

because multiple students could potentially have the same name.

---

# Partial Dependency

A partial dependency occurs when a non-key attribute depends on only part of a composite primary key.

---

## Example

Consider:

| StudentID | ProjectID | StudentName | ProjectName |
|------------|------------|-------------|-------------|
| 1 | 101 | Alice | Database App |
| 2 | 101 | Bob | Database App |
| 1 | 102 | Alice | Robotics App |

Primary Key:

```text
(StudentID, ProjectID)
```

This is called a composite key.

---

### Problem

StudentName depends only on StudentID:

```text
StudentID → StudentName
```

ProjectName depends only on ProjectID:

```text
ProjectID → ProjectName
```

Neither depends on the entire composite key.

Therefore:

```text
Partial Dependency Exists
```

---

## Solution

Split the table:

```text
Students
----------------
StudentID
StudentName

Projects
----------------
ProjectID
ProjectName

StudentProjects
----------------
StudentID
ProjectID
```

The partial dependencies disappear.

---

# Transitive Dependency

A transitive dependency occurs when one non-key attribute depends on another non-key attribute.

General form:

```text
A → B
B → C

Therefore:

A → C
```

---

## Example

| BookID | BookTitle | Author | Nationality |
|---------|-----------|---------|-------------|
| 1 | Ender's Game | Orson Scott Card | American |

---

### Dependencies

```text
BookID → Author
Author → Nationality
```

Therefore:

```text
BookID → Nationality
```

Nationality depends indirectly on BookID through Author.

This is a transitive dependency.

---

## Problem

If an author's nationality changes or is corrected:

```text
American → Canadian
```

Every book by that author must be updated.

This creates redundancy.

---

## Solution

Split the table:

```text
Authors
-----------------
AuthorID
AuthorName
Nationality

Books
-----------------
BookID
Title
AuthorID
```

Now nationality is stored once.

---

# Multivalued Dependency

A multivalued dependency occurs when two independent attributes both depend on the same key.

---

## Example

Suppose we have:

| BikeModel | ManufacturingYear | Color |
|------------|------------------|--------|
| MountainX | 2024 | Red |
| MountainX | 2024 | Blue |
| MountainX | 2025 | Red |
| MountainX | 2025 | Blue |

---

### Dependencies

```text
BikeModel → ManufacturingYear
BikeModel → Color
```

The years and colors are independent.

A color does not determine a year.

A year does not determine a color.

Yet both depend on BikeModel.

This is a multivalued dependency.

---

## Problem

The table produces unnecessary combinations:

```text
2024 + Red
2024 + Blue
2025 + Red
2025 + Blue
```

The amount of duplicated data grows rapidly.

---

## Solution

Split into separate tables:

```text
BikeYears
------------------
BikeModel
Year

BikeColors
------------------
BikeModel
Color
```

The multivalued dependency is eliminated.

---

# The Normal Forms

Now we can understand what each Normal Form is trying to achieve.

---

# First Normal Form (1NF)

## Goal

Eliminate non-atomic values.

---

## Conditions

A table is in 1NF if:

1. Each row is uniquely identifiable.
2. Each column stores a single value.
3. Values are atomic (cannot be broken down further).
4. Each column contains the same type of data.

---

### Violates 1NF

| StudentID | Courses |
|------------|---------|
| 1 | Math, Physics, CS |

Multiple values exist in one cell.

---

### Fixed

| StudentID | Course |
|------------|--------|
| 1 | Math |
| 1 | Physics |
| 1 | CS |

---

# Second Normal Form (2NF)

## Goal

Eliminate partial dependencies.

---

## Conditions

A table is in 2NF if:

1. It is already in 1NF.
2. Every non-key attribute depends on the entire primary key.

---

### Violates 2NF

```text
(StudentID, ProjectID)
```

but:

```text
StudentID → StudentName
```

Partial dependency exists.

---

### Fixed

Separate Students and Projects into their own tables.

---

# Third Normal Form (3NF)

## Goal

Eliminate transitive dependencies.

---

## Conditions

A table is in 3NF if:

1. It is already in 2NF.
2. No non-key attribute depends on another non-key attribute.

---

### Violates 3NF

```text
BookID → Author
Author → Nationality
```

Nationality depends indirectly on BookID.

---

### Fixed

Move Author information into its own table.

---

# Fourth Normal Form (4NF)

## Goal

Eliminate multivalued dependencies.

---

## Conditions

A table is in 4NF if:

1. It is already in 3NF.
2. It contains no multivalued dependencies.

---

### Violates 4NF

```text
BikeModel → Color
BikeModel → ManufacturingYear
```

Both attributes independently depend on BikeModel.

---

### Fixed

Separate the independent attributes into their own tables.


# Example: Taking a Database from Unnormalized Form to 4NF

Let's build a complete example that demonstrates every normalization step.

Suppose a video game store keeps the following table:

| SaleID | CustomerName | CustomerPhone | GameTitle | Publisher | Platform | StoreLocation |
|---------|-------------|----------------|-----------|------------|----------|---------------|
| 1 | Alice | 555-1111 | Minecraft | Mojang | PC | NYC |
| 1 | Alice | 555-1111 | Minecraft | Mojang | Xbox | NYC |
| 1 | Alice | 555-1111 | Terraria | Re-Logic | PC | NYC |
| 2 | Bob | 555-2222 | Minecraft | Mojang | PC | Boston |

Problems already visible:

- Customer information is duplicated.
- Publisher information is duplicated.
- Multiple platforms create repeated rows.
- Different facts are mixed together.

---

# Step 0: Unnormalized Form (UNF)

Suppose the store originally stored platforms as a list:

| SaleID | CustomerName | GameTitle | Platforms |
|---------|-------------|-----------|------------|
| 1 | Alice | Minecraft | PC, Xbox |
| 2 | Bob | Terraria | PC |

This violates 1NF.

Why?

```text
Platforms = PC, Xbox
```

contains multiple values.

The value is not atomic.

---

# Step 1: Convert to First Normal Form (1NF)

## Rule

All values must be atomic.

---

Split the platform list:

| SaleID | CustomerName | GameTitle | Platform |
|---------|-------------|-----------|----------|
| 1 | Alice | Minecraft | PC |
| 1 | Alice | Minecraft | Xbox |
| 2 | Bob | Terraria | PC |

Now every cell contains exactly one value.

We have reached:

```text
1NF
```

---

# Step 2: Identify the Key

Assume:

```text
(SaleID, GameTitle, Platform)
```

uniquely identifies a row.

This is a composite key.

---

Current table:

| SaleID | CustomerName | CustomerPhone | GameTitle | Publisher | Platform |
|---------|-------------|---------------|-----------|-----------|----------|
| 1 | Alice | 555-1111 | Minecraft | Mojang | PC |
| 1 | Alice | 555-1111 | Minecraft | Mojang | Xbox |
| 2 | Bob | 555-2222 | Terraria | Re-Logic | PC |

---

# Step 3: Check for Partial Dependencies

Notice:

```text
SaleID → CustomerName
SaleID → CustomerPhone
```

Customer information depends only on SaleID.

It does NOT depend on:

```text
(SaleID, GameTitle, Platform)
```

Similarly:

```text
GameTitle → Publisher
```

Publisher depends only on GameTitle.

---

These are:

```text
Partial Dependencies
```

which violate 2NF.

---

# Step 4: Convert to Second Normal Form (2NF)

Separate customer information:

## Sales

| SaleID | CustomerID |
|---------|-----------|
| 1 | 101 |
| 2 | 102 |

---

## Customers

| CustomerID | CustomerName | CustomerPhone |
|------------|-------------|---------------|
| 101 | Alice | 555-1111 |
| 102 | Bob | 555-2222 |

---

## SaleGames

| SaleID | GameTitle | Platform |
|---------|-----------|----------|
| 1 | Minecraft | PC |
| 1 | Minecraft | Xbox |
| 2 | Terraria | PC |

---

Still have:

```text
GameTitle → Publisher
```

which causes another problem.

---

# Step 5: Check for Transitive Dependencies

Current table:

| GameTitle | Publisher |
|-----------|-----------|
| Minecraft | Mojang |
| Terraria | Re-Logic |

Dependency:

```text
GameTitle → Publisher
```

Suppose Publisher also stores:

```text
Publisher → Headquarters
```

Then:

```text
GameTitle → Headquarters
```

through Publisher.

This is a:

```text
Transitive Dependency
```

which violates 3NF.

---

# Step 6: Convert to Third Normal Form (3NF)

Create a Publisher table.

---

## Publishers

| PublisherID | PublisherName | Headquarters |
|------------|---------------|--------------|
| 1 | Mojang | Sweden |
| 2 | Re-Logic | USA |

---

## Games

| GameID | GameTitle | PublisherID |
|---------|-----------|-------------|
| 1 | Minecraft | 1 |
| 2 | Terraria | 2 |

Now:

```text
Game → Publisher
Publisher → Headquarters
```

has been separated.

No transitive dependency remains.

We have reached:

```text
3NF
```

---

# Step 7: Check for Multivalued Dependencies

Suppose the store tracks:

| GameTitle | Platform | StoreLocation |
|-----------|----------|--------------|
| Minecraft | PC | NYC |
| Minecraft | Xbox | NYC |
| Minecraft | PC | Boston |
| Minecraft | Xbox | Boston |

Notice:

```text
GameTitle → Platform
GameTitle → StoreLocation
```

Platforms and store locations are independent.

The game can exist on many platforms.

The game can be sold in many stores.

Neither determines the other.

---

This is a:

```text
Multivalued Dependency
```

which violates 4NF.

---

# Why Is This Bad?

The database creates every possible combination:

```text
Minecraft + PC + NYC
Minecraft + Xbox + NYC
Minecraft + PC + Boston
Minecraft + Xbox + Boston
```

As more platforms and stores are added, the duplication explodes.

---

# Step 8: Convert to Fourth Normal Form (4NF)

Separate the independent relationships.

---

## GamePlatforms

| GameID | Platform |
|---------|----------|
| 1 | PC |
| 1 | Xbox |
| 2 | PC |

---

## GameStores

| GameID | StoreLocation |
|---------|--------------|
| 1 | NYC |
| 1 | Boston |
| 2 | Boston |

Now:

```text
GameID → Platform
```

is stored independently from:

```text
GameID → StoreLocation
```

No unnecessary combinations exist.

We have reached:

```text
4NF
```

---

# Final 4NF Schema

## Customers

| CustomerID | CustomerName | Phone |
|------------|-------------|--------|

---

## Sales

| SaleID | CustomerID |
|---------|-----------|

---

## Publishers

| PublisherID | PublisherName | Headquarters |
|------------|---------------|--------------|

---

## Games

| GameID | GameTitle | PublisherID |
|---------|-----------|-------------|

---

## SaleGames

| SaleID | GameID |
|---------|--------|

---

## GamePlatforms

| GameID | Platform |
|---------|----------|

---

## GameStores

| GameID | StoreLocation |
|---------|--------------|

---

# What Each Normal Form Fixed

| Step | Problem Removed |
|--------|----------------|
| 1NF | Non-atomic values |
| 2NF | Partial dependencies |
| 3NF | Transitive dependencies |
| 4NF | Multivalued dependencies |

This is the complete normalization path:

```text
UNF
 ↓
1NF
 ↓
2NF
 ↓
3NF
 ↓
4NF
```

where each step removes a specific type of dependency and produces a more organized database design.
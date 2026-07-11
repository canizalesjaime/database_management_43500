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
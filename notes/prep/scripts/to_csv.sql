SELECT * FROM salaries LIMIT 10;
SELECT * FROM salaries LIMIT 15;


-- going from psql to spreadsheet 
\COPY (SELECT id, name, created_at FROM my_table)
TO '/path/to/output.csv'
WITH CSV HEADER;


\o /path/to/output.txt   -- Start sending query output to file
SELECT * FROM my_table;
\o                    -- Turn output redirection off (back to screen)


-- going from csv to psql
CREATE TABLE my_table(
    col1 TEXT,
    col2 TEXT,
    col3 TEXT
);
\COPY my_table FROM '/path/to/file.csv' WITH CSV HEADER;

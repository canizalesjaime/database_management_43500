CREATE TABLE users (
    column1 TEXT,
    column2 INTEGER,
    column3 DATE
);

\COPY users FROM './users.csv' WITH (FORMAT csv, HEADER true)

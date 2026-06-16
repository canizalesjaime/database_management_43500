CREATE TABLE users (
    column1 TEXT,
    column2 INTEGER,
    column3 DATE
);


\copy users FROM '../data/users.csv' WITH (FORMAT csv, HEADER true)

#\i ./script1.sql

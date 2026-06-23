-- going from psql to spreadsheet 
\COPY (SELECT * FROM employees) TO './output.csv' WITH CSV HEADER;

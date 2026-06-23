SELECT * FROM salaries LIMIT 10;
SELECT * FROM salaries LIMIT 15;

\o ./output.txt   -- Start sending query output to file
SELECT * FROM salaries LIMIT 20;
\o                    -- Turn output redirection off (back to screen)

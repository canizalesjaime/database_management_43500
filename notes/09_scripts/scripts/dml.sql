-- Inserting rows into a table:
INSERT INTO departments VALUES
('d001','Marketing'),
('d002','Finance'),
('d003','Human Resources'),
('d004','Production'),
('d005','Development'),
('d006','Quality Management'),
('d007','Sales'),
('d008','Research'),
('d009','Customer Service');


-- UPDATE: modify data
-- directly overwrite the WHERE criteria specified
UPDATE departments SET department_no = 'd010' WHERE department_no = 'd009';


-- modify another column different from the WHERE criteria
UPDATE departments
SET dept_name = 'Test Test Department' WHERE department_no = 'd010';


-- update multiple column values that fulfill the same WHERE criteria
UPDATE departments SET department_no = 'd011', dept_name = 'Test Department' WHERE department_no = 'd010';


-- DELETE: deletes all rows (same as TRUNCATE)
-- DELETE FROM departments;


-- DELETE: specific rows based on WHERE criteria:
DELETE FROM departments WHERE department_no = 'd011' OR department_no = 'd009';


UPDATE departments
SET department_no = 'd2' WHERE dept_name = 'Finance';

UPDATE departments
SET department_no = 'd3' WHERE dept_name = 'Human Resources';
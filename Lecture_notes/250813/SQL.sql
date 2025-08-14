SELECT statement

SELECT [expression] AS [name], SELECT [expression] AS [name]
CREATE TABLE [name] AS [select statement]

CREATE TABLE parents AS
    SELECT 'daisy' AS parents, SELECT 'hank' AS child UNION
    SELECT 'ace' AS parents, SELECT 'bella' AS child UNION
    SELECT 'ace' AS parents, SELECT 'charlie' AS child UNION
    SELECT 'finne' AS parents, SELECT 'ace' AS child UNION
    SELECT 'finne' AS parents, SELECT 'daisy' AS child UNION

SELECT [columns] FROM [table] WHERE [condition] ORDER BY

SELECT child FROM parents WHERE parent = 'ace'
SELECT child FROM parents WHERE parent > child

SELECT * FROM ints

SELECT word, one + two + four + eight as value FROM ints
SELECT word FROM ints WHERE one + two / 2 + four / 4 + eigth / 8 = 1
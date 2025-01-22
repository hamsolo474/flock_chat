The error message you're encountering indicates that the variable `@table_name_col` is not recognized in the context where you're trying to use it. This typically happens when the variable is not declared in the correct scope or if there is a syntax issue.

In your code, the declaration of `@table_name_col` is correct, but the issue arises because the variable is being used inside a dynamic SQL string (`@sql`) without being properly concatenated. When you build the SQL string, the variable `@table_name_col` is not recognized inside the string because it is treated as a literal string rather than a variable.

To fix this, you need to ensure that the variable is concatenated correctly into the dynamic SQL string. Here’s the corrected version of your code:

```sql
DECLARE @sql NVARCHAR(MAX) = '';
DECLARE @table_name_col NVARCHAR(255);
DECLARE table_insert CURSOR FOR
SELECT TABLE_NAME
FROM WM7HIST.INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE 'DATOS_SRV_%_%_00' OR TABLE_NAME LIKE 'DATOS_LSRV_%_%_00' OR TABLE_NAME LIKE 'DATOS_VSRV_%_%_00' OR TABLE_NAME LIKE 'DATOS_WKS_%_%_00';
OPEN table_insert;
FETCH NEXT FROM table_insert INTO @table_name_col;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = @sql + '
        INSERT INTO DataWareHouse.dbo.Compliance (DEVICE_ID, ID_DATE, VALUE_TYPE, VALUE_ORIGINAL, ID_DATE_START, CPU_VALUES, MEMORY_VALUES, STORAGE_VALUES, AVALIABILTY )
        SELECT
            IDENTIF AS DEVICE_ID,
            FECHA as ID_DATE, VBLE_MODIFICADA as VALUE_TYPE, VALOR_VBLE as VALUE_ORIGINAL, FECHA_INSERT as ID_DATE_START,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%CPU%'' THEN VALOR_VBLE ELSE NULL END) AS CPU_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%Memory%'' THEN VALOR_VBLE ELSE NULL END) AS MEMORY_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%DiskUtilization%'' THEN VALOR_VBLE ELSE NULL END) AS STORAGE_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA = ''STATE'' THEN VALOR_VBLE ELSE NULL END) AS AVALIABILTY
        FROM WM7HIST.dbo.' + QUOTENAME(@table_name_col) + '
        GROUP BY IDENTIF, FECHA, VBLE_MODIFICADA, VALOR_VBLE, FECHA_INSERT;';

    FETCH NEXT FROM table_insert INTO @table_name_col;
END
CLOSE table_insert;
DEALLOCATE table_insert;

-- Execute the dynamic SQL
EXEC sp_executesql @sql;
```

### Key Changes:
1. **Corrected the condition for `AVALIABILTY`:** Changed `LIKE 'STATE'` to `= 'STATE'` since you are checking for an exact match.
2. **Ensure proper concatenation:** The variable `@table_name_col` is concatenated correctly into the dynamic SQL string using `QUOTENAME` to prevent SQL injection and handle special characters.

### Additional Note:
Make sure that the final SQL string in `@sql` is valid and does not contain any syntax errors before executing it. You can print the `@sql` variable before executing it to debug if needed:

```sql
PRINT @sql; -- This will help you see the final SQL statement being executed.
``` 

This should resolve the error you are encountering.
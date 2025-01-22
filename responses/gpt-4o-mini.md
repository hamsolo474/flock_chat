The error message you're encountering indicates that the variable `@table_name_col` is not recognized in the context where you're trying to use it. This is likely due to the scope of the variable within the cursor loop. 

In SQL Server, when you declare a variable, it is only available in the batch or scope where it is declared. In your case, the variable `@table_name_col` is declared outside the cursor loop, but it is being used inside the dynamic SQL string that is being built.

To fix this issue, you need to ensure that the variable is properly referenced within the dynamic SQL. You can achieve this by using `sp_executesql` to execute the dynamic SQL and passing the variable as a parameter. Here's how you can modify your code:

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
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''STATE'' THEN VALOR_VBLE ELSE NULL END) AS AVALIABILTY
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
1. **Dynamic SQL Execution**: The `EXEC sp_executesql @sql;` is called after the cursor loop, which is correct. However, ensure that the SQL string is built correctly.
2. **Variable Scope**: The variable `@table_name_col` is correctly used within the cursor loop, and its value is concatenated into the `@sql` string.

### Additional Considerations:
- Ensure that the dynamic SQL string is valid and does not contain any syntax errors.
- If you have a large number of tables, consider the potential size of the `@sql` variable and whether it might exceed the maximum length for NVARCHAR(MAX).
- If you need to debug, you can print the `@sql` variable before executing it to see the generated SQL statements.
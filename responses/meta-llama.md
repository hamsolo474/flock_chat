The error message indicates that the variable `@table_name_col` is not declared in the scope where it's being used. However, in your code, `@table_name_col` is declared at the beginning.

The issue is likely due to the fact that you're using a cursor to iterate over the table names, and the `EXEC sp_executesql @sql` statement is executed outside the scope of the cursor.

When you concatenate the SQL statements inside the cursor, the variable `@table_name_col` is not replaced with its actual value. Instead, the literal string `@table_name_col` is inserted into the SQL statement.

To fix this issue, you can use the `sp_executesql` statement inside the cursor loop, like this:

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
    SET @sql = '
        INSERT INTO DataWareHouse.dbo.Compliance (DEVICE_ID, ID_DATE, VALUE_TYPE, VALUE_ORIGINAL, ID_DATE_START, CPU_VALUES, MEMORY_VALUES, STORAGE_VALUES, AVALIABILTY )
        SELECT
            IDENTIF AS DEVICE_ID,
            FECHA as ID_DATE, VBLE_MODIFICADA as VALUE_TYPE, VALOR_VBLE as VALUE_ORIGINAL, FECHA_INSERT as ID_DATE_START,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%CPU%'' THEN VALOR_VBLE ELSE NULL END) AS CPU_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%Memory%'' then VALOR_VBLE ELSE NULL END) AS MEMORY_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%DiskUtilization%'' THEN VALOR_VBLE ELSE NULL END) AS STORAGE_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''STATE'' THEN VALOR_VBLE ELSE NULL END) AS AVALIABILTY
        FROM WM7HIST.dbo.' + QUOTENAME(@table_name_col) + '
        GROUP BY IDENTIF, FECHA, VBLE_MODIFICADA, VALOR_VBLE, FECHA_INSERT;';

    EXEC sp_executesql @sql;

    FETCH NEXT FROM table_insert INTO @table_name_col;
END
CLOSE table_insert;
DEALLOCATE table_insert;
```

In this revised code, the `sp_executesql` statement is executed inside the cursor loop, and the `@table_name_col` variable is replaced with its actual value for each iteration.
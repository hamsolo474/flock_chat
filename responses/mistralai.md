 The error message indicates that the variable `@table_name_col` is not declared in the scope where it is being used. The issue is caused by the fact that the variable `@table_name_col` is not declared before the FETCH NEXT statement inside the WHILE loop.

To fix this error, you need to declare the variable `@table_name_col` before the FETCH NEXT statement inside the WHILE loop. Here's the corrected code:
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
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%Memory%'' then VALOR_VBLE ELSE NULL END) AS MEMORY_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''%DiskUtilization%'' THEN VALOR_VBLE ELSE NULL END) AS STORAGE_VALUES,
            MAX(CASE WHEN VBLE_MODIFICADA LIKE ''STATE'' THEN VALOR_VBLE ELSE NULL END) AS AVALIABILTY
        FROM WM7HIST.dbo.' + QUOTENAME(@table_name_col) + '
        GROUP BY IDENTIF, FECHA, VBLE_MODIFICADA, VALOR_VBLE, FECHA_INSERT;';

    FETCH NEXT FROM table_insert INTO @table_name_col;
END

CLOSE table_insert;
DEALLOCATE table_insert;

EXEC sp_executesql @sql;
```
By declaring the variable `@table_name_col` before the FETCH NEXT statement inside the WHILE loop, you ensure that the variable is declared in the scope where it is being used. This should fix the error and allow the code to execute successfully.
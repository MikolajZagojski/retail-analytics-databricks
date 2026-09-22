-- Setup script for the retail analytics project.
-- Creates the catalog, medallion schemas (bronze, silver, gold) and a volume for raw CSV files.
-- If you cannot create catalogs, replace "dunnhumby" with an existing catalog, e.g. "workspace".

CREATE CATALOG IF NOT EXISTS dunnhumby
COMMENT 'Retail analytics project based on the Dunnhumby The Complete Journey dataset';

CREATE SCHEMA IF NOT EXISTS dunnhumby.bronze
COMMENT 'Raw layer: source CSV files and tables loaded 1:1, no transformations';

CREATE SCHEMA IF NOT EXISTS dunnhumby.silver
COMMENT 'Cleaned layer: correct data types, standardized column names, no duplicates';

CREATE SCHEMA IF NOT EXISTS dunnhumby.gold
COMMENT 'Business layer: aggregated tables and KPIs ready for dashboards and analysis';

CREATE VOLUME IF NOT EXISTS dunnhumby.bronze.raw_files
COMMENT 'Raw CSV files from the source dataset';
# Retail analytics on Databricks

A bronze, silver, gold pipeline on the Dunnhumby "The Complete Journey" dataset from [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey), built in Databricks Free Edition. The data is 8 CSV files with about 2.6 million transactions from roughly 2,500 households.

CSV files → Unity Catalog volume → bronze → silver → gold

## Where it stands

| Layer | Schema | Purpose | Status |
|---|---|---|---|
| Bronze | `dunnhumby.bronze` | CSVs loaded 1:1, no transformations | Done |
| Silver | `dunnhumby.silver` | Correct types, standardized names, no duplicates, quality rules | Next |
| Gold | `dunnhumby.gold` | Aggregated tables and KPIs | Later |

## Notes from the bronze layer

- Each CSV is loaded with `read_files` and `CREATE OR REPLACE TABLE`, so the notebook can be run again without cleaning up first.
- Each bronze table also has `_source_file` and `_ingested_at` columns, so every row can be traced back to the file and the load it came from.
- After loading I checked row counts, `_rescued_data` and NULLs. No table is empty, no rows were rescued and there are no NULLs at all. That still does not mean the data is complete: only 801 households have demographic data, so joins to that table have to be `LEFT JOIN`.
- Column names are inconsistent (some upper case, some lower case). I am leaving that for silver.

## Next steps

Silver will use Lakeflow Declarative Pipelines (Delta Live Tables) with expectations for the quality rules. After that come the gold tables.

## Files

```
notebooks/
  00_setup.sql            creates the catalog, schemas and the raw_files volume
  01_bronze_ingestion     loads the CSVs into bronze and runs the checks
utils/
  data_quality.py         row count, rescued data and NULL checks
```

Source files and their bronze tables:

| File | Table |
|---|---|
| transaction_data.csv | transaction_data |
| product.csv | product |
| hh_demographic.csv | household_demographic |
| campaign_desc.csv | campaign_descriptions |
| campaign_table.csv | campaign_table |
| coupon.csv | coupon |
| coupon_redempt.csv | coupon_redemptions |
| causal_data.csv | causal_data |

## Running it

1. Run `notebooks/00_setup.sql`.
2. Upload the CSV files to `dunnhumby.bronze.raw_files` (I downloaded them from Kaggle manually).
3. Run `notebooks/01_bronze_ingestion` from top to bottom.

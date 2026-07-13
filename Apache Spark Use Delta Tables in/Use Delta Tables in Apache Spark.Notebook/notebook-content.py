# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e5fd91e8-ba7b-43ae-9d7e-425859ab7f08",
# META       "default_lakehouse_name": "Lab4_LWH",
# META       "default_lakehouse_workspace_id": "2ea3fe4b-262d-4559-8edd-8cbfc230cf39",
# META       "known_lakehouses": [
# META         {
# META           "id": "e5fd91e8-ba7b-43ae-9d7e-425859ab7f08"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Delta Lake tables 
# Use this notebook to explore Delta Lake functionality 

# CELL ********************

from pyspark.sql.types import StructType, IntegerType, StringType, DoubleType

# define the schema
schema = StructType() \
.add("ProductID", IntegerType(), True) \
.add("ProductName", StringType(), True) \
.add("Category", StringType(), True) \
.add("ListPrice", DoubleType(), True)

df = spark.read.format("csv").option("header","true").schema(schema).load("Files/Use Delta Tables in Apache Spark/products.csv")
# df now is a Spark DataFrame containing CSV data from "Files/products/products.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # **Managed Vs External Table**

# CELL ********************

df.write.format("delta").saveAsTable("dbo.Managed_table")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").saveAsTable("external_table2",path="Files/externaltable2")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").saveAsTable("dbo.products_table")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC UPDATE dbo.products_table
# MAGIC SET ListPrice = ListPrice * 0.9
# MAGIC WHERE Category = 'Mountain Bikes';

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE HISTORY dbo.products_table;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT
# MAGIC     o.ProductName,
# MAGIC     o.ListPrice AS OriginalPrice,
# MAGIC     u.ListPrice AS UpdatedPrice
# MAGIC FROM dbo.products_table VERSION AS OF 0 o
# MAGIC JOIN dbo.products_table u ON o.ProductID = u.ProductID
# MAGIC WHERE o.Category = 'Mountain Bikes'
# MAGIC ORDER BY o.ProductName;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Use the default lakehouse catalog (single-part namespace) instead of a three-part name
# MAGIC -- The table dbo.products_table already exists in the default lakehouse, so we just reference it directly
# MAGIC 
# MAGIC SELECT 
# MAGIC     Category, 
# MAGIC     COUNT(*) AS NumProducts, 
# MAGIC     MIN(ListPrice) AS MinPrice, 
# MAGIC     MAX(ListPrice) AS MaxPrice, 
# MAGIC     AVG(ListPrice) AS AvgPrice
# MAGIC FROM dbo.products_table
# MAGIC GROUP BY Category;
# MAGIC 


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

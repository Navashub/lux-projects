
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, when, to_date
# import os
# from datetime import datetime

# def clean_and_transform():
#     spark = SparkSession.builder.appName("FoodPricesETL").getOrCreate()
    
#     # Read raw data (CSV from Kenya Open Data Portal)
#     input_file = f"data/raw/food_prices_{datetime.now().strftime('%Y%m')}.csv"
#     df = spark.read.csv(input_file, header=True, inferSchema=True)
    
#     # Clean and normalize
#     df = df.withColumn("price", col("price").cast("float")) \
#            .withColumn("date", to_date(col("date"), "yyyy-MM-dd")) \
#            .withColumn("price", when(col("price").isNull(), 0).otherwise(col("price"))) \
#            .withColumnRenamed("commodity", "product_name") \
#            .withColumnRenamed("location", "county_name")
    
#     # Save processed data
#     output_dir = "data/processed"
#     os.makedirs(output_dir, exist_ok=True)
#     df.write(f"{output_dir}/cleaned_food_prices.parquet", mode="overwrite")
    
#     return f"{output_dir}/cleaned_food_prices.parquet"



from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date
import os
from datetime import datetime

def clean_and_transform():
    try:
        spark = SparkSession.builder.appName("FoodPricesETL").getOrCreate()
        
        # Read raw data (CSV from WFP Food Prices for Kenya)
        input_file = f"data/raw/food_prices_{datetime.now().strftime('%Y%m')}.csv"
        print(f"Reading input file: {input_file}")
        df = spark.read.csv(input_file, header=True, inferSchema=True)
        
        # Clean and normalize
        df = df.withColumn("price", col("price").cast("float")) \
               .withColumn("date", to_date(col("date"), "yyyy-MM-dd")) \
               .withColumn("price", when(col("price").isNull(), 0).otherwise(col("price"))) \
               .withColumnRenamed("commodity", "product_name") \
               .withColumnRenamed("admin2", "county_name")
        
        # Save processed data
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/cleaned_food_prices.parquet"
        df.write(output_file, mode="overwrite")
        print(f"Cleaning successful! Processed data saved to {output_file}")
        
        return output_file
    except Exception as e:
        print(f"Error in clean_and_transform: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    clean_and_transform()
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import floor
import csv
import re
import itertools


class FileInsighs:

    @staticmethod
    def only_numbers_udf(x):
        num_regex = "^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$"
        if x is None or x == '':
            return True
        return bool(re.match(num_regex, x))

    @staticmethod
    def source_file_info(source_file_path):

        spark = SparkSession.builder.appName("PlaystoreInsights").getOrCreate()

        raw_df_spark = spark.read.csv(source_file_path, header=True)
        df_spark = raw_df_spark

        udf_number_check = F.udf(FileInsighs.only_numbers_udf, BooleanType())

        numeric_columns_to_append = []
        df_spark_count = df_spark.count()
        df_spark_columns = df_spark.columns
        for field in df_spark_columns:
            df_spark = df_spark.withColumn(
                field, udf_number_check(F.col(field)))

            true_count = df_spark.filter(F.col(field)).count()
            if true_count > 0.02 * df_spark_count:
                numeric_columns_to_append.append(field)

        return numeric_columns_to_append, raw_df_spark, df_spark_columns, df_spark_count

    @staticmethod
    def source_file_insights(field_list_to_combine, numeric_columns, data, binning_range, final_final_path):
        numerical_fields = numeric_columns
        for field in numerical_fields:
            # Assuming at least 20 unique values for binning
            unique_values = data.select(field).distinct().count()
            if unique_values >= 20:
                data = data.withColumn(f"{field}", floor(
                    data[field] / binning_range) * binning_range)

        # Define combinations of properties
        columns_of_interest = field_list_to_combine
        combinations = []
        for r in range(1, len(columns_of_interest) + 1):
            combinations.extend(itertools.combinations(columns_of_interest, r))

        # Generate insights
        insights = []

        for combo in combinations:
            group_by_columns = list(combo)
            counts = data.groupBy(*group_by_columns).count()
            total_count = data.count()
            filtered_counts = counts.filter(
                counts["count"] > total_count * 0.02)

            for row in filtered_counts.collect():
                insight_str = "; ".join(
                    f"{col}={row[col]}" for col in group_by_columns if col not in numerical_fields)

                # Format numerical fields to include ranges
                for field in numerical_fields:
                    if f"{field}" in row:
                        if insight_str:
                            insight_str += "; "
                        insight_str += f"{field}=[{row[f'{field}']}-{row[f'{field}']+binning_range}]"

                insights.append((insight_str, row["count"]))

        # Output to CSV
        output_file = final_final_path
        with open(output_file, "w", newline="") as csvfile:
            fieldnames = ["Insight", "Count"]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=",")

            writer.writeheader()
            for insight, count in insights:
                writer.writerow({"Insight": insight, "Count": count})
        return final_final_path


source_file_path = input(f'Enter your source file path: ')
numeric_cols, raw_data_dataframe, raw_data_columns, raw_data_count = FileInsighs.source_file_info(
    source_file_path)
print(f'source file columns: {raw_data_columns}')
cols_list_to_combine = list(map(str, input(
    f'\u2193 Enter the field names that should be used in combinations by comma seperation \u2193 \n').split(',')))
binning_range = int(input(f'Enter the binning range value: '))
final_final_path = input(
    f'Enter your output csv file path followed by filename: ')
final_file = FileInsighs.source_file_insights(
    field_list_to_combine=cols_list_to_combine, numeric_columns=numeric_cols, data=raw_data_dataframe, binning_range=binning_range, final_final_path=final_final_path)
print(
    f'Final csv with combinations {cols_list_to_combine} is generated at -> {final_final_path}')

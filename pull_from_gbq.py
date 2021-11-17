# ref: https://cloud.google.com/bigquery/docs/samples/bigquery-table-insert-rows-explicit-none-insert-ids#bigquery_table_insert_rows_explicit_none_insert_ids-python
# set credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"

from google.cloud import bigquery
import datetime

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of table to append to.
table_id = "big-data-6893-326823.roommate.apartments"

query = """
    SELECT *
    FROM `big-data-6893-326823.roommate.apartments`
    LIMIT 20
"""
query_job = client.query(query)  # Make an API request.

# list of dict
query_data = [dict(row.items()) for row in query_job]
print(query_data)

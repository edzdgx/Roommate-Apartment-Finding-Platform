# ref: https://cloud.google.com/bigquery/docs/samples/bigquery-table-insert-rows-explicit-none-insert-ids#bigquery_table_insert_rows_explicit_none_insert_ids-python
# set credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/big-data-6893-326823-15d1e60fd014.json"

from google.cloud import bigquery
import datetime

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of table to append to.
table_id = "big-data-6893-326823.roommate.users"

rows_to_insert = [
    {
    'roommatesRecommendation': 'test',
    'apartmentRecommendation': 'test',
    'firstName': 'test',
    'lastName': 'test',
    'uni': 'test',
    'gender': 'test',
    'nationality': 'test',
    'email': 'test',
    'school': 'test',
    'major': 'test',
    'smoking': 'test',
    'alcohol': 'test',
    'certainApartment': 'test',
    'apartment': 'test',
    'distance': 'test',
    'roomType': 'test',
    'roommate': 'test',
    'number': 'test',
    'sameMajor': 'test',
    'sameGender': 'test',
    'time': 'test'
    }
]

errors = client.insert_rows_json(
    table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
)  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))




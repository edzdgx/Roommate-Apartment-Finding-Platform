# ref: https://cloud.google.com/bigquery/docs/samples/bigquery-create-table
# set credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/edz/.ssh/big-data-6893-326823-15d1e60fd014.json"

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "big-data-6893-326823.roommate.users"

schema = [
    bigquery.SchemaField('roommatesRecommendation', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('apartmentRecommendation', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('firstName', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('lastName', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('uni', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('gender', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('nationality', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('email', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('school', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('major', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('smoking', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('alcohol', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('certainApartment', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('apartment', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('distance', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('roomType', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('roommate', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('number', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('sameMajor', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('sameGender', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('time', 'STRING', mode='NULLABLE')
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)




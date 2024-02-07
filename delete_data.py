import mysql.connector

# Function to drop a table
def drop_table(connection, table_name):
    try:
        cursor = connection.cursor()
        drop_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_query)
        connection.commit()
        print(f"Table '{table_name}' dropped successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Connect to the jobs database
try:
    jobs_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="jobs"
    )
except mysql.connector.Error as err:
    print(f"Error connecting to jobs database: {err}")
    exit(1)

# Tables to drop
tables_to_drop = ["parallel_jobs", "simple_jobs"]

# Drop tables in the jobs database
for table in tables_to_drop[:2]:
    drop_table(jobs_connection, table)

# Close connections
jobs_connection.close()

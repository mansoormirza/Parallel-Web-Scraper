import mysql.connector

def table_exists(cursor, table_name):
    # Execute the SHOW TABLES query
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")

    # Check if the table exists
    return cursor.fetchone() is not None

def display_table_data(table_name):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='jobs'
    )

    cursor = conn.cursor()

    # Check if the table exists
    if not table_exists(cursor, table_name):
        print(f"Table '{table_name}' doesn't exist in the database.")
        # Close the database connection
        conn.close()
        return

    # Select all data from the specified table
    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Display the table data
    print(f"\nData in table '{table_name}':")
    for row in rows:
        print(f"ID: {row[0]}\nCompany_Name: {row[1]}\nRequired_Skills: {row[2]}\nMore_Info: {row[3]}")
        print("-" * 50)

    # Close the database connection
    conn.close()


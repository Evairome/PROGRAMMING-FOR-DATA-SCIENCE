import mariadb

first_100_inserts = "SELECT * FROM reading LIMIT 100;"

try:
    with mariadb.connect(
        host="localhost", port=3306, user="root", password=""
    ) as connect:

        # Creating the cursor object to execute queries
        cursor = connect.cursor()

        # Selecting the pollution-db2
        cursor.execute("USE `pollution-db2`;")
        # This executes an sql command using the cursor object created
        cursor.execute(first_100_inserts)

        # Saving the result of the query to a variable
        result = cursor.fetchall()

except mariadb.Error as error:
    print(f"Error connecting to the database: {error}")


with open("insert-100.sql", "w") as file:
    for row in result:
        file.write(str(row))
        file.write("\n")  # A new line character to aid with formatting the output
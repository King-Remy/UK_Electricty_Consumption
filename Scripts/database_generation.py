import sqlite3 as sq

# Query the DB and return all records
def show_all():

    # COnnect to database
    conn = sq.connect('energy.sqlite')

    # Create cursor
    c = conn.cursor()

    # Query the Database
    c.execute("SELECT * FROM UKEnergy WHERE Postcode LIKE 'CV%'")

    UKEnergy = [
            dict(id=row[0], Postcode=row[1], Mean_consumption=row[2], Median_consumption=row[3], Longitude=row[4], Latitude=row[5])
            for row in c.fetchall()
        ]

    for item in UKEnergy:
        return item


    # COmmit our command
    conn.commit()

    # Close our command
    conn.close()
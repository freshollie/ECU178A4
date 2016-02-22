def init():
    import sqlite3 as sql
    import os

    try:
        os.remove('items.sqlite')
    except:
        print("Ignore this message.")

    connection = sql.connect('items.sqlite')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE items (name, type, price, weight)''')

    itemFile = open('itemsraw.txt')

    for iteration, line in enumerate(itemFile):
        if not(line.startswith("#")):
            try:
                iformat = line.strip("\n").split(", ")
                
                name = str(iformat[0])
                itype = str(iformat[1])
                price = int(iformat[2])
                weight = float(iformat[3])
                
                cursor.execute('''INSERT INTO items (name, type, price, weight) VALUES (?, ?, ?, ?)''', (name, itype, price, weight))
            except:
                print("An error exists on line " + str(iteration + 1) + ".")
                print("Please make sure it is in the following format:")
                print("Name (String), Type (String), Price (Integer), Weight (Float).")
            
    connection.commit()

    cursor.execute('''SELECT count(*) FROM items''')

    print(str(cursor.fetchone()[0]) + " items added to the database.")

    if True:
        print("\nDatabase:")
    
        cursor.execute('''SELECT * FROM items''')

        for row in cursor:
            print(' - %s, %s, %s, %s' % row)

    connection.close()


if __name__ == '__main__':
    init()

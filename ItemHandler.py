import sqlite3 as sql

__items = []
__categories = []

class Item:
    
    itemTotal = 0

    def __init__(self, name, itype, price, weight):
        self.name = str(name)
        self.itype = str(itype)
        self.price = int(price)
        self.weight = float(weight)
        self.quantity = 0
        Item.itemTotal += 1

    def __str__(self):
        return("%s, %s, %s, %s" % (self.name, self.itype, self.price, self.weight))

    def __getitem__(self, key):
        if key == 0 or key > 4 or key < 0:
            return self.name
        elif key == 1:
            return self.itype
        elif key == 2:
            return self.price
        elif key == 3:
            return self.weight
        elif key == 4:
            return self.quantity

def getItemsSorted(ifilter, reverse):
    return sorted(__items, key = lambda x: (x[ifilter]), reverse = reverse)

def getCategories():
    return __categories[:]

def getItemsFromCategory(itype):
    items = []

    for item in __items:
        if item.itype == itype:
            items.append(item)

    return items


def init(debug):
    if debug:
        print("Creating item list from database...")
    
    connection = sql.connect('items.sqlite')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM items''')

    iterations = 0

    for row in cursor:
        iterations += 1
        try:
            x = Item(row[0], row[1], row[2], row[3])
            __items.append(x)
            if row[1] not in __categories:
                __categories.append(row[1])

        except:
            if debug:
                print("The database contains an error on row " + str(iterations) + ".")
                print("Please make sure it is in the following format:")
                print("Name (String), Item Type (String), Price (Integer), Weight (Float). \n")
            
    connection.close()
    
    if debug:
        for item in getItemsSorted(0, False):
            print(" - " + str(item))

        print(str(Item.itemTotal) + " items added in total.")

if __name__ == '__main__':
    init(True)

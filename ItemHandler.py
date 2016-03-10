import sqlite3 as sql

__items = []

class Item:
    
    itemTotal = 0

    def __init__(self, name, itype, price, weight):
        self.name = str(name)
        self.itype = str(itype)
        self.price = int(price)
        self.weight = float(weight)
        Item.itemTotal += 1

    def __str__(self):
        return("%s (%s) [%s Gold, %sg]" % (self.name, self.itype, self.price, self.weight))

    def __getitem__(self, key):
        """Returns an attribute for the given key (0: Name, 1: Type, 2: Price, 3: Weight)."""
        if key == 1:
            return self.itype
        elif key == 2:
            return self.price
        elif key == 3:
            return self.weight
        else:
            return self.name
        

def getItemsSorted(ifilter, **kwargs):
    """Returns a list of items sorted by the given filter.

    Arguments:
    ifilter -- The filter used to sort the item list.

    Keyword Arguments:
    items -- The item list to sort (default: __items)
    reverse -- Should the order of the returned list be reversed? (default: false)
    """
    return sorted(kwargs['items'] if 'items' in kwargs else __items, key = lambda item: item[ifilter], reverse = kwargs['reverse'] if 'reverse' in kwargs else False)

def getItemsWhere(ifilter, equivalent, **kwargs):
    """Returns a list of items found in the given filter.

    Arguments:
    ifilter -- The filter used to search the item list.
    equivalent -- The search value.

    Keyword Arguments:
    items -- The item list to search (default: __items)
    reverse -- Should the order of the returned list be reversed? (default: false)
    """
    return sorted([item for item in (kwargs['items'] if 'items' in kwargs else __items) if equivalent in item[ifilter]], key = lambda item: item[0], reverse = kwargs['reverse'] if 'reverse' in kwargs else False)

def getCategories(**kwargs):
    """Returns a list of the categories present in the main item list.

    Keyword Arguments:
    items -- The item list categories should be returned from (default: __items)
    """
    return sorted(set([item[1] for item in (kwargs['items'] if 'items' in kwargs else __items)]))

def init(debug):
    if debug:
        print("Creating item list from database...")
    
    connection = sql.connect('items.sqlite')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM items''')

    for iterations, row in enumerate(cursor):
        try:
            x = Item(row[0], row[1], row[2], row[3])
            __items.append(x)
        except:
            if debug:
                print("The database contains an error on row " + str(iterations + 1) + ".")
                print("Please make sure it is in the following format:")
                print("Name (String), Item Type (String), Price (Integer), Weight (Float). \n")
            
    connection.close()
    
    if debug:
        for item in getItemsSorted(0):
            print(" - " + str(item))

        print(str(Item.itemTotal) + " items added in total.")

        
if __name__ == '__main__':
    init(True)

import ItemHandler
import sys
from tkinter import *

class Gui(Tk):
    
    __typeNames = ('Name', 'Type', 'Price', 'Weight', 'Quantity')
    __orderNames = ('Ascending', 'Descending')

    def __init__(self, items):
        self.sortType = 0
        self.sortOrder = 0
        self.searchText = ''
        self.items = items
        
        Tk.__init__(self)
        self.title('Results Screen')
        self.geometry('700x500')
        
        self.mainFrame = Frame(self, borderwidth = 5)
        self.mainFrame.pack(side = LEFT, fill = BOTH, expand = True)
        
        self.shoppingListTitle = Label(self.mainFrame, text = 'Results')
        self.shoppingListTitle.pack(fill = BOTH)
        
        self.shoppingListText = Text(self.mainFrame, state = 'disable', width = 20)
        self.shoppingListText.pack(fill = BOTH, expand = True)
        
        self.sortButton = Button(self.mainFrame, command = lambda: self.changeSort())
        self.sortButton.pack(fill = BOTH, expand = True)
        
        self.updateShoppingList()

    def changeSort(self):
        top = Toplevel()
        top.title('Sort')
        top.minsize(width = 100, height = 100)
        top.focus_force()

        self.sortTypeButton = Button(top, text = Gui.__typeNames[self.sortType], command = lambda: self.changeSortType())
        self.sortOrderButton = Button(top, text = Gui.__orderNames[self.sortOrder], command = lambda: self.changeSortOrder())
        
        self.sortTypeButton.pack(fill = BOTH, expand = True)
        self.sortOrderButton.pack(fill = BOTH, expand = True)

    def changeSortType(self):
        if self.sortType == len(Gui.__typeNames) - 1:
            self.sortType = 0
        else:
            self.sortType += 1
            
        self.sortTypeButton['text'] = Gui.__typeNames[self.sortType]
        
        self.updateShoppingList()
        
    def changeSortOrder(self):
        self.sortOrder = not(self.sortOrder)
        self.sortOrderButton['text'] = Gui.__orderNames[self.sortOrder]
        
        self.updateShoppingList()

    def updateShoppingList(self):
        #self.shoppingListTitle['text'] = 'Shopping List (%sg/50.0g)' % (round(50.0, 1))
        self.shoppingListText['state'] = 'normal'
        
        self.shoppingListText.delete('1.0', END)
        
        for item in ItemHandler.getItemsSorted(self.sortType, items = self.items, reverse = self.sortOrder):
            self.shoppingListText.insert('end', str(items[item]) + ' x ' + str(item) + '\n')
            
        self.shoppingListText['state'] = 'disable'
        
        self.sortButton['text'] = 'Sort (%s, %s)' % (Gui.__typeNames[self.sortType], Gui.__orderNames[self.sortOrder])

def main(items):
    Gui(items).mainloop()

if __name__ == '__main__':
    ItemHandler.init(False)
    a = ItemHandler.getItemsSorted(0)
    items = {a[1]: 2, a[4]: 5, a[24]: 1}
    main(items)

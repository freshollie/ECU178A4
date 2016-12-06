import ItemHandler
try:
    import Main
except ImportError:
    print('Main.py not found.')

try:
    import GuiResults
except ImportError:
    print('GuiResults.py not found')

import sys
from tkinter import *

class Gui(Tk):
    
    __typeNames = ('Name', 'Type', 'Price', 'Weight', 'Quantity')
    __orderNames = ('Ascending', 'Descending')
    
    def __init__(self):
        self.sortType = 0
        self.sortOrder = 0
        self.searchText = ''
        self.itemIndex = 0
        self.shoppingList = {}
        self.shoppingListWeight = 0
        
        Tk.__init__(self)
        self.title('Shopping List')
        self.geometry('700x500')

        self.mainFrame = Frame(self, borderwidth = 5)
        self.mainFrame.pack(side = LEFT, fill = BOTH, expand = True)

        self.shoppingListFrame = Frame(self)
        self.shoppingListFrame.pack(side = LEFT, fill = BOTH, expand = True)

        self.sortButton = Button(self.mainFrame, height = 3)
        self.sortButton.pack(fill = BOTH)

        self.topFrame = Frame(self.mainFrame)
        self.midFrame = Frame(self.mainFrame)
        self.botFrame = Frame(self.mainFrame)
        
        self.topFrame.pack(fill = BOTH, expand = True)
        self.midFrame.pack(fill = BOTH, expand = True)
        self.botFrame.pack(fill = BOTH, expand = True)
        
        self.navigationFrame = Frame(self.mainFrame, borderwidth = 10)
        self.navigationFrame.pack(fill = BOTH)

        self.navigationButtonMinus = Button(self.navigationFrame, height = 2)
        self.navigationButtonPlus = Button(self.navigationFrame, height = 2)
        
        self.navigationButtonMinus.pack(side = LEFT, fill = BOTH, expand = True)
        self.navigationButtonPlus.pack(side = LEFT, fill = BOTH, expand = True)

        self.shoppingListTitle = Label(self.shoppingListFrame, text = 'Shopping List (0.0g/150.0g)')
        self.shoppingListTitle.pack(fill = BOTH)

        self.shoppingListText = Text(self.shoppingListFrame, state = 'disable', width = 20)
        self.shoppingListText.pack(fill = BOTH, expand = True)

        self.startSimulationButton = Button(self.shoppingListFrame, text = 'Start Simulation', command = self.runSimulation)
        self.startSimulationButton.pack(fill = BOTH)

        self.frameDisplay(0)

    def frameDisplay(self, x):
        for widget in self.topFrame.winfo_children():
            widget.pack_forget()
        for widget in self.midFrame.winfo_children():
            widget.pack_forget()
        for widget in self.botFrame.winfo_children():
            widget.pack_forget()

        if type(x) == ItemHandler.Item:
            self.sortButton['text'] = 'Back to Item List'
            self.sortButton['command'] = lambda: self.frameDisplay(0)
            
            namel = Label(self.midFrame, text = 'Name: ' + x.name, font = ('', 16))
            typel = Label(self.midFrame, text = 'Type: ' + x.itype, font = ('', 16))
            pricel = Label(self.midFrame, text = 'Price: ' + str(x.price), font = ('', 16))
            weightl = Label(self.midFrame, text = 'Weight: ' + str(x.weight), font = ('', 16))
            
            if x in self.shoppingList:
                quantityl = Label(self.midFrame, text = 'In Shopping List: ' + str(self.shoppingList[x]), font = ('Purisa', 16))
            else:
                quantityl = Label(self.midFrame, text = 'In Shopping List: 0', font = ('Purisa', 16))
                
            namel.pack(fill = BOTH, expand = True)
            typel.pack(fill = BOTH, expand = True)
            pricel.pack(fill = BOTH, expand = True)
            weightl.pack(fill = BOTH, expand = True)
            quantityl.pack(fill = BOTH, expand = True)
            
            self.navigationButtonMinus['text'] = '-'
            self.navigationButtonPlus['text'] = '+'

            if x not in self.shoppingList:
                self.navigationButtonMinus['state'] = 'disable'
            else:
                self.navigationButtonMinus['state'] = 'normal'
            
            if self.shoppingListWeight + x.weight > 150.0:
                self.navigationButtonPlus['state'] = 'disable'
            else:
                self.navigationButtonPlus['state'] = 'normal'
                
            self.navigationButtonMinus['command'] = lambda item = x: self.removeFromShoppingList(item, 1)
            self.navigationButtonPlus['command'] = lambda item = x: self.addToShoppingList(item, 1)
        elif x == 1 or x > 1:
            self.sortButton['text'] = 'Back to Item List'
            self.sortButton['command'] = lambda: self.frameDisplay(0)
            
            self.sortTypeButton = Button(self.midFrame)
            self.sortOrderButton = Button(self.botFrame)
            
            self.sortTypeButton['text'] = Gui.__typeNames[self.sortType]
            self.sortTypeButton['command'] = command = lambda: self.changeSortType()
            
            self.sortOrderButton['text'] = Gui.__orderNames[self.sortOrder]
            self.sortOrderButton['command'] = command = lambda: self.changeSortOrder()
            
            self.sortTypeButton.pack(fill = BOTH, expand = True)
            self.sortOrderButton.pack(fill = BOTH, expand = True)
            
            self.navigationButtonMinus['state'] = 'disable'
            self.navigationButtonPlus['state'] = 'disable'
        elif x == 0:
            self.sortButton['text'] = 'Sort (%s, %s)' % (Gui.__typeNames[self.sortType], Gui.__orderNames[self.sortOrder])
            self.sortButton['command'] = lambda: self.frameDisplay(1)

            filteredItems = [x for x in self.shoppingList] if self.sortType == 4 else ItemHandler.getItemsSorted(self.sortType, reverse = self.sortOrder)

            frames = (self.topFrame, self.midFrame, self.botFrame)
            
            for i in range(9):
                try:
                    item = filteredItems[i + self.itemIndex]
                    
                    button = Button(frames[int(i / 3)], width = 3)
                    button['text'] = item.name
                    button['command'] = lambda item = item: self.frameDisplay(item)
                    
                    if item in self.shoppingList:
                        button['foreground'] = '#0080ff'
                    else:
                        button['foreground'] = 'black'
                        
                    button.pack(side = LEFT, fill = BOTH, expand = True)

                except(IndexError):
                    button = Button(frames[int(i / 3)], text = '?', width = 3)
                    button['state'] = 'disable'
                    button.pack(side = LEFT, fill = BOTH, expand = True)

            self.navigationButtonMinus['text'] = '<'
            self.navigationButtonPlus['text'] = '>'
            
            self.navigationButtonMinus['command'] = lambda: self.previousPage()
            self.navigationButtonPlus['command'] = lambda: self.nextPage()

            if self.itemIndex == 0:
                self.navigationButtonMinus['state'] = 'disable'
            else:
                self.navigationButtonMinus['state'] = 'normal'
                
            if self.itemIndex >= len(filteredItems) - 9:
                self.navigationButtonPlus['state'] = 'disable'
            else:
                self.navigationButtonPlus['state'] = 'normal'

    def nextPage(self):
        self.itemIndex += 9
        self.frameDisplay(0)
        
    def previousPage(self):
        self.itemIndex -= 9
        self.frameDisplay(0)
            
    def changeSortType(self):
        if self.sortType == len(Gui.__typeNames) - 1:
            self.sortType = 0
        else:
            self.sortType += 1
            
        self.sortTypeButton['text'] = Gui.__typeNames[self.sortType]
        
        self.itemIndex = 0

    def runSimulation(self):
        results = Main.main(self.shoppingList)
        GuiResults.main(results)

        
    def changeSortOrder(self):
        self.sortOrder = not(self.sortOrder)
        self.sortOrderButton['text'] = Gui.__orderNames[self.sortOrder]
        
        self.itemIndex = 0

    def addToShoppingList(self, item, amount):
        if item in self.shoppingList:
            self.shoppingList[item] += 1
        else:
            self.shoppingList[item] = 1
            
        self.shoppingListWeight += item.weight
        
        self.navigationButtonMinus['state'] = 'normal'
        
        self.updateShoppingList()
        self.frameDisplay(item)

    def removeFromShoppingList(self, item, amount):
        self.shoppingList[item] -= amount
        self.shoppingListWeight -= item.weight * amount
        
        if self.shoppingList[item] < 1:
            self.shoppingList.pop(item)
            
        self.updateShoppingList()
        self.frameDisplay(item)

    def updateShoppingList(self):
        self.shoppingListTitle['text'] = 'Shopping List (%sg/150.0g)' % (round(self.shoppingListWeight, 1))
        self.shoppingListText['state'] = 'normal'
        
        self.shoppingListText.delete('1.0', END)
        
        for item in sorted(self.shoppingList, key = lambda item: item[0]):
            self.shoppingListText.insert('end', str(self.shoppingList[item]) + ' x ' + item.name + '\n')
            
        self.shoppingListText['state'] = 'disable'
        
        
def main(*items):
    ItemHandler.init(False)
    Gui().mainloop()

if __name__ == '__main__':
    ItemHandler.init(False)
    sys.exit(main())

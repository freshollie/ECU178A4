from tkinter import *


root = Tk()

var = StringVar()
label = Label( root, textvariable=var, relief=RAISED )





""" For testing purpose"""
# Laptop = [100, 3]
# Mouse = [5, 0.3]
# GPU = [110, 0.9]
# USBstick = [10, 0.1]
# ScreenProtector = [2, 0]
# HDD = [20, 2]
# GameConsole = [100, 4]
# Keyboard = [10, 1]
""" For testing purpose"""





""" For testing purpose"""
# Products = [Laptop,Mouse,GPU,USBstick,ScreenProtector,HDD,GameConsole,Keyboard]
""" For testing purpose"""


def mergeSort(alist):
    print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    print("Merging ",alist)



""" For testing purpose"""
# alist = [Laptop,Mouse,GPU,USBstick,ScreenProtector,HDD,GameConsole,Keyboard]
""" For testing purpose"""




alist = [54,26,93,17,77,31,44,55,20]

mergeSort(alist)

print(alist)

var.set(alist)
label.pack()
root.mainloop()
def bubbleSort(list):
    n = len(list)
    swapped = False
    while swapped == False:
        print(list)
        swapped = True
        for i in range(1, len(list)):
            if list[i-1] > list[i]:
                a, b = list[i-1], list[i]
                list[i], list[i-1] = a, b
                swapped = False

aList = [1,6,1,7,3,7,46,26]

bubbleSort(aList)
print(aList)

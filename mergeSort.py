def merge(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(A):
    if len(A) < 2:
        return A
    middle = int(len(A) / 2)
    left = mergesort(A[:middle])
    right = mergesort(A[middle:])
    return merge(left, right)

#example sort
#asd = list(["Michael", "Anwar", "Lloyd", "Mark", "Marlon", "Ollie"])
#print(mergesort(asd))

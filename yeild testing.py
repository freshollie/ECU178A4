def reccurr(seq = []):
    for i in range(10):
        if len(seq)>10:
            yield seq[:]+[i]
        else:
            return reccurr(seq[:]+[i])


for i in reccurr():
    print(i)

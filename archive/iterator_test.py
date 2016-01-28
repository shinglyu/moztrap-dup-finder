import itertools

def y(max):
    x = itertools.combinations(range(max), 2)
    return ((xi[0]*10, xi[1]*10 ) for xi in x)

it = y(10)
#print(it)
#while(it):
    #arr = []
    #try:
        #for i in range(10):
            #arr.append(next(it))
    #except StopIteration:
        #print(arr)
        #break
    #print(arr)
#
#while(it):
#    print(list(itertools.islice(it, 0, 10)))
#    import time
#    time.sleep(1)

def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

for chunk in grouper(10, it):
    print(chunk)


from backports.functools_lru_cache import lru_cache
#from cachetools import cached
import time

#@cached(cache={})
class HDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))

def hashable_dict_args(f):
    def cached(*args, **kargs):
        return f(*map(lambda x:HDict(x), args), **kargs)
    return cached

def lru_dict_args(f):
    @hashable_dict_args
    @lru_cache()
    def cached(*args, **kargs):
        return f(*args, **kargs)
    return cached


#@lru_cache()
#@hashable_dict_args
#@lru_cache()
@lru_dict_args
def expensive_computation(x):
    time.sleep(1)
    print(type(x))
    return x['num']*5

if __name__ == "__main__":
    for times in range(3):
        for i in range(3):
            t = time.time()
            expensive_computation({'num':i})
            print("elapsed " + str(time.time() - t))


def log(func):
    def wrapper(*args,**kw):
        print('call %s'%func.__name__)
        return func(*args,**kw)
    return wrapper
@log
def now(arg1,arg2):
    print('2020/8/1',arg1,arg2)
now('Lisa','jisoo')
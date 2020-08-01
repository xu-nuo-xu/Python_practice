# 装饰器(decorator)
```python
#返回函数
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f = lazy_sum(1, 3, 5, 7, 9)     #without output
f()     #output：25
```
>在介绍装饰器前，我们需要先回顾一下返回函数的内容，如下所示，`lazy_sum` 函数的返回值是一个函数，因此单独执行`lazy_sum`不会有结果，在执行中用 `f` 接受 `lazy_sum` 的返回值，执行 `f` 相当于执行了 `sum` 函数。现在我们来看下面装饰器的内容。
```python
#装饰器
def log(func):
    def wrapper(*args,**kw):
        print('call %s'%func.__name__)
        return func(*args,**kw)
    return wrapper
@log
def now(arg1,arg2):
    print('2020/8/1',arg1,arg2)
now('first','second')
'''
output:
call now
2020/8/1 first second
'''
```
>在 `log` 函数中的返回值是一个函数，因此执行 `log` 并不会有结果，而其中的 `wrapper` 函数，才是真正需要执行的函数，而 `@log` 下面定义函数 `def now(arg1,arg2)` ，相当于执行了 `now = log(now)` ，也就是说现在的 `now` 名字是一个变量接收 `log` 函数的返回值，也就是 `now` 这个名字，现在指向的是 `log` 函数返回值 `wrapper` 函数，于是我们执行 `now('first','second')`，相当于执行了 `wrapper('first','second')`。不过我们看到，这里 `log` 函数的参数也是一个函数，并且我们再执行 `now = log(now)` 也就是 `@log` 时，将 `now` 函数传递了进去。注意，这里的 `now` 是一个函数，而不是一个变量。<br>这下我们捋一下执行顺序：首先 `@log` 相当于 `now = log(now)` 现在 `now` 变量指向 `wrapper` 函数，执行 `now('first','second')`，相当于 `wrapper('first','second')`，于是打印 `print('call %s'%func.__name__)` 得到 `call now` 的输出，之后 `return func(*args,**kw)`，返回到 `now` 函数中执行 `print('2020/8/1',arg1,arg2)` 得到输出 `2020/8/1 first second`

>如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：
```python
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log('execute')
def now():
    print('2015-3-25')
now()
'''
output:
execute now():
2015-3-25
'''
```
>我们分析一下这个执行过程，首先`@log('execute')`下面定义`now`函数，就相当于`now=log('execute')(now)`，也就是`now`这个变量现在指向 `wrapper` 函数，因为`decorator`函数的返回值是`wrapper`函数。而传进去的`now`参数作为`decorator`的参数，是属于函数而不是变量。此时，我们如果执行 `now.__name__ `结果一定是`'wrapper'`而不是`now`，因为这个名字已经指向了`wrapper`函数。但其实我们希望这里 `now.__name__` 还是 `'now'`，于是就需要借助Python内置的`functools.wraps`工具，于是一个完整的decorator的写法如下：
```python
import functools

def log(func):
    @functools.wraps(func)  #使得之后wrapper.__name__ = func.__name__
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
```
# type()函数创建类
>关于`type()`函数，正如我们之前见到过的，`type()`函数与`isinstance()`函数类似，都是用来看某一变量/常量的类型，其实`type()`函数还有一个用法，就是创建类。要创建一个`class`对象，`type()`函数依次传入3个参数：<br>
1.class的名称；<br>
2.继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；<br>
3.class的方法名称与函数绑定，这里我们把函数`sayhello`绑定到方法名`hello`上。<br>
如下面代码所示：
```python
def sayhello(self):
    print('hello hello!!')
Hello = type('Hello',(object,),dict(hello=sayhello))
h = Hello()
h.hello()
#output: hello hello!!
```
>这里的`sayhello`函数的self参数不能少，因为`sayhello`要作为`Hello`类的类方法，所以一定要有`self`参数。通过`type()`函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用`type()`函数创建出class。

>然后我要提一点的就是，我们如果执行以下代码：`print(type(Hello))`结果为：`<class 'type'>`。`print(type(h))` 结果为：`<class '__main__.Hello'>`。也就是定义的类的类型为 `type` 型，类的实例类型为相关的类类型，如 `class Hello` 型。
# 定制类
## \_\_slots__
>如果不加以限制，我们可以给一个类任意绑定属性，甚至给实例绑定方法：
```python
class Student(object):
    pass
s=Student()
s.name = 'Lisa'     #绑定属性
def set_age(self,age):
    self.age=age
from types import MethodType
s.set_age = MethodType(set_age,s)   #绑定方法
s.set_age(23)
print(s.age)    #output: 23

def set_height(self,height):
    self.height = height
Student.set_height=set_height
```
>这个是`types`模块的添加方法的函数`MethodType`，通过之前介绍我们也知道`type()`函数也可以直接创建类，顺便绑定函数。不同的是，`MethodType`绑定的方法是对一个实例进行的，对同类的其他实例不起作用。而我们如果要对一个类绑定方法，可以直接用等号，见上述代码最后三行。

>那么当我们需要限制实例属性时，就需要用到`__slots__`变量，它用tuple来接受允许我们绑定的属性的名称：
```python
class Student(object):
    __slots__ = ('age','height','set_age')
s=Student()
def set_age(self,age):
    self.age=age
from types import MethodType
s.set_age = MethodType(set_age,s)
s.set_age(23)
s.sex = 1   #Error

#output:AttributeError: 'Student' object has no attribute 'sex'
```
>`__slots__`只对当前类有限制，对子类没有限制，如上面例子如果有一个类继承了`Student`类，也可以绑定`sex`属性。除非子类也有相关的`__slots__`限制，这样子类能定义的除了自己的`__slots__`还有父类的`__slots__`

##@property
>我们知道面向对象可以用`set`和`get`方法来限制相关属性的修改、获取权限，修改内容范围来检查参数。但是，在调用时相比于直接赋值、直接查看写起来复杂一些。于是`@property`给我们了一个方法让我们在查看属性和修改属性时还按原来的方法:
```python
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
    @property
    def minus_score(self):
        return -self.score
        
s = Student()
s.score = 99    #直接设置属性并进行检查
print(s.score)  #直接访问属性
#output: 99
```
>在上面的代码中我们需要注意一点，两个`score`方法中，`self._score`前面的下划线不能去掉，因为去掉了的话，在执行时解释器会以为`self.score`是方法本身，进而变成了递归调用。要么就把方法改名，要么就把变量加上单下划线。`score/_score/__score`都是一个变量只不过访问权限不同。

>注意如果一个方法只有`@property`而没有相应的`@setter`就说明是只读属性，如上面的`minus_score`方法

##\_\_str__
>__str__方法的设置可以对类直接进行打印相关信息：
```python
class Student(object):
    def __init__(self, name):
         self.name = name
    def __str__(self):
         return 'Student object (name: %s)' % self.name
print(Student('Lisa'))

'''
output: Student object (name: Lisa)
if don't set the __str__ method the output gonna be:
<__main__.Student object at 0x000001DB1A3C65C0>
'''
```
## \_\_iter__与\_\_next__
>我们都知道`list，tuple`等都是可迭代对象，其实我们可以通过`__iter__与__next__`把类也变成可迭代对象：
```python
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 10: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
for n in Fib():
    print(n)

#output: 1 1 2 3 5 8
```
## \_\_getitem__
>我们更进一步，用`__getitem__`我们可以使得`Fib()`当作`list`使用，即可以通过索引访问：
```python
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
f=Fib()
print(f[12])

#output: 233

print(f[5:10])
#output TypeError: 'slice' object cannot be interpreted as an integer
```
>也就是说这样我们可以取到任意一个迭代值。但如果我们像list一样切片访问，就会报错，因为我们之前定义的`__getitem__`方法的`range(n)`的参数`n`只能是整数，现在传进来一个切片当然不行。我们可以对其方法进行改造：
```python
class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
f=Fib()
print(f[5:10])

#output: [8, 13, 21, 34, 55]
```
>但其实，如果要完善__getitem__还需要进行负数的错误处理等等，因此我们有时需要考虑更全面一些。
## \_\_getattr__
>正常情况下，我们在访问一个类没有绑定的属性时，会产生报错:
```python
class Student(object):

    def __init__(self):
        self.name = 'Michael'
s=Student()
print(s.age)

#output: AttributeError: 'Student' object has no attribute 'age'
```
>但是我们可以事先在`Student`类中，写一个`__getattr__`方法，用来对特殊未绑定属性进行动态绑定：
```python
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr=='score':
            return 99
        else:
            raise AttributeError('\'Student\' object has no attribute : %s' %attr)
s=Student()
print(s.score)    #output: 99
print(s.age)      #output: AttributeError: 'Student' object has no attribute : age
```
## \_\_call__
>我们都知道调用类的相关方法时，一般是创建一个类的实例，然后用`instance.method()`来调用，那么能不能直接用`instance()`即直接调用实例来完成一些操作，答案是可以的：
```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
s = Student('Michael')
s()     #output: My name is Michael.
```
>`__call__()`还可以定义参数。对实例进行直接调用就好比对一个函数进行调用一样，所以你完全可以把对象看成函数，把函数看成对象，因为这两者之间本来就没啥根本的区别。判定一个变量名是否可以调用：我们通过`callable()`函数，我们就可以判断一个对象是否是“可调用”对象:
```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
s = Student('Michael')
print(callable(s))          #output: True
print(callable(Student))    #output: True
```
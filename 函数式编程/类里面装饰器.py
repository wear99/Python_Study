# 类里面可以定义属性和方法。但属性是可以自由修改的，如果不想被修改就要加上方法get/set方法来中转。
# 使用装饰器可以更快捷的达到此目的：：：把一个方法变成同名属性，然后这个方法再来执行操作，返回指定的真正属性


class 学生(object):
    def __init__(self, name, age=20):  # 类的实例有_姓名，_年龄这2个属性，但会被任意修改，也无法检查传入的数据是否正确
        self.__姓名 = name
        self.__年龄 = age

    # 使用装饰器把 姓名 这个方法(函数) 转变成 属性了，这样当使用 .姓名时，实际只会return 实际的-姓名属性，无法进行修改。
    @property
    def 姓名(self):
        return self.__姓名

    @姓名.setter           # setter是个固定用法，当被赋值时就调用此setter。此外还有 .del ,当使用 del 命令时自动调用此装饰器
    def 姓名(self, name):
        self.__姓名 = name


a = 学生('孙')
print(a.姓名)
a.姓名 = 'sun'    # 当赋值时，自动调用 .setter 后对应的方法
print(a.姓名)  # 通过@property，把 姓名 这个方法转化成属性来使用了


# 另一种用法，property
class Foo(object):
    def __init__(self,s=''):
        self.__name=s

    def get_name(self):

        return 'get_name:'+self.__name

    def set_name(self, value):
        '''必须两个参数'''

        self.__name = value
        return 'set value:' + self.__name

    NAME = property(get_name, set_name)     #property后面依次为：fget,fset,fdel,doc；依次为取属性函数，赋值函数，删除函数，说明函数


obj = Foo()
print(obj.NAME)  # 调用get方法
obj.NAME = 'alex'  # 调用set方法
print(obj.NAME)

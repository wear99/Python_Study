# 摘要函数f()对任意长度的数据data计算出固定长度的摘要digest，目的是为了发现原始数据是否被人篡改过
# 对原始数据做一个bit的修改，都会导致计算出的摘要完全不同
# 摘要函数是一个单向函数,反推非常困难

import hashlib

md5 = hashlib.md5()
md5.update('123456'.encode('utf-8'))
print(md5.hexdigest())
# MD5是最常见的摘要算法，生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示

# 另一种常见的摘要算法是SHA1，调用SHA1和调用MD5完全类似

# 摘要算法用于存储一些敏感信息,比如密码,这样就避免被人直接得到.每次用户登录时通过对比md5码是否相同
# 由于常用口令的MD5值很容易被计算出来，所以，要确保存储的用户口令不是那些已经被计算出来的常用口令的MD5，
# 这一方法通过对原始口令加一个复杂字符串来实现，俗称“加盐”：
# 只要加入的 复杂字符串 不被黑客知道，即使用户输入简单口令，也很难通过MD5反推明文口令
# 还可以通过把用户名和密码组合在一起计算md5码

# 要注意摘要算法不是加密算法，不能用于加密（因为无法通过摘要反推明文），只能用于防篡改

print('**********练习**********')
import hashlib, random


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = get_md5(username + password)


db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}

m = db['michael']
print(m.salt)
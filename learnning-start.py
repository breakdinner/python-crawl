# -*- coding: utf-8 -*-

# 字符串变量
a = 'I\'m \n"OK"!\n'
b = "I'm \nOK!"
print(a, b)

# 不转义
d = r'\n\t'
print(d)

# 多行文本
c = '''
其实我也不清楚
你说的是不是
'''
print(c)

# 字符串中使用变量
name = 'break'
age = 26
var1 = 'my name is ' + name
var2 = 'I\'m %d' % age + 'years old'
var3 = 'Hello, {0}, 成绩提提成了 {1:.2f}%'.format('小明', 17.252)
print(var2)
print(var3)

# list, 有序
classmates = ['michael', 'bob', 'tracy']
classmates2 = classmates
# 追加元素
classmates2.append('stanford')
print(classmates2)
# 从后向前获取元素, 使用负数
print(classmates2[-3])
# 插入元素到指定位置
classmates2.insert(2, 'break')
print(classmates2)
# 从后删除元素pop, 如果要删除指定位置则pop(n)
classmates2.pop()
classmates2.pop(2)
print(classmates2)
# list嵌套
classmates2.append(classmates2)
print(classmates2)

# tuple 元组. 一旦定义, 不可改变. 这里的不可改变是相对所指向的位置而言.
classmates = ('michael', 'bob', 'tracy')
print(classmates)
# 如果只有一个元素且是数字, 则必须要后跟逗号来定义, 否则会被视作数学运算
number = (1, )
print(number)
# 一个"可变的'tuple案例
example = ('A', 'B', [1, 2], (3, ))
example[2][0] = 'W'
example[2][1] = 'Y'
example[2].append(555)
# ('A', 'B', ['W', 'Y']) 因为该tuple的第3个值最初定义指向的是一个list,list是可变的
# 我们改变的是这个list中的值
print(example)

# 标准输入
# print(input('请输入任意字符并回车:\n'))

# if条件
a = 1
b = 2
if a > b and a > 0:
    print(1)
elif b > 5:
    print(3)
else:
    print(2)

# 类型获取
a = '123'
b = int(a)
print(type(a), type(b))

# 循环
names = ['break heather', 'tender', 'land']
for name in names:
    print(name)                 # 原数据
    print(name.capitalize())    # 首字母大写
    print(name.title())         # 每个单词首字母都大写

sum = 0
n = 99
while n > 0:
    # 可以使用break和continue控制
    sum += n
    n -= 2
print('sum为{0}'.format(sum))

# range
a = list(range(10, 20, 2))
print(a)
for i in range(5, 20, 3):
    print(i)

# dict
d = {'name': 'break', 'age': 26}
print(d)
print('here is a boy called {0}, he is {1} years old'.format(d['name'], d['age']))
d['tools'] = 'bass'
print(d['tools'].title())
if 'name' in d:     # 判断d中是否有name
    print(d['name'])

print(d.get('what'))    # 不存在的键会返回None
print(d.get('name'))
d.pop('age')    # 删除age字段. 且dict的pop必须传参
print(d)

# set. 无重复元素
s1 = {1, 2, 7, 7, 2}   # 也可以用set([1, 2, 7])的方式定义, 但ide会出警告提示不建议使用
print(s1)
s1.add(88)       # 在开头增加元素.但set实际上没有顺序
print(s1)
s2 = {4, 2, 7}
s3 = {4, 5, 7}
print(s1 & s2)  # 取并集
print(s1 | s2)  # 取合集

# 不可变对象

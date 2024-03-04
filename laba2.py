#!/usr/bin/env python
# coding: utf-8

# # Лабораторная работа №2
# ## Вариант 15
# ### Мотякин Артем Андреевич СКБ211

# __15: Массив данных ЗАГСа:__ ФИО жениха, дата рождения жениха,  ФИО невесты, дата рождения невесты, дата бракосочетания,  номер ЗАГСа (сравнение по полям – номер ЗАГСа, дата  бракосочетания, ФИО жениха)<br>
# 
# __а) Сортировка выбором<br>
# г) Шейкер-сортировка<br>
# е) Быстрая сортировка__

# In[35]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from datetime import datetime, timedelta
import time
from math import log, sqrt


# In[19]:


arr_sizes = np.array([100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000])
table = pd.read_csv('Names.csv', sep=';', index_col=False, header=None)#csv где по 100 женских и мужских ФИО
arr_names_man = np.array(table[0])
arr_names_woman = np.array(table[1])


# In[24]:


#Сгенерируем 9 наборов данных следующих размерностей: 100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000
print("Generating data...\n")
for i in np.nditer(arr_sizes):
    name_groom = np.random.choice(arr_names_man, size=i)
    name_bride = np.random.choice(arr_names_woman, size=i)
    num_registry = np.random.randint(1, high=i+1, size=i)
    date_groom = []
    date_bride = [] 
    date_wedding = []
    
    for _ in range(i):
        start_date_birthday = datetime.strptime("01-01-1980", "%d-%m-%Y")
        end_date_birthday = datetime.strptime("01-01-2000", "%d-%m-%Y")

        start_date_wedding = datetime.strptime("01-01-2018", "%d-%m-%Y")
        end_date_wedding = datetime.strptime("01-01-2024", "%d-%m-%Y")

        days_birthday = (end_date_birthday - start_date_birthday).days
        days_wedding = (end_date_wedding - start_date_wedding).days

        date_groom.append((start_date_birthday + timedelta(days=np.random.randint(0, high=days_birthday))).strftime("%d-%m-%Y"))
        date_bride.append((start_date_birthday + timedelta(days=np.random.randint(0, high=days_birthday))).strftime("%d-%m-%Y"))
        date_wedding.append((start_date_wedding + timedelta(days=np.random.randint(0, high=days_wedding))).strftime("%d-%m-%Y"))
        
    print('Generating ', len(date_wedding), "done!")
    
    d = {"Groom fullname": name_groom,
           "Groom birth date": np.array(date_groom),
           "Bride fullname": name_bride,
           "Bride birth date": np.array(date_bride),
           "Wedding date": np.array(date_wedding),
           "Registry office number": num_registry}
    df = pd.DataFrame(data=d)
    df.to_csv(f"Data_{i}.csv")
    print('Saved ', len(date_wedding), "to csv!")


# In[53]:


class Obj:
    def __init__(self, arr):
        self.num_reg = int(arr[6])
        self.gr_fname = arr[1]
        self.date_w = datetime.strptime(arr[5], "%d-%m-%Y")
        self.date_gr = datetime.strptime(arr[2], "%d-%m-%Y")
        self.br_fname = arr[3]
        self.date_br = datetime.strptime(arr[4], "%d-%m-%Y")
        
    def __le__(self, other): # <=
        return (self.num_reg, self.gr_fname, self.date_w) <= (other.num_reg, other.gr_fname, other.date_w)
        
    def __ge__(self, other): # >=
        return (self.num_reg, self.gr_fname, self.date_w) >= (other.num_reg, other.gr_fname, other.date_w)
        
    def __lt__(self, other): # <
        return (self.num_reg, self.gr_fname, self.date_w) < (other.num_reg, other.gr_fname, other.date_w)
    
    def __gt__(self, other): # >
        return (self.num_reg, self.gr_fname, self.date_w) > (other.num_reg, other.gr_fname, other.date_w)
    
    def __eq__(self, other): # ==
        return (self.num_reg, self.gr_fname, self.date_w) == (other.num_reg, other.gr_fname, other.date_w)
    
    def pr(self): # вывод в консоль
        print(f"{self.gr_fname}, {self.date_gr}, {self.br_fname}, {self.date_br}, {self.date_w}, {self.num_reg}")
    
    
def SelectSort(arr):
    l = len(arr)
    for i in range(l): # i - current step
        k = i
        x = arr[i]
        for j in range(i+1, l): # loop for searching minimal element
            if Obj(arr[j]) < Obj(x):
                k = j
                x = arr[j]
        # swap minimal element and a[i]
        arr[k], arr[i] = arr[i], x


def ShakerSort(arr):
    k = len(arr) - 1
    ub = len(arr) - 1
    lb = 1
    while True:
        # from bottom to top passage 
        for j in reversed(range(1, ub+1)):
            if Obj(arr[j-1]) > Obj(arr[j]):
                arr[j-1], arr[j] = arr[j], arr[j-1]
                k = j
        lb = k+1
        
        # passage from top to bottom
        for j in range(lb, ub+1):
            if Obj(arr[j-1]) > Obj(arr[j]):
                arr[j-1], arr[j] = arr[j], arr[j-1]
                k = j
        ub = k-1
        if lb >= ub:
            break

            
def partition(arr, left, right):
    pivot = Obj(arr[right])
    sorted_idx = left - 1
    for j in range(left, right):
        if Obj(arr[j]) < pivot:
            sorted_idx += 1
            arr[sorted_idx], arr[j] = arr[j], arr[sorted_idx]
    arr[sorted_idx+1], arr[right] = arr[right], arr[sorted_idx+1]
    return sorted_idx + 1

def QuickSort(arr, left, right):
    if left < right:
        pivot = partition(arr, left, right)
        QuickSort(arr, left, pivot-1)
        QuickSort(arr, pivot+1, right)


# In[ ]:


print("Getting data...\n")
arr_select = []
arr_shaker = []
arr_quick = []
for i in np.nditer(arr_sizes):
    print(f"Computing {i}")
    df = pd.read_csv(f'Data_{i}.csv', index_col=False, header=None)
    arr1 = df.to_numpy().tolist()[1:]
    arr2 = df.to_numpy().tolist()[1:]
    arr3 = df.to_numpy().tolist()[1:]
    
    print(f"SelectSort {i}")
    start_time = time.time_ns() / 1000000 # time in milliseconds
    SelectSort(arr1)
    arr_select.append(time.time_ns() / 1000000 - start_time)
    df1 = pd.DataFrame(data=arr1)
    df1.to_csv(f"Data_SelectSort_{i}.csv")
    
    print(f"ShakerSort {i}")
    start_time = time.time_ns() / 1000000 # time in milliseconds
    ShakerSort(arr2)
    arr_shaker.append(time.time_ns() / 1000000 - start_time)
    df2 = pd.DataFrame(data=arr2)
    df2.to_csv(f"Data_ShakerSort_{i}.csv")
    
    print(f"QuickSort {i}")
    start_time = time.time_ns() / 1000000 # time in milliseconds
    QuickSort(arr3, 0, len(arr3)-1)
    arr_quick.append(time.time_ns() / 1000000 - start_time)
    df3 = pd.DataFrame(data=arr3)
    df3.to_csv(f"Data_QuickSort_{i}.csv")
    
    assert arr1==arr2
    assert arr1==arr3
    
print("Done!")


# In[12]:


plt.plot(arr_sizes, arr_select, label='SelectSort')
plt.plot(arr_sizes, arr_shaker, label='ShakerSort')
plt.plot(arr_sizes, arr_quick, label='QuickSort')
plt.xlabel('Size of Input Data')
plt.ylabel('Time (milliseconds)')
plt.legend()
plt.show()


# In[13]:


plt.plot(arr_sizes, [log(i) for i in arr_select], label='SelectSort')
plt.plot(arr_sizes, [log(i) for i in arr_shaker], label='ShakerSort')
plt.plot(arr_sizes, [log(i) for i in arr_quick], label='QuickSort')
plt.xlabel('Size of Input Data')
plt.ylabel('Ln() from Time (milliseconds)')
plt.xticks(arr_sizes, rotation=-65)
plt.xlim(arr_sizes[0], arr_sizes[-1])
plt.legend()
plt.show()


# # Лабораторная работа №2
# ## Вариант 15
# ### Мотякин Артем Андреевич СКБ211

# 1) Реализовать поиск заданного элемента в массиве  объектов по ключу в соответствии с вариантом (ключом является  первое НЕ числовое поле объекта) следующими методами:<br>
# с помощью __бинарного дерева поиска__<br>
# с помощью __красно-черного дерева__<br>
# с помощью __хэш таблицы__
# 2) Для хэш таблицы необходимо реализовать хэш функцию и метод разрешения коллизий. Подсчитать число коллизий хэш функции и построить график зависимости от размерности массива.
# 3) Выполнить поиск 7-10 раз на массивах разных размерностей от 100 и более (но не менее, чем до 100000). Засечь (программно) время поиска для  всех способов. По полученным точкам  построить сравнительные графики зависимости времени поиска от размерности  массива. 
# 4) Записать входные данные в ассоциативный массив multimap<key,  object> и сравнить время поиска по ключу в нем с временем поиска из п.3. Добавить данные по времени поиска в ассоциативном массиве в общее сравнение с остальными способами и построить график зависимости времени поиска от размерности массива.

# In[62]:


class BTreeNode: # бинарное дерево
    def __init__(self, value=None, content=None): # конструктор
        self.left = None
        self.right = None
        self.value = value
        self.content = content

    def insert(self, value, content=None): # вставка нового элемента
        if self.value is None:
            self.value = value
            self.content = content
        elif value < self.value:
            if self.left is None:
                self.left = BTreeNode(value, content)
            else:
                self.left.insert(value, content)
        else:
            if self.right is None:
                self.right = BTreeNode(value, content)
            else:
                self.right.insert(value, content)

    def traversal(self): # проходка и вывод дерева 
        if self.left:
            self.left.traversal()
        print(self.value, self.content)
        if self.right:
            self.right.traversal()

    def find(self, value): # поиск элемента по ключу
        if value < self.value:
            if self.left is None:
                raise Exception('error, node content is None')
            else:
                return self.left.find(value)
        elif value > self.value:
            if self.right is None:
                raise Exception('error, node content is None')
            else:
                return self.right.find(value)
        else:
            return self.content


class RBTreeNode: # чёрно-красное дерево (узел дерева)
    def __init__(self, val, content=None): # конструктор
        self.red = False
        self.parent = None
        self.val = val
        self.left = None
        self.right = None
        self.content = content


class RBTree: # чёрно-красное дерево (само дерево)
    def __init__(self): # конструктор
        self.nil = RBNode(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert(self, val, content=None): # вставка нового элемента
        new_node = RBTreeNode(val, content)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True
        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                return
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
        self.fix_insert(new_node)

    def fix_insert(self, new_node): # метод, который делает дерево черно-красным (приводит его к правильному виду)
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_left(new_node.parent.parent)
            else:
                u = new_node.parent.parent.right
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_right(new_node.parent.parent)
        self.root.red = False

    def exists(self, val): # поиск элемента
        curr = self.root
        while curr != self.nil and val != curr.val:
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        if curr.content is None:
            raise Exception('error, node content is None')
        else:
            return curr.content

    def rotate_left(self, x): # вращение влево
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x): # вращение вправо
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def __repr__(self): # перегрузка оператора вывода
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)


def print_tree(node, lines, level=0): # вывод дерева
    if node.val != 0:
        print_tree(node.left, lines, level + 1)
        print(node.val, node.content)
        print_tree(node.right, lines, level + 1)


class HashTable: #хэш таблица
    __collisions = 0 # количество коллизий

    def __init__(self, n=100): # конструктор
        self.MAX = n
        self.arr = [[] for i in range(self.MAX)]

    def __get_hash(self, key): # получить хэш
        h = 0
        for char in key:
            h += ord(char)
        return h % self.MAX

    def __setitem__(self, key, value): # добавить значение
        hsh = self.__get_hash(key)
        found = False
        for idx, element in enumerate(self.arr[hsh]):
            if len(element) == 2 and element[0] == key:
                if element[1] == value:
                    self.arr[hsh][idx] = (key, value)
                    found = True
                    break
        if not found and len(self.arr[hsh]) > 0:
            self.arr[hsh].append((key, value))
            self.__collisions += 1
        elif not found:
            self.arr[hsh].append((key, value))

    def __getitem__(self, key): # получить значение
        hsh = self.__get_hash(key)
        for element in self.arr[hsh]:
            if element[0] == key:
                return element[1]
        raise Exception(f"No {key} key in HashTable")

    def __delitem__(self, key): # удалить значение
        hsh = self.__get_hash(key)
        for idx, element in enumerate(self.arr[hsh]):
            if element[0] == key:
                del self.arr[hsh][idx]

    def get_collisions_number(self): # получить количество коллизий
        print('Количество коллизий: ', self.__collisions)
        return self.__collisions

    def pr(self): # вывод хэш таблицы
        for i in self.arr:
            print(i)


# In[63]:


print("Getting data...\n")
arr_btree = []
arr_rbtree = []
arr_htable = []
arr_multimap = []
for i in np.nditer(arr_sizes):
    print(f"Setting data {i}")
    df = pd.read_csv(f'Data_{i}.csv', index_col=False, header=None)
    arr = df.to_numpy().tolist()[1:]
    arr_btree.append(TreeNode())
    arr_rbtree.append(RBTree())
    arr_htable.append(HashTable(100))#len(df.index)
    arr_multimap.append(dict())
    for row in arr:
        obj = Obj(row) # создаём наш объект (из Лабораторной 1)
        arr_btree[-1].insert(value=row[1], content=obj)
        arr_rbtree[-1].insert(val=row[1], content=obj)
        arr_htable[-1][row[1]] = obj
        arr_multimap[-1][row[1]] = obj
print("\nCreating data structures done!\n")


# In[64]:


print("Start computing...\n")
arr_btree_time = []
arr_rbtree_time = []
arr_htable_time = []
arr_htable_collisions = []
arr_multimap_time = []
arr_names = ["Новиков Виктор Маркович", "Смирнов Лев Михайлович", "Данилов Владимир Егорович", "Горбачев Александр Тихонович", "Жуков Андрей Петрович", "Филатов Лука Андреевич", "Фетисов Кирилл Артемьевич"]

for i in range(len(arr_sizes)):
    times = 0
    for name in arr_names:
        start_time = time.time_ns() / 1000 # time in microseconds
        arr_btree[i].find(name).pr()
        times += time.time_ns() / 1000 - start_time 
    arr_btree_time.append(times / len(arr_names))
    print(f'Бинарное дерево (size {arr_sizes[i]}): ', arr_btree_time[-1])

    times = 0
    for name in arr_names:
        start_time = time.time_ns() / 1000 # time in microseconds
        arr_rbtree[i].exists(name).pr()
        times += time.time_ns() / 1000 - start_time 
    arr_rbtree_time.append(times / len(arr_names))
    print(f'Черно-красное дерево (size {arr_sizes[i]}): ', arr_rbtree_time[-1])

    times = 0
    for name in arr_names:
        start_time = time.time_ns() / 1000 # time in microseconds
        arr_htable[i][name].pr()
        times += time.time_ns() / 1000 - start_time 
    arr_htable_time.append(times / len(arr_names))
    print(f'Хеш-таблица (size {arr_sizes[i]})', arr_htable_time[-1])

    times = 0
    for name in arr_names:
        start_time = time.time_ns() / 1000 # time in microseconds
        arr_multimap[i][name].pr()
        times += time.time_ns() / 1000 - start_time 
    arr_multimap_time.append(times / len(arr_names))
    print(f'MultiMap (size {arr_sizes[i]}): ', arr_multimap_time[-1])

    arr_htable_collisions.append(arr_htable[i].get_collisions_number())
    print("\n\n\n")

print("\nComputing done!")


# In[65]:


plt.plot(arr_sizes, arr_btree_time, label='BTree')
plt.plot(arr_sizes, arr_rbtree_time, label='RBTree')
plt.plot(arr_sizes, arr_htable_time, label='HashTable')
plt.plot(arr_sizes, arr_multimap_time, label='MultiMap')
plt.xlabel('Size of Input Data')
plt.ylabel('Time (microseconds)')
plt.legend()
plt.show()


# In[67]:


plt.plot(arr_sizes, [log(i) for i in arr_btree_time], label='BTree')
plt.plot(arr_sizes, [log(i) for i in arr_rbtree_time], label='RBTree')
plt.plot(arr_sizes, [log(i) for i in arr_htable_time], label='HashTable')
plt.plot(arr_sizes, [log(i) for i in arr_multimap_time], label='MultiMap')
plt.xlabel('Size of Input Data')
plt.ylabel('Ln() from Time (microseconds)')
plt.xticks(arr_sizes, rotation=-65)
plt.xlim(arr_sizes[0], arr_sizes[-1])
plt.legend()
plt.show()


# In[66]:


plt.plot(arr_sizes, arr_htable_collisions, label='HashTable')
plt.xlabel('Size of Input Data')
plt.ylabel('Collisions amount')
plt.legend()
plt.show()


# In[ ]:





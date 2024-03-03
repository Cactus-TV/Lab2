#!/usr/bin/env python
# coding: utf-8

# # Лабораторная работа №2
# ### Мотякин Артем Андреевич СКБ211


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from datetime import datetime, timedelta
import time
from math import log, sqrt
import codecs


arr_sizes = np.array([100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000])
table = pd.read_csv('Names.csv', sep=';', index_col=False, header=None)#csv где по 100 женских и мужских ФИО
arr_names_man = np.array(table[0])
arr_names_woman = np.array(table[1])


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
    
    def pr(self): # вывод в консоль
        print(f"{self.gr_fname}, {self.date_gr}, {self.br_fname}, {self.date_br}, {self.date_w}, {self.num_reg}")
    

class TreeNode: # бинарное дерево
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
                self.left = TreeNode(value, content)
            else:
                self.left.insert(value, content)
        else:
            if self.right is None:
                self.right = TreeNode(value, content)
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


class RBNode: # чёрно-красное дерево (узел дерева)
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
        new_node = RBNode(val, content)
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


def print_tree(node, lines, level=0): # перегрузка
    if node.val != 0:
        print_tree(node.left, lines, level + 1)
        print(node.val, node.content)
        print_tree(node.right, lines, level + 1)


class HashTable: #хэш-таблица
    __collisions = 0

    def __init__(self, n=100):
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
        print('Количество коллизий: ',self.__collisions)

    def pr(self): # вывод таблицы
        for i in self.arr:
            print(i)


file = codecs.open('Data_20000.csv', 'r', 'utf_8_sig')
next(file)
row_counter = sum(1 for row in file)
file.seek(0)
next(file)
tree_1 = TreeNode()
rb_tree_1 = RBTree()
table_1 = HashTable(row_counter)
d = dict()
for row in file:
    r = row.split(",")
    w = Obj(r)
    tree_1.insert(value=r[1], content=w)
    rb_tree_1.insert(val=r[1], content=w)
    table_1[r[1]] = w
    d[r[1]] = w


start = time.time()
tree_1.find('Смирнов Лев Михайлович').pr()
end = time.time()
print('Бинарное дерево: ', end-start)

start = time.time()
rb_tree_1.exists('Смирнов Лев Михайлович').pr()
end = time.time()
print('Черно-красное дерево: ', end-start)

start = time.time()
table_1['Смирнов Лев Михайлович'].pr()
end = time.time()
print('Хеш-таблица', end-start)

start = time.time()
d['Смирнов Лев Михайлович'].pr()
end = time.time()
print('MultiMap: ', end-start)

table_1.get_collisions_number()
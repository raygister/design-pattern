#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/12
#
# 定义：观察者模式定义了对象之间的一对多依赖，当一个对象（主题）改变状态时，它的所有依赖者（观察者）都会收到通知并自动更新。
# 好处：提供了一种对象设计，让主题和观察者之间松耦合，降低对象之间的互相依赖（改变主题和观察者其中一方，并不影响另一方，只要它们之间的接口仍被遵守）。
# OO原则：松耦合设计，降低对象之间的互相依赖，以应对变化。


class Inventory(object):
    def __init__(self):
        self.observers = []
        self._product = None
        self._quantity = 0

    def register(self, observer):
        self.observers.append(observer)

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value
        self._update_observers()

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self._update_observers()

    def _update_observers(self):
        for observer in self.observers:
            observer()


class Observer(object):
    def __init__(self, inventory):
        self.inventory = inventory

    def __call__(self, *args, **kwargs):
        print(self.inventory.product)
        print(self.inventory.quantity)


def main():
    inv = Inventory()
    ob = Observer(inv)
    ob2 = Observer(inv)
    inv.register(ob)
    inv.register(ob2)

    print('inventory set product')
    inv.product = 'apple'
    print('inventory set quantity')
    inv.quantity = 233


if __name__ == '__main__':
    main()

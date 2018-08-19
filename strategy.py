#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/19
#
# 定义：策略模式将一系列可以互相替换的算法（接口一致），分别封装成为一个个策略类，然后使用委托的方法，决定使用哪一个行为（实现不同）。
#       一般包括上下文（策略委托者）、策略接口、策略实现。
# 好处：让算法可以独立于使用算法的客户而变化。
# OO原则：封装变化；多用组合少用继承；针对接口编程，不针对实现编程（各个具体策略类有一致的接口，只是接口的实现不同）。

from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name credit')


class LineItem(object):
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order(object):  # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        discount = 0
        if self.promotion:
            discount = self.promotion(self) if callable(self.promotion) else self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


# 传统实现：
class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """
        返回折扣金额
        Args:
            order:

        Returns:

        """


class CreditPromo(Promotion):
    """
    为积分在1000以上的顾客提供5%的折扣
    """
    def discount(self, order):
        return order.total() * 0.05 if order.customer.credit >= 1000 else 0


class BulkItemPromo(Promotion):
    """
    单个商品为20个或以上时提供10%的折扣
    """
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount


class LargeOrderPromo(Promotion):
    """
    订单中的不同商品达到10个以上时提供7%的折扣
    """
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0


# python实现：具体策略没有内部状态即实例属性，更像是函数，而python函数就是一等对象，还省了策略类实例化对象的运行时开销
def credit_promo(order):
    return order.total() * 0.05 if order.customer.credit >= 1000 else 0


def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    return 0


def best_promo(order):
    promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']
    return max(promo(order) for promo in promos)


if __name__ == '__main__':
    print('traditional strategy:')
    joe = Customer('Joe', 0)
    ann = Customer('Ann', 1100)
    cart = [LineItem('banana', 4, 0.5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]
    banana_cart = [LineItem('banana', 30, 0.5), LineItem('apple', 10, 1.5)]
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print('joe with no credit: {}'.format(Order(joe, cart, CreditPromo())))
    print('ann with 1100 credict: {}'.format(Order(ann, cart, CreditPromo())))
    print('joe with 30 banana: {}'.format(Order(joe, banana_cart, BulkItemPromo())))
    print('joe with 10 different item: {}'.format(Order(joe, long_order, LargeOrderPromo())))

    print('pythonic strategy:')
    print('joe with no credit: {}'.format(Order(joe, cart, credit_promo)))
    print('ann with 1100 credict: {}'.format(Order(ann, cart, credit_promo)))
    print('joe with 30 banana: {}'.format(Order(joe, banana_cart, bulk_item_promo)))
    print('joe with 10 different item: {}'.format(Order(joe, long_order, large_order_promo)))
    print('best promotion of joe with 10 different item: {}'.format(Order(joe, long_order, best_promo)))
    print('best promotion of joe with 30 banana: {}'.format(Order(joe, banana_cart, best_promo)))
    print('best promotion of ann with 1100 credict: {}'.format(Order(ann, cart, best_promo)))

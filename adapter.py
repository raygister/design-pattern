#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/26
#
# 定义：适配器模式将一个类的接口转换成客户期望的另一个接口。
# 好处：让客户从实现的接口解耦，不必为了应对不同的接口而跟着改变。


class Target(object):
    def request(self):
        print('normal request.')


class Adaptee(object):
    def specific_request(self):
        print('specific request.')


class Adapter(Target):
    def __init__(self):
        self.adaptee = Adaptee()

    def request(self):
        self.adaptee.specific_request()


if __name__ == '__main__':
    target = Adapter()
    target.request()

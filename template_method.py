#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/25
#
# 定义：模板方法模式在一个方法中定义了一个算法的骨架，而将一些步骤的实现延迟到子类中。
#       模板方法的抽象类可以定义具体方法、抽象方法和钩子（hook）。
# 好处：使得子类可以在不改变算法结构的情况下，重新定义算法中的某些步骤。
# OO原则：好莱坞原则，don't call us, we'll call you，别调用我（高层模块），我会调用你（低层模块），
#         即高层决定如何以及何时调用低层模块。
# 区分：策略模式和模板方法模式都封装算法，但前者用组合，后者用继承。工厂方法是模板方法的一种特殊版本。


class Person(object):
    def chew(self):
        raise NotImplementedError

    @staticmethod
    def swallow():
        print('Quick swallow.')

    def eat(self):
        self.chew()
        self.swallow()


class Man(Person):
    def chew(self):
        print("Men don't chew, just swallow.")


class Woman(Person):
    def chew(self):
        print('Ladies chew things carefully.')


if __name__ == '__main__':
    man = Man()
    man.eat()

    woman = Woman()
    woman.eat()

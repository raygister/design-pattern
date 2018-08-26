#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/26
#
# 定义：外观模式提供了一个统一的接口，用来访问子系统中的一群接口；定义了一个高层接口，让子系统更容易使用。实现一个外观，
#       需要将子系统组合进外观中，然后将工作委托给子系统执行。
# 好处：让客户从一个复杂的子系统中解耦。
# OO原则：最少知识原则，具体来说就是对象只应该调用属于以下范围的方法：①该对象本身；②传进来的对象；
#         ③此方法所创建或实例化的对象；④对象的组件


class Computer(object):
    def __init__(self):
        self.bios = Bios()
        self.kernal = Kernal()

    def start(self):
        self.bios.start()
        self.kernal.start()

    def stop(self):
        self.bios.stop()
        self.kernal.stop()


class Bios(object):
    def __init__(self):
        pass

    @staticmethod
    def start():
        print('Bios start.')

    @staticmethod
    def stop():
        print('Bios stop.')


class Kernal(object):
    def __init__(self):
        pass

    @staticmethod
    def start():
        print('Kernal start.')

    @staticmethod
    def stop():
        print('Kernal stop.')


if __name__ == '__main__':
    computer = Computer()
    computer.start()
    computer.stop()

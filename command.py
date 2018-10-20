#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/10/20

# 定义：命令模式将请求封装成（命令）对象，以便随心所欲地储存、传递和调用它们。命令模式可以用来实现队列（配合线程池）、
#       日志（添加store和load方法）和支持撤销操作等。
# 好处：将发出请求的对象（调用者）和执行请求的对象（接收者）解耦。
# 坏处：每增加一个单独的命令都要实现一个ConcreteCommand类。

from collections import defaultdict


WC_SLOT = 0
KITCHEN_SLOT = 1


# Receiver
class Light(object):
    def __init__(self, name):
        self.light = name

    def on(self):
        print(str(self.light) + ' light on')

    def off(self):
        print(str(self.light) + ' light off')


# Command Interface
class Command(object):
    def execute(self):
        raise NotImplementedError()

    def undo(self):
        pass


# Concrete Command
class NoCommand(Command):
    def execute(self):
        print('Command Not Found')

    def undo(self):
        print('Command Not Found')


class LightOnCmd(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class LightOffCmd(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()


# Invoker
class RemoteController(object):
    def __init__(self):
        self.on_command = defaultdict(lambda: NoCommand())
        self.off_command = defaultdict(lambda: NoCommand())
        self.previous_cmd = NoCommand()

    def set_command(self, slot, on_command, off_command):
        self.on_command[slot] = on_command
        self.off_command[slot] = off_command

    def on_button_pressed(self, slot):
        curr_cmd = self.on_command[slot]
        curr_cmd.execute()
        self.previous_cmd = curr_cmd

    def off_button_pressed(self, slot):
        curr_cmd = self.off_command[slot]
        curr_cmd.execute()
        self.previous_cmd = curr_cmd

    def undo_button_pressed(self):
        self.previous_cmd.undo()


if __name__ == '__main__':
    remote_ctrl = RemoteController()
    wc_light = Light('Washroom')
    kitchen_light = Light('Kitchen')

    wc_light_on = LightOnCmd(wc_light)
    wc_light_off = LightOffCmd(wc_light)
    kitchen_light_on = LightOnCmd(kitchen_light)
    kitchen_light_off = LightOffCmd(kitchen_light)

    remote_ctrl.set_command(WC_SLOT, wc_light_on, wc_light_off)
    remote_ctrl.set_command(KITCHEN_SLOT, kitchen_light_on, kitchen_light_off)

    remote_ctrl.on_button_pressed(WC_SLOT)
    remote_ctrl.off_button_pressed(WC_SLOT)
    remote_ctrl.undo_button_pressed()
    remote_ctrl.undo_button_pressed()
    remote_ctrl.on_button_pressed(KITCHEN_SLOT)
    remote_ctrl.off_button_pressed(KITCHEN_SLOT)
    remote_ctrl.undo_button_pressed()
    remote_ctrl.undo_button_pressed()

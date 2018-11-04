#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/25
#
# 定义：状态模式允许对象在内部状态改变时改变它的行为（不同状态中展现不同行为），表面上让对象看起来像是修改了它的类，
#       实际上就是封装基于状态的行为，并将行为委托到当前状态（状态转换可以由state或context类控制）。
# 好处：允许对象基于内部状态而拥有不同的行为，把可能的改变局部化到状态类中。
# 坏处：类数目增加。
# OO原则：同策略模式。
# 区分：状态模式和策略模式之间的不同在于，策略模式通常对其他策略对象没有意识，而状态模式的状态或上下文则需要知道
#       它们将会切换到什么样的状态（即任何状态改变都是定义好的）。


SOLD_OUT = 0
NO_QUARTER = 1
HAS_QUARTER = 2  # 被投入了25分钱
SOLD = 3


# Context
class GumballMachine(object):
    def __init__(self, count):
        self.state = SoldOutState(self)
        self.count = count
        if self.count > 0:
            self.state = NoQuarterState(self)

    # 将行为委托给状态
    def insert_quarter(self):
        self.state.insert_quarter()

    def eject_quarter(self):
        self.state.eject_quarter()

    def turn_crank(self):
        self.state.turn_crank()
        self.state.dispense()
    # end

    def release_ball(self):
        print('A gumball comes rolling out the slot...')
        if self.count != 0:
            self.count -= 1


# State Interface
class State(object):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine

    def insert_quarter(self):
        pass

    def eject_quarter(self):
        pass

    def turn_crank(self):
        pass

    def dispense(self):
        pass


# Concrete State
class HasQuarterState(State):
    def insert_quarter(self):
        print('Please consume your quarter before you insert another quarter.')

    def eject_quarter(self):
        print('Quarter returned.')
        self.gumball_machine.state = NoQuarterState(self.gumball_machine)

    def turn_crank(self):
        print('You turn the crank.')
        self.gumball_machine.state = SoldState(self.gumball_machine)

    def dispense(self):
        print('Not at this state, please wait a second.')


class SoldOutState(State):
    def insert_quarter(self):
        print('Please do not insert a quarter, the gumball is sold out.')

    def eject_quarter(self):
        print('You can not eject, you have not insert a quarter.')

    def turn_crank(self):
        print('You turn the crank, but there is no gumball.')

    def dispense(self):
        print('No gumball dispense.')


class NoQuarterState(State):
    def insert_quarter(self):
        print('You insert a quarter.')
        self.gumball_machine.state = HasQuarterState(self.gumball_machine)

    def eject_quarter(self):
        print('You can not eject, you have not insert a quarter.')

    def turn_crank(self):
        print('You turned the crank, there is no quarter.')

    def dispense(self):
        print('You need to pay first.')


class SoldState(State):
    def insert_quarter(self):
        print('Please wait, we are giving you a gumball.')

    def eject_quarter(self):
        print('Sorry, you already turned the crank.')

    def turn_crank(self):
        print('Turning the crank twice do not get you another gumball!')

    def dispense(self):
        self.gumball_machine.release_ball()
        if self.gumball_machine.count > 0:
            self.gumball_machine.state = NoQuarterState(self.gumball_machine)
        else:
            print('Oops, out of gumball.')
            self.gumball_machine.state = SoldOutState(self.gumball_machine)


if __name__ == '__main__':
    gumballMachine = GumballMachine(2)
    print(gumballMachine.count)
    print(gumballMachine.state)
    print("=====================================================")
    gumballMachine.insert_quarter()
    print(gumballMachine.state)
    gumballMachine.eject_quarter()
    gumballMachine.eject_quarter()
    gumballMachine.insert_quarter()
    print(gumballMachine.state)
    gumballMachine.turn_crank()
    print(gumballMachine.state)
    print(gumballMachine.count)
    gumballMachine.insert_quarter()
    gumballMachine.turn_crank()
    print(gumballMachine.state)
    print("=====================================================")
    gumballMachine.turn_crank()

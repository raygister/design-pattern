#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/8/12
#
# 装饰者模式动态地将责任附加到对象上（在所委托被装饰者的行为之前与/或之后加上自己的行为）。
# 好处：想要扩展功能，装饰者提供有别于继承地另一种选择。
# 坏处：装饰者会导致设计中出现许多小对象，如果过度使用，会让程序变得很复杂。

import time


def log_calls(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        print('calling {} with {} and {}'.format(
            func.__name__, args, kwargs))
        ret_val = func(*args, **kwargs)  # real execution here
        print('Executed {} in {}ms'.format(func.__name__, time.time() - now))
        return ret_val
    return wrapper


def test1(a, b):
    print('\ttest1 called')


@log_calls
def test2(a, b, name):
    print('\ttest2 called')
    time.sleep(1)


def main():
    logged_test1 = log_calls(test1)

    logged_test1(1, 2)
    print('pythonic decorated test2 called')
    test2(3, 4, name='ray')


if __name__ == '__main__':
    main()

#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/10/21
#
# 定义：组合模式允许你将对象组成树形结构来表现“整体/部分”的层次结构。组合能让客户以一致的方式处理个别对象和对象组合。
# 好处：允许客户对个别对象和组合对象一视同仁。
# 坏处：组合模式的实现有许多设计上的折衷，如：以单一职责原则换取透明性（元素是组合Composite还是叶节点Leaf对客户是透明的）。
# 使用场景：需要动态地透明地调用整体或者部分的功能接口。如Linux的树形文件系统。


# Component
class Company(object):
    def __init__(self, name):
        self.name = name

    def add(self, company):
        pass

    def remove(self, company):
        pass

    def display(self, depth):
        pass

    def list_duty(self):
        pass


# Composite
class ConcreteCompany(Company):
    def __init__(self, name):
        super().__init__(name)
        self.children_company = []

    def add(self, company):
        self.children_company.append(company)

    def remove(self, company):
        self.children_company.remove(company)

    def display(self, depth):
        print('\t' * depth, self.name)

        for company in self.children_company:
            company.display(depth + 1)

    def list_duty(self):
        # 迭代处理子节点，以达到透明性
        for company in self.children_company:
            company.list_duty()


# Leaf
class HrDepartment(Company):
    def __init__(self, name):
        super().__init__(name)

    def display(self, depth):
        print('\t' * depth + self.name)

    def list_duty(self):
        print('Hire and recruit for {}'.format(self.name))


class FinanceDepartment(Company):
    def __init__(self, name):
        super().__init__(name)

    def display(self, depth):
        print('\t' * depth + self.name)

    def list_duty(self):
        print('Finance issue for {}'.format(self.name))


if __name__ == '__main__':
    root = ConcreteCompany('Global Head Office')
    root.add(ConcreteCompany('SZ Branch Office'))

    hk_branch = ConcreteCompany('HK Branch Office')
    hk_branch.add(HrDepartment('HRD of HK Branch Office'))
    hk_branch.add(FinanceDepartment('Finance Department of HK Branch Office'))
    root.add(hk_branch)

    us_branch = ConcreteCompany('US Branch Office')
    us_branch.add(HrDepartment('HRD of US Branch Office'))
    us_branch.add(FinanceDepartment('Finance Department of US Branch Office'))
    root.add(us_branch)

    print('Structure of company:')
    root.display(0)

    print('Duties of departments:')
    root.list_duty()

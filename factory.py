#!/usr/bin/python
# coding=utf-8
#
# created by raylei, 2018/9/1


# 简单工厂：
# 定义：只是把创建对象的代码提取到一个工厂方法中。
# 缺点：①由于工厂类集中了所有产品创建逻辑，违反了高内聚责任分配原则，一旦不能正常工作，整个系统都要受到影响。
#       ②系统扩展困难，一旦添加新产品就不得不修改工厂逻辑，在产品类型较多时，有可能造成工厂逻辑过于复杂，
#       不利于系统的扩展和维护。
# 使用场景：①工厂类负责创建的对象较少。
#           ②客户只知道传入工厂类的参数，对于如何创建对象（逻辑）不关心；客户端既不需要关心创建细节，
#           甚至连类名都不需要记住，只需要知道类型所对应的参数。
class CheesePizza(object):
    def __init__(self):
        self.pizza = 'cheese pizza'

    def __str__(self):
        return self.pizza


class ClamPizza(object):
    def __init__(self):
        self.pizza = 'clam pizza'

    def __str__(self):
        return self.pizza


class SimplePizzaFactory(object):
    def __init__(self):
        self.pizza = None

    def create_pizza(self, pizza_type):
        if pizza_type == 'cheese':
            self.pizza = CheesePizza()
        elif pizza_type == 'clam':
            self.pizza = ClamPizza()
        return self.pizza


class SimplePizzaStore(object):
    @staticmethod
    def order_pizza(pizza_type):
        factory = SimplePizzaFactory()
        pizza = factory.create_pizza(pizza_type)
        return pizza


# 工厂方法：
# 定义：工厂父类提供创建产品对象的接口即工厂方法，而具体的工厂子类则实现了工厂方法，即由子类来确定究竟应该实例化哪一个具体产品类。
# 好处：①工厂方法集中的在一个地方创建对象，使对象的跟踪变得更容易。
#       ②工厂方法模式可以帮助我们将产品的实现从使用中解耦。如果增加产品或者改变产品的实现，Creator 并不会收到影响。
#       ③在系统中加入新产品时，无须修改抽象工厂和抽象产品提供的接口，无须修改客户端，也无须修改其他的具体工厂和具体产品，
#       而只要添加一个具体工厂和具体产品就可以了。这样，系统的可扩展性也就变得非常好，完全符合“开闭原则”
class PizzaStore(object):
    def __init__(self):
        self.pizza = None

    def create_pizza(self, pizza_type):
        raise NotImplementedError

    def order_pizza(self, pizza_type):
        pizza = self.create_pizza(pizza_type)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        return pizza


class FactoryMethodPizza(object):
    def __init__(self):
        self.name = None
        self.dough = None
        self.sauce = None
        self.toppings = []

    def prepare(self):
        print('preparing {}'.format(self.name))
        print('tossing dough...')
        print('adding sauce...')
        print('adding toppings:')
        for topping in self.toppings:
            print(' {}'.format(topping))

    @staticmethod
    def bake():
        print('bake for 25 min at 250')

    @staticmethod
    def cut():
        print('cutting the pizza into diagonal slices')

    @staticmethod
    def box():
        print('place pizza in official Pizza store box')

    def __str__(self):
        return self.name


class NewYorkCheesePizza(FactoryMethodPizza):
    def __init__(self):
        self.name = 'NY style sauce and cheese pizza'
        self.dough = 'thin crust dough'
        self.sauce = 'marinara sauce'
        self.toppings = ['Grated', 'Reggiano', 'Cheese']


class ChicagoCheesePizza(FactoryMethodPizza):
    def __init__(self):
        self.name = 'Chicago style deep dish cheese pizza'
        self.dough = 'extra thick crust dough'
        self.sauce = 'plum tomato sauce'
        self.toppings = ['Shredded', 'Mozzarella', 'Cheese']

    @staticmethod
    def cut():
        print('cutting the pizza into square slices')


class NewYorkPizzaStore(PizzaStore):
    def create_pizza(self, pizza_type):
        if pizza_type == 'cheese':
            self.pizza = NewYorkCheesePizza()
        return self.pizza


class ChicagoPizzaStore(PizzaStore):
    def create_pizza(self, pizza_type):
        if pizza_type == 'cheese':
            self.pizza = ChicagoCheesePizza()
        return self.pizza


# 抽象工厂：
# 定义：提供了一组接口，用于创建相关或依赖对象的家族，而不需要明确指定具体类。
# 好处：①可以将客户从具体产品中解耦；②抽象工厂可以让对象创建更容易被追踪；③同时将对象创建与使用解耦；④也可以优化内存占用提升应用性能
# 缺点：因为抽象工厂是将一组相关的产品集合起来，如果需要扩展这组产品，就需要改变接口，而改变接口则意味着需要改变每个子类的接口。
# OO原则：依赖倒置原则，即要依赖抽象类，不要依赖具体类（针对抽象编程，不要针对具体类编程）。
# 区别：工厂方法使用继承，抽象工厂使用对象的组合（一般都是多个工厂方法的组合，所以一般发现有多个工厂方法的时候，就该使用抽象工厂了）。
class FreshClams(object):
    def __str__(self):
        return 'Fresh Clams'


class MarinaraSauce(object):
    def __str__(self):
        return 'Marinara Sauce'


class ThickCrustDough(object):
    def __str__(self):
        return 'Thick Crust Dough'


class ReggianoCheese(object):
    def __str__(self):
        return "Reggiano Cheese"


class SlicedPepperoni(object):
    def __str__(self):
        return "Sliced Pepperoni"


class Garlic(object):
    def __str__(self):
        return "Garlic"


class Onion(object):
    def __str__(self):
        return "Onion"


class RedPepper(object):
    def __str__(self):
        return "Red Pepper"


class PizzaIngredientFactory(object):
    def create_dough(self):
        raise NotImplementedError

    def create_sauce(self):
        raise NotImplementedError

    def create_cheese(self):
        raise NotImplementedError

    def create_pepperoni(self):
        raise NotImplementedError

    def create_clam(self):
        raise NotImplementedError

    def create_veggies(self):
        raise NotImplementedError


class NYPizzaIngredientFactory(PizzaIngredientFactory):
    def create_dough(self):
        dough = ThickCrustDough()
        print('Tossing {}'.format(dough))
        return dough

    def create_sauce(self):
        sauce = MarinaraSauce()
        print('Adding {}'.format(sauce))
        return sauce

    def create_cheese(self):
        cheese = ReggianoCheese()
        print('Adding {}'.format(cheese))
        return cheese

    def create_pepperoni(self):
        pepperoni = SlicedPepperoni()
        print('Adding {}'.format(pepperoni))
        return pepperoni

    def create_clam(self):
        clam = FreshClams()
        print('Adding {}'.format(clam))
        return clam

    def create_veggies(self):
        veggies = [Garlic(), Onion(), RedPepper()]
        for veggie in veggies:
            print(' {}'.format(veggie))
        return veggies


class AbstractFactoryPizza(object):
    def __init__(self, name, ingredient_factory):
        self.name = name
        self.ingredient_factory = ingredient_factory
        self.dough = None
        self.sauce = None
        self.cheese = None
        self.pepperoni = None
        self.clam = None
        self.veggies = []

    def prepare(self):
        raise NotImplementedError

    @staticmethod
    def bake():
        print('bake fot 25 min at 350')

    @staticmethod
    def cut():
        print('cutting the pizza into diagonal slices')

    @staticmethod
    def box():
        print('place pizza in official pizza store box')

    def __str__(self):
        return self.name


class NYCheesePizza(AbstractFactoryPizza):
    def prepare(self):
        self.dough = self.ingredient_factory.create_dough()
        self.sauce = self.ingredient_factory.create_sauce()
        self.cheese = self.ingredient_factory.create_cheese()
        self.clam = self.ingredient_factory.create_clam()
        self.veggies = self.ingredient_factory.create_veggies()


class AbstractFactoryPizzaStore(object):
    def __init__(self):
        self.ingredient_factory = None

    def create_pizza(self, pizza_type):
        raise NotImplementedError

    def order_pizza(self, pizza_type):
        pizza = self.create_pizza(pizza_type)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        return pizza


class NYPizzaStore(AbstractFactoryPizzaStore):
    def __init__(self):
        self.pizza = None
        self.ingredient_factory = NYPizzaIngredientFactory()

    def create_pizza(self, pizza_type):
        if pizza_type == 'cheese':
            self.pizza = NYCheesePizza('NewYork Sauce and Cheese Pizza', self.ingredient_factory)
        return self.pizza


def main():
    print()
    print('Simple Factory')
    ps = SimplePizzaStore()
    pizza = ps.order_pizza('cheese')
    print('Ordered a pizza: {}, from simple pizza store'.format(pizza))

    print()
    print('Factory Method')
    nys = NewYorkPizzaStore()
    pizza = nys.order_pizza('cheese')
    print('Ordered a {}, from NewYork pizza store'.format(pizza))

    cs = ChicagoPizzaStore()
    pizza = cs.order_pizza('cheese')
    print('Ordered a {}, from Chicago pizza store'.format(pizza))

    print()
    print('Abstract Factory')
    nys = NYPizzaStore()
    pizza = nys.order_pizza('cheese')
    print('*' * 10)
    print('Ordered a {}, from NewYork pizza store'.format(pizza))
    print('*' * 10)


if __name__ == '__main__':
    main()

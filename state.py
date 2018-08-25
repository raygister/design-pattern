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


class Node(object):
    def __init__(self, tag_name, parent=None):
        self.tag_name = tag_name
        self.parent = parent
        self.children = []
        self.text = ''

    def __str__(self):
        if self.text:
            return '{}: {}'.format(self.tag_name, self.text)
        else:
            return self.tag_name


class Parser(object):
    def __init__(self, parse_str):
        self.parse_str = parse_str
        self.root = None
        self.curr_node = None
        self.state = first_tag

    def process(self, remaining_str):
        remaining = self.state.process(remaining_str, self)
        if remaining:
            self.process(remaining)

    def start(self):
        self.process(self.parse_str)


class FirstTag(object):
    @staticmethod
    def process(remaining_str, parser):
        index_start_tag, index_end_tag = remaining_str.find('<'), remaining_str.find('>')
        tag_name = remaining_str[index_start_tag + 1: index_end_tag]
        root = Node(tag_name)
        parser.root = parser.curr_node = root
        parser.state = child_node
        return remaining_str[index_end_tag+1:]


class ChildNode(object):
    @staticmethod
    def process(remaining_str, parser):
        # 注意这里只做判断应该转移到哪个状态，并不处理解析
        stripped = remaining_str.strip()
        if stripped.startswith('</'):
            parser.state = close_tag
        elif stripped.startswith('<'):
            parser.state = open_tag
        else:
            parser.state = text_node
        return stripped


class OpenTag(object):
    @staticmethod
    def process(remaining_str, parser):
        index_start_tag, index_end_tag = remaining_str.find('<'), remaining_str.find('>')
        tag_name = remaining_str[index_start_tag + 1: index_end_tag]
        node = Node(tag_name, parser.curr_node)  # 以当前节点作为父节点创造新节点
        parser.curr_node.children.append(node)  # 将新节点加到当前节点的子节点中
        parser.curr_node = node  # 开始标签了，迭代到新节点处理
        parser.state = child_node  # 状态转移
        return remaining_str[index_end_tag + 1:]


class CloseTag(object):
    @staticmethod
    def process(remaining_str, parser):
        index_start_tag, index_end_tag = remaining_str.find('<'), remaining_str.find('>')
        assert remaining_str[index_start_tag + 1] == '/'  # 确保为关闭标签
        tag_name = remaining_str[index_start_tag + 2: index_end_tag]  # 取出关闭标签的属性值
        assert tag_name == parser.curr_node.tag_name  # 确保关闭标签名与开始标签名相同
        parser.curr_node = parser.curr_node.parent  # 关闭标签了，返回父节点处理
        parser.state = child_node  # 状态转移
        return remaining_str[index_end_tag + 1:].strip()


class TextNode(object):
    @staticmethod
    def process(remaining_str, parser):
        index_start_tag = remaining_str.find('<')
        text = remaining_str[:index_start_tag]
        parser.curr_node.text = text  # 把标签对应文本设置为当前节点的属性值
        parser.state = child_node  # 状态转移
        return remaining_str[index_start_tag:]


# python的模块变量能够模仿单例，这里我们创建了可被重用的状态类实例
first_tag = FirstTag()
child_node = ChildNode()
open_tag = OpenTag()
close_tag = CloseTag()
text_node = TextNode()


if __name__ == '__main__':
    with open('./state.xml') as file:
        contents = file.read()
        parser = Parser(contents)
        parser.start()

        # BFS
        nodes = [parser.root]
        while nodes:
            node = nodes.pop(0)
            print(node)
            nodes = node.children + nodes

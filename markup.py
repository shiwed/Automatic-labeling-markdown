# encoding: utf-8
import sys
import re
from handlers import *
from util import *
from rules import *


class Parser:
    """
    Parser读取文本文件，应用规则并控制处理程序
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_filter(self, pattern, name):
        def the_filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(the_filter)

    def parse(self, file):
        for block in blocks(file):
            for the_filter in self.filters:
                block = the_filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break


class BasicTextParser(Parser):
    def __init__(self, handler):
        super().__init__(handler)
        self.add_rule(ListItemRule())
        self.add_rule(TitleRule())
        self.add_rule(HeadingRule())
        self.add_rule(Paragraph())

        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.add_filter(r'\(([\.a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+)\)', 'mail')


handler = MarkdownRenderer()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)

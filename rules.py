# encoding: utf-8
class Rule:
    def __init__(self):
        self.type = None

    def action(self, block, handler):
        handler.modify(self.type)
        handler.feed(block)
        return True


class HeadingRule(Rule):
    """
    标题只包含一行，不超过70个字符且不以冒号结尾
    """

    def __init__(self):
        super().__init__()
        self.type = 'heading'

    def condition(self, block):
        return '\n' not in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRule):
    """
    题目是文档中的第一个文本块，前提条件是它属于标题，所以继承标题类
    """

    def __init__(self):
        super().__init__()
        self.type = 'title'
        self.first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self, block)


class ListItemRule(Rule):
    """
    列表项是以连字符打头的段落。设置格式的过程中，将把连字符删除
    """

    def __init__(self):
        super().__init__()
        self.type = 'list_item'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.modify(self.type)
        handler.feed(block[1:].strip())
        return True


class Paragraph(Rule):
    def __init__(self):
        super().__init__()
        self.type = 'paragraph'

    def condition(self, block):
        return True

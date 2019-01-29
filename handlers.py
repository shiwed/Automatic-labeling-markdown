# encoding: utf-8
"""
这是一个文本处理程序
"""


class Handler(object):
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def modify(self, name):
        self.callback('modify_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                return match.group(0)
            return result
        return substitution


class MarkdownRenderer(Handler):
    @staticmethod
    def modify_heading():
        print('##', end='')

    @staticmethod
    def modify_list_item():
        print('- ', end='')

    @staticmethod
    def modify_title():
        print('#', end='')

    @staticmethod
    def modify_paragraph():
        pass

    @staticmethod
    def sub_emphasis(match):
        return '**%s**' % match.group(1)

    @staticmethod
    def sub_url(match):
        return '[%s](%s)' % (match.group(1), match.group(1))

    @staticmethod
    def sub_mail(match):
        return '<%s>' % (match.group(1))

    @staticmethod
    def feed(data):
        print(data)

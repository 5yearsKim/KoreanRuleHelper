from lib2to3.pytree import convert
from .parser import Parser
from .utils import convert_rule, check_match, tags2strlist
from copy import deepcopy

parser = Parser()

class KoreanSentence:
    def __init__(self, sentence):
        self.parsed = parser(sentence)
        self.original = sentence

    def __repr__(self):
        return f'KoreanSentence({self.text})'

    def __add__(self, obj):
        sent = deepcopy(self)
        sent.original = sent.original + obj.original
        sent.parsed = sent.parsed + obj.parsed
        return sent


    def parse(self, sent):
        return parser(sent)

    def replace(self, rules, expression):
        if type(rules) is not list:
            rules = [rules]
        rules = convert_rule(rules)
        sent = deepcopy(self)
        for tag in sent.parsed:
            for rule in rules: 
                if check_match([tag], rule)[0]:
                    tag.surface = expression
                    continue
        return sent 
    
    def strip(self, rules):
        if type(rules) is not list:
            rules = [rules]
        rules = convert_rule(rules)
        sent = deepcopy(self)
        def strip_one():
            for rule in rules: 
                if check_match(sent.parsed, rule)[0]:
                    sent.parsed.pop(0)
                    return True 
            for rule in rules: 
                if check_match(sent.parsed[-1:], rule)[0]:
                    sent.parsed.pop()
                    return True
            return False
        while len(sent.parsed) > 0 and strip_one():
            pass
        return sent 


    @property
    def text(self):
        parsed = tags2strlist(self.parsed)
        return ''.join(parsed)

        
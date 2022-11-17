from __future__ import annotations
from copy import deepcopy
from typing import TypeVar
from .parser import Parser, Tag
from .rule import Rule


class KoreanSentence:
    parser: Parser = Parser()

    def __init__(self, sentence: str) -> None:
        self.tags = self.parser(sentence)
        self.original = sentence

    def __repr__(self) -> str:
        return f'KoreanSentence({self.text})'

    # def __add__(self, obj):
    #     sent = deepcopy(self)
    #     sent.original = sent.original + obj.original
    #     sent.tags = sent.tags + obj.parsed
    #     return sent

    @property
    def text(self) -> str:
        surfaces = list(map(lambda tag: tag.surface, self.tags))
        return ''.join(surfaces)

    def parse(self, sent: str) -> list[Tag] :
        return self.parser(sent)

    def replace(self, rules: list[Rule]|Rule, expression: str) -> KoreanSentence:
        if isinstance(rules, Rule):
            rules = [rules]
        sent = deepcopy(self)
        for tag in sent.tags:
            for rule in rules: 
                if rule.check_match([tag], space_sensitive=True)[0]:
                    tag.surface = expression
                    break 
        return sent 
    
    def strip(self, rules: list[Rule]|Rule) -> KoreanSentence:
        _rules: list[Rule] = [rules] if isinstance(rules, Rule) else rules
        sent = deepcopy(self)
        def strip_one() -> bool:
            for rule in _rules:
                if rule.check_match(sent.tags)[0]:
                    sent.tags.pop(0)
                    return True 
            for rule in _rules: 
                if rule.check_match(sent.tags[-1:])[0]:
                    sent.tags.pop()
                    return True
            return False
        while len(sent.tags) > 0 and strip_one():
            pass
        return sent 



        
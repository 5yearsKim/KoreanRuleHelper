from __future__ import annotations

class Tag:
    def __init__(self, surface: str, pos: str, has_jongseong: bool=False, expression: str|None=None) -> None:
        self.surface: str = surface
        self.pos: str = pos
        self.has_jongseong: bool = has_jongseong
        if expression:
            self.expression: list[Tag]|None = self.split_expression(expression)
        else:
            self.expression = None

    def __repr__(self) -> str:
        if self.pos == '_':
            return '$_'
        if self.expression:
            return f'${self.surface}{self.expression}/{self.pos}'
        else:
            return f'${self.surface}/{self.pos}'

    def split_expression(self, expression: str) -> list[Tag]:
        # expression='나/NP/*+의/JKG/*
        def exp2tag(exp: str) -> Tag:
            surf, pos, _ = exp.split('/')
            return Tag(surf, pos)
        tags = expression.split('+')
        return list(map(exp2tag, tags))

from .tag import Tag
from .mecab import SimpleMecab

class ParserError(Exception):
    pass


class Parser:
    def __init__(self) -> None:
        self.mecab = SimpleMecab()

    def __call__(self, sent: str) -> list[Tag]:
        if sent == ' ':
            return [Tag(' ', '_')]
        holder: list[Tag] = []
        parsed = self.mecab.parse(sent)
        tmp_sent = sent
        for surface, feature in parsed:
            while tmp_sent[0] == ' ':
                tag = Tag(' ', '_')
                holder.append(tag)
                tmp_sent = tmp_sent[1:]
            if tmp_sent.startswith(surface):
                tag = Tag(surface, feature.pos, feature.has_jongseong, feature.expression)
                holder.append(tag)
                tmp_sent = tmp_sent[len(surface):]
            else:
                raise ParserError(f'{tmp_sent} not matching with {surface}!')
        return holder

import mecab

class Parser:
    def __init__(self):
        self.mecab = mecab.MeCab()

    def __call__(self, sent):
        if sent == ' ':
            return [Tag(' ', '_')]
        holder = []
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
                print('unmatched!')
                break
        return holder


class Tag:
    def __init__(self, surface, pos, has_jongseong=None, expression=None):
        self.surface = surface
        self.pos = pos
        self.has_jongseong = has_jongseong
        if expression:
            self.expression = self.split_expression(expression)
        else:
            self.expression = None
    
    def split_expression(self, expression):
        def exp2tag(exp):
            surf, pos, _ = exp.split('/')
            return Tag(surf, pos)
        tags = expression.split('+')
        tags = tuple(map(exp2tag, tags))
        return tags

    def __str__(self):
        return str(self.surface)

    def __repr__(self):
        if self.pos == '_':
            return '$_'
        if self.expression:
            return f'${self.surface}{self.expression}/{self.pos}'
        else:
            return f'${self.surface}/{self.pos}'

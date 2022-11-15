from typing import TypeVar
from .parser import Tag
from .config import WILDCARD

# rule_default = {
#     'surface': None, # str | [str]
#     'pos': None, # str | [str]
#     '!pos': None, # str | [str]
#     'return': False,
#     'optional': False,
# }



class ImportRuleError(Exception):
    pass


def split_wildcard(s: str, wildcard: str) -> list[str]:
    holder = []
    j = 0
    for i in range(len(s)):
        if s[i] == wildcard:
            if i > j:
                holder.append(s[j:i])
            holder.append(wildcard)
            j = i + 1
    if len(s) > j:
        holder.append(s[j:])
    holder = list(map(lambda s: s.strip(), holder))
    return holder

TRule = TypeVar('TRule', bound='Rule')

class Rule:
    def transform(raws: list[str | dict[str, str|list[str]|bool|None]]) -> list[TRule]:
        holder: list[Rule] = []
        for raw in raws:
            if isinstance(raw, str):
                for piece in split_wildcard(raw, WILDCARD):
                    rule = Rule().from_str(piece)
                    holder.append(rule)
            elif isinstance(raw, dict):
                rule = Rule().from_dict(raw)
                holder.append(rule)
        return holder

    def __init__(self,
        surface: str|list[str]|None = None,
        pos: str|list[str]|None = None,
        npos: str|list[str]|None = None,
        blank: bool = False,
        optional: bool = False,
    ) -> None:
        self.surface = surface
        self.pos = pos
        self.npos = npos
        self.blank = blank
        self.optional = optional

    def __repr__(self) -> str:
        contents: list[str]= [] 
        if (self.surface):
            contents.append(str(self.surface))
        if (self.pos):
            contents.append(str(self.pos))
        if (self.npos):
            contents.append(str(self.npos))
        if (self.blank):
            contents.append('blank')
        if (self.optional):
            contents.append('optional')
        return f'Rule({",".join(contents)})'

    @property 
    def is_wc(self) -> bool: # is wildcard?
        if self.surface == '*':
            return True
        if self.blank:
            return True
        return False

    def from_str(self, raw: str) -> None:
        self.surface = raw

    def from_dict(self, raw: dict[str, str|list[str]|bool|None]) -> None:
        if 'surface' in raw:
            self.surface = raw['surface']
        if 'pos' in raw:
            self.pos = raw['pos']
        if 'npos' in raw:
            self.npos = raw['npos']
        if 'blank' in raw:
            self.blank = raw['blank']
        if 'optional' in raw:
            self.optional = raw['optional']


    def check_match(self, tags: list[Tag], space_sensitive: bool=False) -> tuple[bool, list[Tag]]:
        if not tags:
            return False, []
        if self.surface:
            is_match, new_parsed_list = self._check_str_match(tags, space_sensitive=space_sensitive)
            return is_match, new_parsed_list
        else:
            '''
            o m result
            x x F
            x o T, p[1:]
            o x T, p[:]
            o o T, p[1:]
            '''
            is_match = self.judge_tag(tags[0])
            if is_match:
                return True, tags[1:]
            elif self.optional:
                return True, tags 
            else:
                return False, [] 


    def _check_str_match(self, tags: list[Tag], space_sensitive: bool=False):
        assert self.surface is not None
        rule: str = self.surface
        if rule == WILDCARD:
            return True, [] 
        if space_sensitive:
            rule = rule.strip()
        else:
            rule = rule.replace(' ', '')

        # strip parsed
        while tags[0].surface.isspace():
            tags = tags[1:]

        for i, tag in enumerate(tags):
            if tag.surface.isspace() and not space_sensitive:
                continue
            if rule == '':
                return True, tags[i:]
            if rule.startswith(tag.surface) or tag.surface.startswith(rule):
                rule = rule[len(tag.surface):]
            else:
                return False, None
        if rule == '':
            return True, tags[i+1:] # index + 1 when parsed match rule
        else:
            return False, None

    def judge_tag(self, tag: Tag) -> bool:
        # print(parsed_item, rule_item)
        def to_list(x: str|list[str]|None) -> list[str]:
            if not x:
                return []
            if isinstance(x, str):
                return [str]
            return x

        def is_common_pos(cand_pos: list[str], rule_pos: list[str]) -> bool:
            for rp in rule_pos:
                for cp in cand_pos:
                    if cp.startswith(rp):
                        return True
            return False 

        surfaces: list[str] = to_list(self.surface)
        if surfaces:
            surf_cand: list[str] = [tag.surface]
            if tag.expression:
                for exp in tag.expression:
                    surf_cand.append(exp.surface)
            common = set(surf_cand).intersection(set(surfaces))
            if len(common) == 0:
                return False
        poses: list[str] = to_list(self.pos)
        if poses:
            pos_cand = tag.pos.split('+')
            if not is_common_pos(pos_cand, poses):
                return False
        nposes: list[str] = to_list(self.npos)
        if nposes:
            pos_cand = tag.pos.split('+')
            if is_common_pos(pos_cand, nposes):
                return False
        return True



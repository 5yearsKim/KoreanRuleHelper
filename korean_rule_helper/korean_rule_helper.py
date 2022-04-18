from .parser import Parser
from .utils import convert_rule, check_match, tags2strlist, josa_rule
import hgtk
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
        rules = list(map(convert_rule, rules))
        sent = deepcopy(self)
        for tag in sent.parsed:
            for rule in rules: 
                if check_match(tag, rule):
                    tag.surface = expression
                    continue
        return sent 
    
    def strip(self, rules):
        if type(rules) is not list:
            rules = [rules]
        rules = list(map(convert_rule, rules))
        sent = deepcopy(self)
        def strip_one():
            tag = sent.parsed[0]
            for rule in rules: 
                if check_match(tag, rule):
                    sent.parsed.pop(0)
                    return True 
            tag = sent.parsed[-1]
            for rule in rules: 
                if check_match(tag, rule):
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

        

class KoreanRuleHelper:
    def __init__(self):
        pass

    def parse(self, sent):
        return parser(sent)
    
    def order_match(self, sentence, rule, return_str=True):
        parsed = sentence.parsed
        rule = list(map(convert_rule, rule))
        result, arg = self._recursive_order_match(parsed, rule, arg=[], tmp_arg=[])
        if arg and return_str:
            arg = list(map(lambda s: ' '.join(tags2strlist(s)).strip(), arg))
        return result, arg

    # def order_match_many(self, sentence, rules, return_str=True):
    #     parsed = self.parse(sentence)
    #     holder = []
    #     for rule in rules:
    #         result, arg = self._order_match(parsed, rule, return_str)
    #         if arg and return_str:
    #             arg = list(map(lambda s: ''.join(tags2strlist(s)).strip(), arg))
    #         holder.append((result, arg))
    #     return holder


    def make_polite(self, sentence):
        pass


    

    def add_josa(self, word, type='I_X'):
        if type not in josa_rule.keys():
            raise ValueError(f'type {type} not in {josa_rule.keys()}')
        js, njs = josa_rule[type]
        letter = word.strip()[-1]
        has_js = hgtk.checker.is_hangul(letter) and hgtk.text.decompose(letter)[2] != hgtk.text.DEFAULT_COMPOSE_CODE
        if has_js:
            return word + js
        else:
            return word + njs

    def _recursive_order_match(self, parsed, rule_list, arg=[], tmp_arg=[]):
        # print(parsed, rule_list, '\n')
        if not rule_list:
            return True, arg
        if not parsed:
            return False, None
        rule = rule_list[0]
        is_match = check_match(parsed[0], rule)
        if rule['is_first']:
            if not is_match:
                return False, None
        if rule['is_last']:
            if len(parsed) > 1:
                return self._recursive_order_match(parsed[-1:], rule_list, arg)
            else:
                if not is_match:
                    return False, None
        
        # print(is_match, 'is_match')
        # print(tmp_arg, 'tmp_arg', arg, 'arg')
        if rule['return']:
            if is_match:
                tmp_arg.append(parsed[0])
            if len(rule_list) == 1:
                if len(parsed) == 1:
                    if tmp_arg:
                        arg.append(tmp_arg.copy())
                        return self._recursive_order_match(parsed[1:], rule_list[1:], arg)
                    else:
                        return False, None
                else:
                    return self._recursive_order_match(parsed[1:], rule_list, arg, tmp_arg)
            else:
                is_next_match = check_match(parsed[0], rule_list[1])
                if is_match and len(tmp_arg) == 1 and is_next_match:
                    arg.append(tmp_arg.copy())
                    return self._recursive_order_match(parsed[1:], rule_list[1:], arg, [])
                elif tmp_arg and is_next_match:
                    if is_match:
                        tmp_arg = tmp_arg[:-1]
                    arg.append(tmp_arg.copy())
                    # print('*', rule_list)
                    return self._recursive_order_match(parsed, rule_list[1:], arg, [])
                else:
                    return self._recursive_order_match(parsed[1:], rule_list, arg, tmp_arg.copy())
        else:
            if is_match:
                return self._recursive_order_match(parsed[1:], rule_list[1:], arg, [])
            else:
                return self._recursive_order_match(parsed[1:], rule_list, arg, [])



            


    

from .utils import convert_rule, check_match, tags2strlist, josa_rule
import hgtk
from .korean_sentence import parser

class KoreanRuleError(Exception):
    pass

class KoreanRuleHelper:
    def __init__(self, space_sensitive=False):
        self.space_sensitive = space_sensitive

    def parse(self, sent):
        return parser(sent)
 
    def _precheck_rules(self, rules):
        for i, rule in enumerate(rules):
            # optional following * is not allowed
            try:
                if i > 0 and rules[i-1] == '*' and rule['optional']:
                    raise KoreanRuleError('optional rule following return rule is not allowed', rules)
                if i > 0 and rules[i-1]['return'] and rule['optional']:
                        raise KoreanRuleError('optional rule following return rule is not allowed', rules)
            except TypeError:
                pass

    def match(self, sentence, rule, return_str=True, strict=True):
        parsed = sentence.parsed
        rule = convert_rule(rule)
        self._precheck_rules(rule)
        result, arg = self._match(parsed, rule, arg=[], tmp_arg=[], strict=strict)
        if arg and return_str:
            arg = list(map(lambda s: ''.join(tags2strlist(s)).strip(), arg))
        return result, arg

    def _match(self, parsed, rule_list, arg=[], tmp_arg=[], strict=True):
        # print(parsed, rule_list)
        # print('------')
        if not rule_list:
            if strict and len(parsed) > 0:
                return False, None
            else:
                return True, arg
        if not parsed:
            return False, None

        rule = rule_list[0]
        
        if rule == '*':
            if len(rule_list) <= 1:
                return True, arg
            next_rule = rule_list[1]
            is_next_match, _ = check_match(parsed, next_rule, space_sensitive=self.space_sensitive)
            if is_next_match:
                return self._match(parsed, rule_list[1:], arg, [], strict=strict)
            else:
                return self._match(parsed[1:], rule_list, arg, [], strict=strict)
        # if rule is str ( exact matching )
        if isinstance(rule, str):
            is_match, new_parsed = check_match(parsed, rule, space_sensitive=self.space_sensitive)
            if is_match:
                return self._match(new_parsed, rule_list[1:], arg, [], strict=strict)
            else:
                return False, None


        is_match, new_parsed = check_match(parsed, rule)
        if rule['is_first']:
            if not is_match:
                return False, None
        if rule['is_last']:
            if len(parsed) > 1:
                return self._match(parsed[-1:], rule_list, arg, [], strict=strict)
            else:
                if not is_match:
                    return False, None

        if rule['optional']:
            if is_match:
                return self._match(parsed[1:], rule_list[1:], arg, [], strict=strict)
            else:
                return self._match(parsed, rule_list[1:], arg, [], strict=strict)
        
        # print(is_match, 'is_match')
        # print(tmp_arg, 'tmp_arg', arg, 'arg')
        if rule['return']:
            if is_match:
                tmp_arg.append(parsed[0])
            if len(rule_list) == 1:
                if len(parsed) == 1:
                    if tmp_arg:
                        arg.append(tmp_arg.copy())
                        return self._match(parsed[1:], rule_list[1:], arg, strict=strict)
                    else:
                        return False, None
                else:
                    return self._match(parsed[1:], rule_list, arg, tmp_arg, strict=strict)
            else:
                is_next_match, _ = check_match(parsed, rule_list[1])
                if is_match and len(tmp_arg) > 0 and is_next_match:
                    arg.append(tmp_arg.copy())
                    return self._match(parsed[1:], rule_list[1:], arg, [], strict=strict)
                elif tmp_arg and is_next_match:
                    if is_match:
                        tmp_arg = tmp_arg[:-1]
                    arg.append(tmp_arg.copy())
                    # print('*', rule_list)
                    return self._match(parsed, rule_list[1:], arg, [], strict=strict)
                else:
                    return self._match(parsed[1:], rule_list, arg, tmp_arg.copy(), strict=strict)
        else:
            if is_match:
                return self._match(parsed[1:], rule_list[1:], arg, [], strict=strict)
            else:
                if strict:
                    return False, None
                else:
                    return self._match(parsed[1:], rule_list, arg, [], strict=strict)


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

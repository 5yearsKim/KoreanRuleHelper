from .utils import convert_rule, check_match, tags2strlist, josa_rule, is_star
import hgtk

class KoreanRuleError(Exception):
    pass

class KoreanRuleHelper:
    def __init__(self, space_sensitive=False):
        self.space_sensitive = space_sensitive
    
    def _precheck_rules(self, rules):
        for i in range(len(rules) -1):
            r_a, r_b = rules[i], rules[i + 1]
            # optional following * is not allowed
            try:
                if is_star(r_a) and r_b['optional']:
                    raise KoreanRuleError('optional rule following * rule is not allowed', rules)
                if is_star(r_a) and is_star(r_b):
                    raise KoreanRuleError('* rule following * rule is not allowed', rules)
            except TypeError:
                pass

    def match(self, sentence, rule, return_str=True):
        parsed = sentence.parsed
        rule = convert_rule(rule)
        self._precheck_rules(rule)
        result, arg = self._match(parsed, rule)
        if arg and return_str:
            arg = list(map(lambda s: ''.join(tags2strlist(s)).strip(), arg))
        return result, arg

    ################
    #pppppp parsed
    #rrrrrr rule
    ################
    def _match(self, parsed_list, rule_list):
        is_return = lambda r: isinstance(r, dict) and ('return' in r) and r['return']
        is_optional = lambda r: isinstance(r, dict) and ('optional' in r) and r['optional']
        def helper(p_list, r_list):
            if not r_list and not p_list:
                return True, []
            if not r_list and p_list:
                return False, None
            # r_list always exists from below
            r = r_list[0] 
            if len(r_list) == 1 and is_star(r):
                # when r == '*' -> return true with no arg 
                if not is_return(r): 
                    return True, []
                arg = []
                for p in p_list:
                    if check_match([p], r, space_sensitive=self.space_sensitive)[0]:
                        arg.append(p)
                # when r['return'] true with no arg filtered -> return False 
                if arg == []:
                    return False, None
                # when r['return] true with arg -> return true
                return True, [arg]
            # when no p_list and all left rules are optional
            if not p_list and all([is_optional(x) for x in r_list]):
                return True, []
            if not p_list:
                return False, None

            if not is_star(r):
                is_match, next_p_list = check_match(p_list, r, space_sensitive=self.space_sensitive)
                if is_match:
                    return helper(next_p_list, r_list[1:])
                else:
                    return False, None
            else: # is_star(r)
                rr = r_list[1]
                assert not is_star(rr), 'rule following * rule cannot be a * rule'
                for i in range(len(p_list)):
                    # STEP 1 : check p_list match
                    is_next_match, next_p_list = check_match(p_list[i:], rr, space_sensitive=self.space_sensitive)
                    if not is_next_match:
                        continue
                    # STEP 2: check arg exist for return=True
                    arg = []
                    for p in p_list[:i]:
                        if check_match([p], r, space_sensitive=self.space_sensitive)[0]:
                            arg.append(p)
                        if arg and p.surface.isspace() and not arg[-1].surface.isspace():
                            arg.append(p)
                    if is_return(r) and arg == []:
                        continue
                    # STEP 3: check following p_list 
                    is_rp_match, rp_args = helper(next_p_list, r_list[2:])
                    if is_rp_match:
                        if is_return(r):
                            return True, [arg] + rp_args
                        else:
                            return True, rp_args
                    else:
                        continue
                return False, None
        return helper(parsed_list, rule_list)

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

from .parser import Tag
from .rule import Rule
from .korean_sentence import KoreanSentence

class KoreanRuleError(Exception):
    pass

class KoreanRuleHelper:
    def __init__(self, space_sensitive: bool=False):
        self.space_sensitive: bool = space_sensitive
    
    def _precheck_rules(self, rules: list[Rule]) -> None:
        for i in range(len(rules) -1):
            r_a, r_b = rules[i], rules[i + 1]
            # optional following * is not allowed
            if r_a.is_wc and r_b.optional:
                raise KoreanRuleError('optional rule following wildcard(*) rule is not allowed', rules)
            if r_a.is_wc and r_b.is_wc:
                raise KoreanRuleError('wildcard(*) following wildcard is not allowed', rules)

    def match(self, sentence: KoreanSentence, rules: list[Rule]) -> tuple[bool, list[str]]:
        """ Checking if sentence follow the order of given rlues
        - Argument
        sentence: KoreanSentence (Sentence parsed with tagger)
        rules: list[Rule] (List of custom rules)
        - Return
        result, arg : tuple[bool, list[str]]
        arg contains value for blank rule
        """
        def tags2str(tags: list[Tag]) -> str:
            holder = []
            for tag in tags:
                holder.append(tag.surface)
            return ''.join(holder)
        tags = sentence.tags
        self._precheck_rules(rules)
        result, arg = self._match(tags, rules)
        str_arg = list(map(lambda s: ''.join(tags2str(s)).strip(), arg))
        return result, str_arg

    def match_original(self, sentence: KoreanSentence, rules: list[Rule]) -> tuple[bool, list[list[Tag]]]:
        tags = sentence.tags
        self._precheck_rules(rules)
        result, arg = self._match(tags, rules)
        return result, arg

    ################
    #pppppp parsed
    #rrrrrr rule
    ################
    def _match(self, tags: list[Tag], rules: list[Rule]) -> tuple[bool, list[list[Tag]]]:
        def helper(p_list: list[Tag], r_list: list[Rule]) -> tuple[bool, list[list[Tag]]]:
            # print(p_list)
            # print(r_list)
            # print('--------------------------')
            if not r_list and not p_list:
                return True, []
            if not r_list and p_list:
                return False, [] 
            # r_list always exists from below
            r = r_list[0] 
            if len(r_list) == 1 and r.is_wc:
                # when r == '*' -> return true with no arg
                if not r.blank: 
                    return True, []
                arg = []
                for p in p_list:
                    if r.check_match([p],  space_sensitive=self.space_sensitive)[0]:
                        arg.append(p)
                # when r.blank true with no arg filtered -> return False 
                if arg == []:
                    return False, [] 
                # when r.blank true with arg -> return true
                return True, [arg]
            # when no p_list and all left rules are optional
            if not p_list and all([x.optional for x in r_list]):
                return True, []
            if not p_list:
                return False, []

            if not r.is_wc:
                is_match, next_p_list = r.check_match(p_list, space_sensitive=self.space_sensitive)
                if is_match:
                    return helper(next_p_list, r_list[1:])
                else:
                    return False, [] 
            else: # is_star(r)
                rr = r_list[1]
                assert not rr.is_wc, 'rule following wildcard(*) rule cannot be a wildcard rule'
                for i in range(len(p_list)):
                    # STEP 1 : check p_list match
                    is_next_match, next_p_list = rr.check_match(p_list[i:], space_sensitive=self.space_sensitive)
                    if not is_next_match:
                        continue
                    # STEP 2: check arg exist for return=True
                    arg = []
                    for p in p_list[:i]:
                        if r.check_match([p], space_sensitive=self.space_sensitive)[0]:
                            arg.append(p)
                        # add space if not included in arg
                        if arg and p.surface.isspace() and not arg[-1].surface.isspace():
                            arg.append(p)
                    if r.blank and arg == []:
                        continue
                    # STEP 3: check following p_list 
                    is_rp_match, rp_args = helper(next_p_list, r_list[2:])
                    if is_rp_match:
                        if r.blank:
                            return True, [arg] + rp_args
                        else:
                            return True, rp_args
                    else:
                        continue
                return False, [] 
        return helper(tags, rules)
            

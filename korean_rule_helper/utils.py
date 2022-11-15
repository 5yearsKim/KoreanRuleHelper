from .config import wildcard

josa_rule = {
    # tag: [True, False](종성 여부)
    'I_GA': ['이', '가'],
    'EUN_NEUN': ['은', '는'],
    'GWA_WA': ['과', '와'],
    'A_YA': ['아', '야'],
    'EUL_REUL': ['을', '를'],
    'RYUL_YUL': ['률', '율'],
    'EURO_RO': ['으로', '로'],
    'I_X': ['이', ''],
}

# def tags2strlist(tags):
#     return list(map(lambda tag: str(tag), tags))


        

def convert_rule(rules):
    holder = []
    for rule in rules:
        if type(rule) is str:
            rule = split_wildcard(rule, wildcard)
            holder.extend(rule)
        elif type(rule) is dict:
            template = rule_default.copy()
            template.update(rule)
            holder.append(template)
    return holder 



if __name__ == '__main__':
    import korean_rule_helper.parser.parser as parser
    sent = '내 꿈은 과학자가 되는 것이야.'
    parser = parser.Parser()
    parsed = parser(sent)
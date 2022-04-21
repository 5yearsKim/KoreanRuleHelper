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

rule_default = {
    'surface': None, # str | [str]
    'pos': None, # str | [str]
    '!pos': None, # str | [str]
    'return': False,
    'optional': False,
}


def tags2strlist(tags):
    return list(map(lambda tag: str(tag), tags))

def split_wildcard(s, wildcard):
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

def is_common_pos(cand_pos, rule_pos):
    for rp in rule_pos:
        for cp in cand_pos:
            if cp.startswith(rp):
                return True
    return False 

def is_star(rule):
    if rule == '*':
        return True
    try:
        return rule['return']
    except:
        return False

def check_match(parsed_list, rule, space_sensitive=False):
    if isinstance(rule, str):
        is_match, new_parsed_list = check_str_match(parsed_list, rule, space_sensitive=space_sensitive)
        return is_match, new_parsed_list
    else:
        '''
        o m result
        x x F
        x o T, p[1:]
        o x T, p[:]
        o o T, p[1:]
        '''
        is_match = check_rule_match(parsed_list[0], rule)
        if is_match:
            return True, parsed_list[1:]
        elif rule['optional']:
            return True, parsed_list
        else:
            return False, None

def check_rule_match(parsed_item, rule_item):
    to_list = lambda x : [x] if type(x) is not list else x
    surfaces = to_list(rule_item['surface']) if rule_item['surface'] else None
    poses = to_list(rule_item['pos']) if rule_item['pos'] else None
    nposes = to_list(rule_item['!pos']) if rule_item['!pos'] else None
    # print(parsed_item, rule_item)
    if surfaces:
        surf_cand = [parsed_item.surface]
        if parsed_item.expression:
            for exp in parsed_item.expression:
                surf_cand.append(exp.surface)
        common = set(surf_cand).intersection(set(surfaces))
        if len(common) == 0:
            return False
    if poses:
        pos_cand = parsed_item.pos.split('+')
        if not is_common_pos(pos_cand, poses):
            return False
    elif nposes:
        pos_cand = parsed_item.pos.split('+')
        if is_common_pos(pos_cand, nposes):
            return False
    return True

def check_str_match(parsed_list, rule, space_sensitive=False):
    if rule == wildcard:
        return True, [] 
    if space_sensitive:
        rule = rule.strip()
    else:
        rule = rule.replace(' ', '')

    # strip parsed
    while parsed_list[0].surface.isspace() == '_':
        parsed_list = parsed_list[1:]

    for i, parsed in enumerate(parsed_list):
        surf = parsed.surface
        if surf.isspace() and not space_sensitive:
            continue
        if rule == '':
            return True, parsed_list[i:]
        if rule.startswith(surf) or surf.startswith(rule):
            rule = rule[len(surf):]
        else:
            return False, None
    if rule == '':
        return True, parsed_list[i+1:] # index + 1 when parsed match rule
    else:
        return False, None

if __name__ == '__main__':
    import parser
    sent = '내 꿈은 과학자가 되는 것이야.'
    parser = parser.Parser()
    parsed = parser(sent)
    result = check_str_match(parsed, '내 꿈은', space_sensitive=False)
    print(result)
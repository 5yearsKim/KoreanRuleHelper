
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
    'is_first': False, 
    'is_last': False,
    # 'is_concat': False,
    'pos': None, # str | [str]
    '!pos': None, # str | [str]
    'return': False,
}


def tags2strlist(tags):
    return list(map(lambda tag: str(tag), tags))

def convert_rule(rule):
    template = rule_default.copy()
    if type(rule) is str:
        rule = rule if rule == ' ' else rule.strip()
        template.update({'surface': rule})
    elif type(rule) is dict:
        template.update(rule)
    return template

def is_common_pos(cand_pos, rule_pos):
    for rp in rule_pos:
        for cp in cand_pos:
            if cp.startswith(rp):
                return True
    return False 


def check_match(parsed_item, rule_item):
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
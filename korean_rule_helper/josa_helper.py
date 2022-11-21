import hgtk

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

class JosaHelper:
    def __init__(self) -> None:
        pass

    def add_josa(self, word: str, type: str='I_X') -> str:
        if type not in josa_rule.keys():
            raise ValueError(f'type {type} not in {josa_rule.keys()}')
        js, njs = josa_rule[type]
        letter = word.strip()[-1]
        has_js = hgtk.checker.is_hangul(letter) and hgtk.text.decompose(letter)[2] != hgtk.text.DEFAULT_COMPOSE_CODE
        if has_js:
            return word + js
        else:
            return word + njs
        
    


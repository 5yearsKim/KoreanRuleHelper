import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanRuleHelper, KoreanSentence

rh = KoreanRuleHelper()


def test_replace():
    sent = '문재인은 19대 대통령이다.'
    sent = KoreanSentence(sent)

    rule = {'surface': '다', 'pos': 'EF'}

    new_sent = sent.replace(rule, '에요')
    print(sent)
    print(new_sent)

def test_strip():
    sent = '문재인은 19대 대통령이다.'
    sent = KoreanSentence(sent)

    rules = [{'pos': ['EF', 'S']}]

    new_sent = sent.strip(rules)
    print(sent)
    print(new_sent)

def test_add_josa():
    from korean_rule_helper.utils import josa_rule
    import random
    js_list = ['가방', '설립', '소진', '상담', '돌']
    njs_list = ['현우', '지우', '수리', '장비', '희']
    for josa_type in josa_rule.keys():
        js = random.choice(js_list)
        njs = random.choice(njs_list)
        added_js = rh.add_josa(js, josa_type)
        added_njs = rh.add_josa(njs, josa_type)
        print(josa_type)
        print(js, added_js)
        print(njs, added_njs)
        print('\n')


if __name__ == "__main__":
    test_replace()

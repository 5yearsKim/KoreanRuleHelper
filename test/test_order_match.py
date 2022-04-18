import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanRuleHelper, KoreanSentence


rh = KoreanRuleHelper()

import pprint
pp = pprint.PrettyPrinter(indent=4)

# pp.pprint(parsed)

def test_order_one():
    tester = [
        (
            '내 꿈은 과학자야.',
            [{'surface': '나', 'return': True}, {'pos': 'N', 'return': True }, {'!pos':['J', 'E', 'S'], 'return': True} ],
        ),
        (
            '너 내 이름이 뭔지 알아?',
            [{'surface': '내', 'pos': 'NP'}, {'pos': 'NNG', 'return': True}, {'surface': '뭐', 'pos': 'NP'}, {'surface': '알', 'pos': 'VV'}]
        ),
        (
            '너 내 이름이 뭔지 아니?',
            [{'surface': '내', 'pos': 'NP'}, {'pos': 'NNG', 'return': True}, {'surface': '뭐', 'pos': 'NP'}, {'surface': '알', 'pos': 'VV'}]
        ),
        (
            '내 꿈 내 꿈 내 꿈',
            ['내', '꿈', '내', {'surface': '꿈','pos': 'N', 'is_last': True, 'return': True}]
        ),
        (
            '너 내 이름 뭔지 알아?',
            ['너', '내', {'return': True}, {'surface': '알'}],
        ),
    ]
    for sent, rule in tester:
        print(rh.parse(sent))
        sent = KoreanSentence(sent)
        result = rh.order_match(sent, rule, return_str=True)
        print(result, '$')
        print('---------------------')


if __name__ == '__main__':
    test_order_one()



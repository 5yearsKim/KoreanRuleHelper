import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanRuleHelper, KoreanSentence


rh = KoreanRuleHelper(space_sensitive=False)

import pprint
pp = pprint.PrettyPrinter(indent=4)

# pp.pprint(parsed)

def test_order_one():
    tester = [
        (
            [
            '내 꿈은 과학자야.',
            ],
            [{'surface': '나'}, {'pos': 'N', 'return': True }, {'pos': 'JX'}, {'!pos':['J', 'E', 'S'], 'return': True} ],
        ),
        (   [
                '너 내 이름이 뭔지 알아?',
                '너 내 이름 뭔지 알아?',
                '이름 알아?',
                '너 내 이름 알아?',
            ],
            ['너 내 이름', {'pos': 'J', 'optional': True}, {'return': True}, '알아?']
        ),
        (
            [
                '내가 잘 사는 것 조차 싫다',
                '내가 조차라고 말하는 것 조차 싫다',
                '내가 뭐라고 말하는 것 조차 싫고 이렇게 하는 것 조차 싫다.',
            ],
            ['내가', {'return': True}, '조차', '싫다', {'pos': 'SF', 'optional': True}]
        )
    ]
    for sent_list, rule in tester:
        print(rule)
        print('*'*30)
        for sent in sent_list:
            print(sent)
            sent = KoreanSentence(sent)
            result = rh.match(sent, rule, return_str=True)
            print('$', result)
            print('-'*30)
        print('&'*30)


if __name__ == '__main__':
    test_order_one()



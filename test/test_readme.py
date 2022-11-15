import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanRuleHelper, KoreanSentence, Rule 



sentence = KoreanSentence('나는 너를 사랑한다.')
print(sentence.tags) #[$나/NP, $는/JX, $_, $너/NP, $를/JKO, $_, $사랑/NNG, $한다($하/XSV, $ᆫ다/EF)/XSV+EF, $./SF]
print(sentence.text) # 나는 너를 사랑한다.

''' rule '''
# rule from string -> surface
rule = Rule.from_str('과자')
print(rule) # Rule(surface: 과자)

# rule from dict -> k - v pairs matching
rule = Rule.from_dict({'pos': ['N', 'V']})
print(rule) # Rule(pos: ['N', 'V'])

# rule from list of dict, str combined
rule = Rule.transform(['과자', {'pos': ['N', 'V']}])
print(rule) # [Rule(surface: 과자), Rule(pos: ['N', 'V'])]

''' order match '''
# order match 

rh = KoreanRuleHelper()
sentence = KoreanSentence('내 이름은 김치야')

rule = ['내', '이름', '은', '김치야']
rule = Rule.transform(rule)
is_match, arg = rh.match(sentence, rule)
print(is_match, arg) # True []

rule = ['내', '이름', {'blank': True, 'pos': 'N'}] 
rule = Rule.transform(rule)
is_match, arg = rh.match(sentence, rule)
print(is_match, arg) # True ['김치']

rule = ['내', {'blank': True, 'pos': 'N'}, '김치', {'pos': 'E'}]
rule = Rule.transform(rule)
is_match, arg = rh.match(sentence, rule)
print(is_match, arg) # True ['이름']

rule = ['내', {'blank': True, 'pos': 'N'}, '고기' ]
rule = Rule.transform(rule)
is_match, arg = rh.match(sentence, rule)
print(is_match, arg) # False []


# replace
sentence = KoreanSentence('문재인은 19대 대통령이다.')

rule = {'surface': '다', 'pos': 'EF'}
rule = Rule.from_dict(rule)
sentence = sentence.replace(rule, '에요')
print(sentence.text) # 문재인은 19대 대통령이에요.


rule = {'pos': 'NNP'}
rule = Rule.from_dict(rule)
sentence = sentence.replace(rule, '000')
print(sentence.text) # 000은 19대 대통령이에요.

# strip
sentence = KoreanSentence('박근혜는 18대 대통령이다.')

rules = [{'surface': '.', 'pos': 'S'}, '박근혜', '는'] # multiple rule
rules = Rule.transform(rules)
sentence = sentence.strip(rules)
print(sentence.text) #  18대 대통령이다

rule = '다' # single rule
rule = Rule.from_str(rule)
sentence = sentence.strip(rule)
print(sentence.text) #  18대 대통령이 



# add_josa
from korean_rule_helper import JosaHelper

js = JosaHelper()

word = '설빙'
josa_word = js.add_josa(word, type='EUL_REUL')
print(josa_word) # 설빙을

word = '사과'
josa_word = js.add_josa(word, type='GWA_WA')
print(josa_word) # 사과와












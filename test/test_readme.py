import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanRuleHelper, KoreanSentence

rh = KoreanRuleHelper()


sentence = KoreanSentence('나는 너를 사랑한다.')
print(sentence.parsed) #[$나/NP, $는/JX, $_, $너/NP, $를/JKO, $_, $사랑/NNG, $한다($하/XSV, $ᆫ다/EF)/XSV+EF, $./SF]
print(sentence.text) # 나는 너를 사랑한다.

''' order match '''

# order match 
sentence = KoreanSentence('내 이름은 김치야.')

rule = ['내', '이름']
is_match, arg = rh.order_match(sentence, rule)
print(is_match, arg) # True []

rule = ['내', '이름', {'return': True, 'pos': 'N'}] 
is_match, arg = rh.order_match(sentence, rule)
print(is_match, arg) # True ['김치']

rule = ['내', '성별', {'return': True, 'pos': 'N'}]
is_match, arg = rh.order_match(sentence, rule)
print(is_match, arg) # False None 

# replace
sentence = KoreanSentence('문재인은 19대 대통령이다.')

rule = {'surface': '다', 'pos': 'EF'}
sentence = sentence.replace(rule, '에요')
print(sentence.text) # 문재인은 19대 대통령이에요.


rule = {'pos': 'NNP'}
sentence = sentence.replace(rule, '000')
print(sentence.text) # 000은 19대 대통령이에요.

# strip
sentence = KoreanSentence('박근혜는 18대 대통령이다.')

rules = [{'surface': '.', 'pos': 'S'}, '박근혜', '는'] # multiple rule
sentence = sentence.strip(rules)
print(sentence.text) #  18대 대통령이다

rule = '다' # single rule
sentence = sentence.strip(rule)
print(sentence.text) #  18대 대통령이 



# add_josa
word = '설빙'
josa_word = rh.add_josa(word, type='EUL_REUL')
print(josa_word) # 설빙을

word = '사과'
josa_word = rh.add_josa(word, type='GWA_WA')
print(josa_word) # 사과와












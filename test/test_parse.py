import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanSentence
# sent = '진짜?'
sent = '너 내 이름이 뭐야?'
sent = KoreanSentence(sent)

print(sent.parsed)
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from korean_rule_helper import KoreanSentence

sent = '나는 명박이의 친구'
sent = KoreanSentence(sent)

print(sent.parsed)
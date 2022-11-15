import mecab_ko as MeCab
from collections import namedtuple

Feature = namedtuple('Feature', [
    'pos',
    'semantic',
    'has_jongseong',
    'reading',
    'type',
    'start_pos',
    'end_pos',
    'expression',
])

def _extract_line(line: str) -> tuple[str, Feature]:
    surface, feat_raw = line.split('\t')
    feat = feat_raw.split(',')
    assert len(feat) == 8

    values = [value if value != '*' else None for value in feat]
    feature = dict(zip(Feature._fields, values))
    feature['has_jongseong'] = True if feature['has_jongseong'] == 'T' else False # type: ignore

    return surface, Feature(**feature)

class SimpleMecab:
    def __init__(self) -> None:
        self.tagger =  MeCab.Tagger()
    
    def parse(self, sentence: str) -> list[tuple[str, Feature]]:
        raw = self.tagger.parse(sentence)
        lines = raw.split('\n')
        eos_idx = lines.index('EOS')
        if (eos_idx <=0):
            return []
        lines = lines[:eos_idx] 
        parsed = list(map(lambda l: _extract_line(l), lines))
        
        return parsed 
    

if __name__ == '__main__':
    mc = SimpleMecab()

    print(mc.parse('고'))

        
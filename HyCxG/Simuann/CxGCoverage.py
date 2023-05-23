from Simuann.SimuAnneal import Annealer
import random

PATTERN_SCORE = {
    'WORD' : 1.5,
    'CLUSTER' : 1.2,
    'TAG' : 1.,
    'NUM' : 0.
}

COVERAGE_SCORE = {
    'COVER' : 1,
    'INTER' : -0.4
}
THRESHOLD_RATE = 1000

def randint_generation(min, max, mount):
    list = []
    while len(list) != mount:
        unit = random.randint(min, max)
        if unit not in list:
            list.append(unit)
    return list

def obtain_elescore(pat : str):
    if '<' in pat:
        return (1, PATTERN_SCORE['CLUSTER'])
    elif pat.isupper():
        return (1, PATTERN_SCORE['TAG'])
    elif '[' in pat:
        return (0, PATTERN_SCORE['NUM'])
    else:
        return (1, PATTERN_SCORE['WORD'])

class CxGCoverageProblem(Annealer):
    """
    Find the maximum coverage of CxGs.
    """
    def __init__(self, state, patterns, starts, ends, vis = False):
        super(CxGCoverageProblem, self).__init__(state, vis)
        self.watch_dog = 0
        self.cxgs = patterns
        self.starts = starts
        self.ends = ends
        self.pattern_score = self.calculate_pattern_score(patterns)
        self.max_coverage = max(ends) - min(starts)

    def flip(self):
        ids = random.randint(0, len(self.cxgs)-1)
        self.state[ids] = 1- self.state[ids]
        if max(self.state) < 1:
            ids = random.randint(0, len(self.cxgs)-1)
            self.state[ids] = 1 - self.state[ids]

    def move(self):
        initial_energy = self.energy()
        self.flip()
        self.watch_dog += 1
        if self.watch_dog / (2 ** len(self.cxgs)) <= THRESHOLD_RATE:
            return self.energy() - initial_energy
        else:
            return self.energy() - initial_energy + THRESHOLD_RATE

    def energy(self):
        maximum_score = self.max_coverage * COVERAGE_SCORE['COVER'] + PATTERN_SCORE['WORD']
        e, pattern_score, coverage = 0, 0., []
        for i in range(len(self.cxgs)):
            if self.state[i] == 1:
                coverage.extend(list(range(self.starts[i], self.ends[i])))
                pattern_score += self.pattern_score[i]
        pattern_score /= sum(self.state)
        set_cover = set(coverage)
        e += (len(set_cover) * COVERAGE_SCORE['COVER'] + (len(coverage) - len(set_cover)) * COVERAGE_SCORE['INTER']) + pattern_score
        return maximum_score - e

    def calculate_pattern_score(self, patterns):
        pattern_scores = []
        for pat in patterns:
            scores = [obtain_elescore(p) for p in pat.split('--')]
            scores = sum([sco[1] for sco in scores]) / sum([sco[0] for sco in scores])
            pattern_scores.append(scores)
        return pattern_scores


if __name__ == '__main__':
    # Short Example
    # cxgs = {
    #     'the--NOUN--was--ADV' : (1, 5),
    #     'the--NOUN--was' : (1, 4),
    #     'NOUN--AUX--ADV' : (2, 5),
    #     'AUX--so--ADJ' : (3, 6)
    # }

    # Long Example
    # cxgs = {
    #     'PART--be--<830>': (0, 3),
    #     'AUX--completely--ADJ': (1, 4),
    #     'DET--ADJ--<976>': (5, 8),
    #     'which--AUX--ADV': (13, 16),
    #     't--VERB--up' : (22, 25),
    #     'VERB--up--ADP--DET' : (23, 27),
    #     'VERB--up--ADP' : (23, 26),
    #     'up--ADP--DET' : (24, 27),
    #     'ADP--all--DET--ADJ' : (25, 29),
    #     'ADP--all--DET' : (25, 28),
    #     'ADP--all--DET--ADJ--NOUN' : (25, 30),
    #     'all--DET--ADJ--NOUN' : (26, 30),
    #     'all--DET--ADJ' : (26, 29),
    #     'all--DET--ADJ--NOUN--ADP' : (26, 31),
    #     'DET--other--NOUN--ADP' : (27, 31),
    #     'DET--other--NOUN' : (27, 30),
    #     'other--NOUN--of' : (28, 31)
    # }

    # Example
    cxgs = {
        'NOUN--PUNCT--NOUN': (9, 12),
        'the--NOUN--are': (14, 17),
        'enough--to--VERB--DET--NOUN': (18, 23), #
        'enough--PART--VERB': (18, 21),
        'to--VERB--DET--NOUN--in': (19, 24),
        'to--VERB--DET--NOUN': (19, 23),
        'to--VERB--DET': (19, 22), #
        'VERB--DET--NOUN': (20, 23),
        'VERB--DET--NOUN--ADP': (20, 24),
        'the--NOUN--ADP': (21, 24),
        'NOUN--ADP--half': (22, 25),
        'so--PRON--VERB': (25, 28),
        'so--PRON--VERB--ADP': (25, 29),
        'you--VERB--to--VERB--DET--NOUN': (26, 32),
        'you--VERB--to--VERB--DET': (26, 31),
        'you--VERB--to': (26, 29),
        'you--VERB--to--VERB': (26, 30),
        'VERB--to--VERB--DET--NOUN': (27, 32),
        'VERB--to--VERB': (27, 30),
        'VERB--to--VERB--DET': (27, 31),
        'to--VERB--DET--NOUN--[2]': (28, 32),
        'to--VERB--DET--[2]': (28, 31),
        'VERB--DET--NOUN--[2]': (29, 32),
        'NOUN--PUNCT--NOUN--[2]': (31, 34)
    }
    cxg_names = list(cxgs)
    init_state = [0] * len(cxg_names)
    for _ in range(random.randint(1, len(cxg_names))):
        init_state[random.randint(0, len(cxg_names)-1)] = 1
    starts, ends, patterns = [], [], []
    for cxg  in cxgs:
        starts.append(cxgs[cxg][0])
        ends.append(cxgs[cxg][1])
        patterns.append(cxg)
    cp = CxGCoverageProblem(init_state, patterns, starts, ends, vis=True)
    cp.set_schedule(cp.auto(minutes=0.05))
    state, energy = cp.anneal()
    print()
    for ids in range(len(state)):
        if state[ids] == 1:
            cxg = list(cxgs)[ids]
            print('CXG : {}, ({}, {})'.format(cxg, cxgs[cxg][0], cxgs[cxg][1]))
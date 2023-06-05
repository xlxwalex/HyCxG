from Simuann import CxGCoverage
import random

t_minutes = 0.05
test_cxgs = {
    'the--NOUN--was--ADV' : (1, 5),
    'the--NOUN--was' : (1, 4),
    'NOUN--AUX--ADV' : (2, 5),
    'AUX--so--ADJ' : (3, 6)
}

cxg_names = list(test_cxgs)

# Initialize states
init_state = [0] * len(cxg_names)
for _ in range(random.randint(1, len(cxg_names))):
    init_state[random.randint(0, len(cxg_names)-1)] = 1

# Pack inputs
starts, ends, patterns = [], [], []
for cxg in test_cxgs:
    starts.append(test_cxgs[cxg][0])
    ends.append(test_cxgs[cxg][1])
    patterns.append(cxg)

# Initialize CxGCoverage
cp = CxGCoverage(init_state, patterns, starts, ends, vis=True)
cp.set_schedule(cp.auto(minutes=t_minutes))
state, energy = cp.anneal()
print()
print('>> Results:')
for ids in range(len(state)):
    if state[ids] == 1:
        cxg = list(test_cxgs)[ids]
        print('CXG : {}, ({}, {})'.format(cxg, test_cxgs[cxg][0], test_cxgs[cxg][1]))

# Output:
#  Temperature        Energy    Accept   Improve     Elapsed   Remaining
#      0.10000          0.66     0.00%     0.00%     0:00:01     0:00:00
#  Temperature        Energy    Accept   Improve     Elapsed   Remaining
#      0.10000          0.66     0.07%     0.04%     0:00:03     0:00:00
# >> Results:
# CXG : the--NOUN--was, (1, 4)
# CXG : AUX--so--ADJ, (3, 6)
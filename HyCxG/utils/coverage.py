from Simuann import CxGCoverage

def init_solver_state(cxg_length : int) -> list:
    init_state = [0] * cxg_length
    return init_state

def _unpack(cxg_dict : dict) -> dict:
    starts, ends, patterns = [], [], []
    for cxg in cxg_dict:
        starts.append(cxg_dict[cxg][0])
        ends.append(cxg_dict[cxg][1])
        patterns.append(cxg)
    return {'patterns' : patterns, 'starts' : starts, 'ends': ends}

def pre_detect(cons_pos : list) -> bool:
    if len(cons_pos) < 2:
        return False
    else:
        coverage = []
        for cons in cons_pos: coverage.extend(list(range(cons[0], cons[1])))
        if len(coverage) - len(set(coverage)) == 0: return False
        else:
            return True

def construct_dict(cons_pos: list) -> dict:
    # To avoid dup in the origin way of "dict([[ele[3], (ele[0], ele[1])] for ele in cons_pos])"
    cxg_dict, cxg_counter = {}, {}
    for cons in cons_pos:
        if cons[3] in cxg_dict:
            cxg_dict[cons[3] + '--[{}]'.format(cxg_counter[cons[3]] + 1)] = (cons[0], cons[1])
            cxg_counter[cons[3]] += 1
        else:
            cxg_dict[cons[3]] = (cons[0], cons[1])
            cxg_counter[cons[3]] = 1
    return cxg_dict

def cxg_max_coverage(starts, ends, indexs, cxgs, T_minutes = 0.05) -> list:
    cons_pos = list(zip(starts, ends, indexs, cxgs))
    cons_pos.sort(key=lambda x : x[0])
    # PRE-FILTER
    flag = pre_detect(cons_pos)
    if not flag: return cons_pos
    cxg_dict = construct_dict(cons_pos)
    init_state = init_solver_state(len(cxgs))
    solver = CxGCoverage(init_state, **_unpack(cxg_dict))
    solver.set_schedule(solver.auto(minutes=T_minutes))
    state, _ = solver.anneal()
    results = [cons_pos[ids] for ids in range(len(state)) if state[ids] == 1]
    return results
import multiprocessing as mp


class Parser(object):
    def __init__(self, Loader, Encoder, workers=10):
        self.Loader = Loader
        self.Encoder = Encoder
        self.workers = workers

    def parse_lines(self, lines):
        if self.workers is not None:
            chunk_size = 1000
            pool_instance = mp.Pool(processes=self.workers, maxtasksperchild=None)
            lines = pool_instance.map(self.Encoder.tagline, lines, chunksize=chunk_size)
            pool_instance.close()
            pool_instance.join()
            pool_instance = mp.Pool(processes=self.workers, maxtasksperchild=None)
            results = pool_instance.map(self.match_cons, lines, chunksize=chunk_size)
            pool_instance.close()
            pool_instance.join()
        else:
            lines = [self.Encoder.tagline(line) for line in lines]
            results = [self.match_cons(line) for line in lines]
        results = [self.del_duplicate(res) for res in results]
        return results

    def del_duplicate(self, result):
        if len(result[0]) <= 1:
            return result
        s = set()
        k = 0
        for i in range(len(result[0])):
            if (result[1][i], result[2][i]) not in s:
                result[0][k] = result[0][i]
                result[1][k] = result[1][i]
                result[2][k] = result[2][i]
                s.add((result[1][i], result[2][i]))
                k += 1
        for i in range(len(result)):
            del(result[i][k:])
        return result

    def match_cons(self, line):
        cons_idx, cons_start, cons_end = [], [], []
        for i, unit in enumerate(line):
            candidates = self.get_candidates(unit)
            for con, idx in candidates:
                match = True
                for j in range(1, len(con)):
                    if i + j < len(line):
                        if line[i + j][con[j][0] - 1] != con[j][1]:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match:
                    cons_idx.append(idx)
                    cons_start.append(i)
                    cons_end.append(i + len(con))
        return cons_idx, cons_start, cons_end

    def get_candidates(self, unit):
        candidates = []
        for i in self.Loader.dict_cons[0]:
            candidate = self.Loader.dict_cons[1][i][unit[i-1]]
            candidates += candidate
        return candidates





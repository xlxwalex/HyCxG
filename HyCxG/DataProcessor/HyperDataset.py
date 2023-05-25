from argparse import Namespace
from multiprocessing import Pool
from torch.utils.data import Dataset
from utils import DATASET_MAP
from utils import read_dataset, cxg_max_coverage, tokenize_aspect, tokenize_glue, pair_hypocxg, reconstruct_sentence
from tqdm import tqdm
from Tokenizer.ModelTokenizer import CxGTokenizer
from transformers import AutoTokenizer

class HyperDataLM(Dataset):
    def __init__(self, args: Namespace, set_name: str, desc: str = 'train', num_workers: int = 1, debug=False):
        super(HyperDataLM, self).__init__()
        self.args = args
        self.lmg  = args.lm_group
        self.CLS = '[CLS]' if self.lmg == 'BERT' else '<s>'
        self.SEP = '[SEP]' if self.lmg == 'BERT' else '</s>'
        self.sets = set_name
        self.desc = desc
        self.num_workers = num_workers
        self.debug = debug
        assert isinstance(num_workers, int)
        if num_workers > 1: print('>> Using multi-processing with `{}` workers to process the SimuAnneal Solver'.format(num_workers))
        elif num_workers < 1: raise Exception("[ERROR] HyperDataset param `{}` is incorrect (`{}` should > 0)".format('num_workers', 'num_workers'))
        assert set_name in DATASET_MAP
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(args.lm_path)
        if set_name.split('_')[-1] in ['French', 'Spanish', 'Dutch', 'German', 'Turkish']: # Multilingual Options
            self.tokenizer = AutoTokenizer.from_pretrained(args.lm_path)
            if set_name.split('_')[-1] == 'French': self.cxgprocessor = CxGTokenizer(args, lang='fra')
            elif set_name.split('_')[-1] == 'Dutch': self.cxgprocessor = CxGTokenizer(args, lang='nld')
            elif set_name.split('_')[-1] == 'Spanish': self.cxgprocessor = CxGTokenizer(args, lang='spa')
            elif set_name.split('_')[-1] == 'Turkish': self.cxgprocessor = CxGTokenizer(args, lang='tur')
            elif set_name.split('_')[-1] == 'German': self.cxgprocessor = CxGTokenizer(args, lang='deu')
            else: raise Exception('Cannot utilize an unknown parser for extracting CxGs, error mode ``.'.format(set_name.split('_')[-1]))
        else: self.cxgprocessor = CxGTokenizer(args)
        # Data Path
        if set_name.split('_')[-1] not in ['MNLI']:
            self.base_dir = DATASET_MAP[set_name]['base_dir']
            self.train_path = DATASET_MAP[set_name]['train_path']
            self.valid_path = DATASET_MAP[set_name]['valid_path']
            self.test_path  = DATASET_MAP[set_name]['test_path']
            self.mapper = {'train': self.train_path, 'valid' : self.valid_path, 'test' : self.test_path}
        else:
            self.base_dir = DATASET_MAP[set_name]['base_dir']
            self.train_path = DATASET_MAP[set_name]['train_path']
            self.valid_m_path = DATASET_MAP[set_name]['valid_m_path']
            self.test_m_path = DATASET_MAP[set_name]['test_m_path']
            self.valid_mm_path = DATASET_MAP[set_name]['valid_mm_path']
            self.test_mm_path = DATASET_MAP[set_name]['test_mm_path']
            self.mapper = {'train' : self.train_path, 'validm' : self.valid_m_path, 'validmm' : self.valid_mm_path, 'testm' : self.test_m_path, 'testmm' : self.test_mm_path}
        # Debug Info
        if self.debug:
            import os
            self.debug_path = os.path.join(self.base_dir, 'debug_{}'.format(desc))
            if os.path.exists(self.debug_path):
                import shutil
                shutil.rmtree(self.debug_path)
            if not os.path.exists(self.debug_path): os.mkdir(self.debug_path)
            print('>> Debug mode ON, the logs for multiple-wokrers are stored at %s.' % self.debug_path)
        # Read Data
        self.data = read_dataset(set_name, self.mapper[desc])
        # Syntax parser
        # Not Available in this repo.
        # Processor
        self.items, self.labels = self._multiprocessing()
        print('>>> Data [{}] Processed'.format(set_name))

    def _multiprocessing(self):
        # Select Processor
        data_len = len(self.data)
        if self.sets.startswith('JSONABSA'):
            worker_func = self._process_absa_json
        elif self.sets.startswith('JSONGLUE'):
            inner_name = self.sets.split('_')[-1]
            if inner_name in ['CoLA', 'SST', 'Counterfactual']:
                worker_func = self._process_single_json
            elif inner_name in ['RTE', 'MRPC', 'MNLIM', 'STS', 'QNLI', 'MNLI', 'QQP']:
                worker_func = self._process_pair_json
            else:
                raise Exception('Cannot parse the GLUE set : {}'.format(self.sets))
        else:
            raise Exception('Cannot parse the set : {}'.format(self.sets))
        # Run workers
        if self.num_workers == 1:
            return worker_func(0, 0, data_len, -1)
        else:
            pool = Pool()
            pool_list = []
            items, labels = [], []
            # Allocate data
            for i in range(self.num_workers):
                if i < self.num_workers:
                    start = i * data_len // (self.num_workers)
                    end = (i + 1) * data_len // (self.num_workers)
                    result = pool.apply_async(func=worker_func, args=[i, start, end, i])
                    pool_list.append(result)
            pool.close()
            pool.join()
            # Collect Data
            for res in pool_list:
                item, label = res.get()
                items.extend(item)
                labels.extend(label)
            return items, labels

    def _process_single_json(self, worker, start, end, position):
        items, labels = [], []
        for step, line in enumerate(tqdm(self.data[start: end], desc='Processing {} dataset'.format(self.desc) if worker < 0 else 'Processing [worker {}]'.format(worker), position=position)):
            sent_mask = [0]
            sentence = line[0]
            polarity = line[1]
            adj_matrix = None
            tok_res = tokenize_glue(self.tokenizer, sentence, adj_matrix)
            tokens, sents = tok_res
            sent_mask += len(tokens) * [1]
            post_tokens = [self.CLS] + tokens + [self.SEP]
            sent_mask += [0] * (len(post_tokens) - len(sent_mask))
            token_ids = self.tokenizer.convert_tokens_to_ids(post_tokens)
            try:
                cxgs = self.cxgprocessor.tokenize(sents, raw=True)
            except:
                print('[Error] cannot process %s, skip it' % sents)
                continue
            connections = cxg_max_coverage(cxgs['cons_start'], cxgs['cons_end'], cxgs['cons_idx'], cxgs['cons_pattern'], T_minutes=self.args.t_minutes)
            items.append([tokens, token_ids, sent_mask, connections, None])
            labels.append(polarity)
        return items, labels

    def _process_pair_json(self, worker, start, end, position):
        items, labels = [], []
        for step, line in enumerate(tqdm(self.data[start: end], desc='Processing CoLA {} dataset'.format(self.desc) if worker < 0 else 'Processing [worker {}]'.format(worker), position=position)):
            sent_mask = [0]
            premise = line[0]
            hypothesis = line[1]
            if self.debug:
                debug_fp = open(self.debug_path + '/worker_{}.txt'.format(worker), 'a+', encoding='utf-8')
                debug_fp.write('Worker [{}], ID[{}], Premise[{}], Hypothesis[{}]\n'.format(worker, start + step, ' '.join(premise), ' '.join(hypothesis)))
                debug_fp.close()
            polarity = line[2]
            adj_matrix = None
            premise_res = tokenize_glue(self.tokenizer, premise, adj_matrix)
            if self.args.parse_syntax:
                premise_tokens, premise_sents, premise_adj = premise_res
            else:
                premise_tokens, premise_sents = premise_res
            hypothesis_res = tokenize_glue(self.tokenizer, hypothesis, adj_matrix)
            if self.args.parse_syntax:
                hypothesis_tokens, hypothesis_sents, hypothesis_adj = hypothesis_res
            else:
                hypothesis_tokens, hypothesis_sents= hypothesis_res
            if (self.lmg == 'BERT'  and len(premise_tokens) > self.args.padding_size - 3) or (self.lmg == 'RoBERTa'  and len(premise_tokens) > self.args.padding_size - 4):
                premise_tokens = premise_tokens[: self.args.padding_size // 2]
                premise_sents = reconstruct_sentence(premise_tokens, lmg=self.lmg)
            if (self.lmg == 'BERT'  and len(hypothesis_tokens) > self.args.padding_size - len(premise_tokens) - 2) or (self.lmg == 'RoBERTa'  and len(hypothesis_tokens) > self.args.padding_size - len(premise_tokens) - 3):
                if self. lmg == 'BERT' : hypothesis_tokens = hypothesis_tokens[: self.args.padding_size - len(premise_tokens) - 2]
                else: hypothesis_tokens = hypothesis_tokens[: self.args.padding_size - len(premise_tokens) - 4]
                hypothesis_sents = reconstruct_sentence(hypothesis_tokens, lmg=self.lmg)
            sent_mask += len(premise_tokens) * [1]
            post_tokens = [self.CLS] + premise_tokens + [self.SEP]
            bias = len(post_tokens) - 1
            sent_mask += [0] * (len(post_tokens) - len(sent_mask))
            if self.lmg == 'RoBERTa':
                post_tokens = post_tokens + [self.SEP]
                sent_mask += [0]
                bias += 1
            post_tokens += (hypothesis_tokens + [self.SEP])
            sent_mask += ([1] * (len(hypothesis_tokens)) + [0])
            token_ids = self.tokenizer.convert_tokens_to_ids(post_tokens)
            try:
                premise_cxgs = self.cxgprocessor.tokenize(premise_sents, raw=True)
                premise_connections = cxg_max_coverage(premise_cxgs['cons_start'], premise_cxgs['cons_end'], premise_cxgs['cons_idx'],  premise_cxgs['cons_pattern'], T_minutes=self.args.t_minutes)
            except:
                print('[Error] cannot process %s, skip it' % premise_sents)
                continue
            try:
                hypothesis_cxgs = self.cxgprocessor.tokenize(hypothesis_sents, raw=True)
                hypothesis_connections = cxg_max_coverage(hypothesis_cxgs['cons_start'], hypothesis_cxgs['cons_end'], hypothesis_cxgs['cons_idx'], hypothesis_cxgs['cons_pattern'], T_minutes=self.args.t_minutes)
            except:
                print('[Error] cannot process %s, skip it' % hypothesis_sents)
                continue
            connections = premise_connections + pair_hypocxg(hypothesis_connections, bias)
            if len(post_tokens) > self.args.padding_size:
                print('Skip {}'.format(' '.join(post_tokens)))
                continue
            items.append([[premise_tokens, hypothesis_tokens], token_ids, sent_mask, connections, None])
            labels.append(polarity)
        if self.debug:
            debug_fp = open(self.debug_path + '/worker_{}.txt'.format(worker), 'a+', encoding='utf-8')
            debug_fp.write( 'Worker [{}] is all done.\n'.format(worker))
            debug_fp.close()
            debug_fp = open(self.debug_path + '/overall.txt'.format(worker), 'a+', encoding='utf-8')
            debug_fp.write('Worker [{}] is all done.\n'.format(worker))
            debug_fp.close()
        return items, labels

    def _process_absa_json(self, worker, start, end, position):
        items, labels = [], []
        for step, line in enumerate(tqdm(self.data[start: end], desc='Processing {} dataset'.format(self.desc) if worker < 0 else 'Processing [worker {}]'.format(worker), position=position)):
            sent_mask = [0]
            sentence = line[0]
            aspect = line[1]
            from_to = line[2]
            polarity = line[3]
            if self.debug:
                debug_fp = open(self.debug_path + '/worker_{}.txt'.format(worker), 'a+', encoding='utf-8')
                debug_fp.write('Worker [{}], ID[{}], Sentence[{}], Aspect[{}]\n'.format(worker, start + step, ' '.join(sentence), ' '.join(aspect)))
                debug_fp.close()
            adj_matrix = None
            tok_res = tokenize_aspect(self.tokenizer, sentence, from_to, adj_matrix)
            tokens, aspmask, sents = tok_res
            aspmask = [0] + aspmask
            sent_mask += len(tokens) * [1]
            post_tokens = [self.CLS] + tokens + [self.SEP] + self.tokenizer.tokenize(aspect) + [self.SEP]
            sent_mask += [0] * (len(post_tokens) - len(sent_mask))
            token_ids = self.tokenizer.convert_tokens_to_ids(post_tokens)
            try:
                cxgs = self.cxgprocessor.tokenize(sents, raw=True)
            except:
                print('[Error] cannot process %s, skip it' % sents)
                continue
            connections = cxg_max_coverage(cxgs['cons_start'], cxgs['cons_end'], cxgs['cons_idx'], cxgs['cons_pattern'], T_minutes=self.args.t_minutes)
            items.append([tokens, token_ids, sent_mask, aspmask, connections, None])
            labels.append(polarity)
        if self.debug:
            debug_fp = open(self.debug_path + '/worker_{}.txt'.format(worker), 'a+', encoding='utf-8')
            debug_fp.write( 'Worker [{}] is all done.\n'.format(worker))
            debug_fp.close()
            debug_fp = open(self.debug_path + '/overall.txt'.format(worker), 'a+', encoding='utf-8')
            debug_fp.write('Worker [{}] is all done.\n'.format(worker))
            debug_fp.close()
        return items, labels

    def __getitem__(self, item_id):
        if 'ABSA' in self.sets:
            _, tokid, mask, aspmask, cxgs, adj = self.items[item_id]
            polarity = self.labels[item_id]
            return {
                'tok' : tokid,
                'mask' : mask,
                'aspmask' : aspmask,
                'cxg' : cxgs,
                'adj' : adj,
                'label' : polarity,
                'padding' : self.args.padding_size,
                'aux_token' : _
            }
        elif self.sets.split('_')[-1] in ['CoLA', 'SST', 'RTE', 'MRPC', 'MNLIM', 'MNLI', 'STS', 'QNLI', 'Counterfactual', 'QQP']:
            _, tokid, mask, cxgs, adj = self.items[item_id]
            label = self.labels[item_id]
            return {
                'tok': tokid,
                'mask': mask,
                'cxg': cxgs,
                'adj': adj,
                'label': label,
                'padding': self.args.padding_size,
                'aux_token': _
            }

    def __len__(self):
        return len(self.labels)
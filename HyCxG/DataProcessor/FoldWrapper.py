from argparse import Namespace
from DataProcessor.HyperDataset import HyperDataLM
from copy import deepcopy
from sklearn.model_selection import KFold

# Note: This Module is only utilized for Countertfactual task
class KFoldWrapper(HyperDataLM):
    def __init__(self, args: Namespace, set_name: str, desc: str = 'train', num_workers: int = 1, debug=False):
        super(KFoldWrapper, self).__init__(args, set_name, desc, num_workers, debug)
        self.curfold_items, self.curfold_labels = deepcopy(self.items), deepcopy(self.labels)
        kfold_splitter = KFold(n_splits=args.kfold)
        self.grtrain_ids, self.grvalid_ids = self.calculate_ids(kfold_splitter)

    def calculate_ids(self, splitter):
        train_ids, valid_ids = [], []
        for train_index, valid_index in splitter.split(self.curfold_items):
            train_ids.append(train_index)
            valid_ids.append(valid_index)
        return train_ids, valid_ids

    def set_valid(self):
        self.desc = 'valid'

    def set_group(self, index : int):
        if index >= self.args.kfold: raise Exception('Error in setting `index`, `index` need to be lower than %d' % self.args.kfold)
        if self.desc == 'train': inds = self.grtrain_ids[index]
        elif self.desc == 'valid': inds = self.grvalid_ids[index]
        else: raise Exception('Error in setting `desc` mode, you can only choose [`train`, `valid`]')
        self.items, self.labels = [self.curfold_items[idx] for idx in inds], [self.curfold_labels[idx] for idx in inds]
        print('>> Kfold set the group to %d for %s set, total %d instances.' % (index, self.desc, len(self)))
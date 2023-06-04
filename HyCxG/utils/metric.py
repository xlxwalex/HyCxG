from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, matthews_corrcoef
import numpy as np
from scipy.stats import pearsonr

class Metric(object):
    def __init__(self, args):
        self.args = args

    def __call__(self, preds : np.ndarray, truth : np.ndarray, sets_name = 'ABSA'):
        if sets_name not in ['STS']:
            accuracy = accuracy_score(truth, preds)
            precision = precision_score(truth, preds, average='macro')
            recall = recall_score(truth, preds, average='macro')
            f1score = f1_score(truth, preds, average='macro')
            return accuracy, precision, recall, f1score
        else:
            pearson = pearsonr(truth, preds)[0]
            return pearson

    def report(self, preds : np.ndarray, truth : np.ndarray, digit : int = 5):
        print(classification_report(truth, preds, digits=digit))

    def print_matthew(self, preds : np.ndarray, truth : np.ndarray):
        matt = matthews_corrcoef(truth, preds) * 100
        print('CoLA Matthews_coef = {:.3f}'.format(matt))
        return matt
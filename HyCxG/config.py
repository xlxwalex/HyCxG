from utils.argument import ArgumentGroup
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='HyCxG Model Parameters Setting')
    # Base Params
    base_args = ArgumentGroup(parser, 'base', 'Base Settings')
    base_args.add_arg('mode', str, 'train', 'Experiment Mode')
    base_args.add_arg('cuda', bool, True, 'CUDA device')
    base_args.add_arg('gpu_id', int, 0, 'GPU ID, 0 for cuda:0')
    base_args.add_arg('seed', int, 0, 'Global Random Seed')
    base_args.add_arg('checkpoints', str, 'checkpoints/', 'Checkpoint Path')
    base_args.add_arg('checkp', str, 'hyper_cxg_mams/', 'Checkpoint Dir')

    # Dataset Params
    data_args = ArgumentGroup(parser, 'dataset', 'Dataset Settings')
    data_args.add_arg('data_name', str, 'JSONABSA_MAMS', 'Name of Dataset')
    data_args.add_arg('num_workers', int, 64, 'Number of workers to solve coverage problem')
    data_args.add_arg('t_minutes', float, 0.05, 'Cost of time to solve the coverage problem per instance (minutes)')
    data_args.add_arg('test_outpath', str, 'result_test.csv', 'Output test results for analysis')

    # Model Params
    model_args = ArgumentGroup(parser, 'model', 'Model Settings')
    model_args.add_arg('num_classes', int, 3, 'Number of classes or each task')
    model_args.add_arg('padding_size', int, 150, 'Padding size Of PLM Model')
    model_args.add_arg('padding_val', int, 0, 'Padding value of PLM Model')
    model_args.add_arg('lm_dropout', float, 0.0, 'Dropout for PLM model')
    model_args.add_arg('hg_dropout', float, 0.4, 'Dropout for R-HGAT network')
    model_args.add_arg('hg_inter_dim', int, 384, 'Size of representations for transform hgatt network')
    model_args.add_arg('hg_layers', int, 1, 'Number of layers for R-HGAT network')
    model_args.add_arg('inter_size', int, 3072, 'Size of middle representations in FFN module')
    model_args.add_arg('leaky_alpha', float, 0.2, 'Alpha setting for leaky_relu in R-HGAT network')
    model_args.add_arg('edge_trans', bool, True, 'Transform hyperedge embedding (construction)')
    model_args.add_arg('remove_layernorm', bool, False, 'Remove layernorm for the embedding of cxg')
    # If enable multi-head R-HGAT (Not available in the repo)
    model_args.add_arg('heads_num', int, 12, 'Head num of hyper graph attention')
    # If enable syntactic graph (Not available in the repo)
    model_args.add_arg('parse_syntax', bool, False, 'Whether to inject syntax inform')
    model_args.add_arg('parse_direct', bool, False, 'Whether to construct direct graph')

    # Tokenizer and CxG Processor Params
    tokenizer_args = ArgumentGroup(parser, 'tokenizer', 'Tokenizer Settings')
    tokenizer_args.add_arg('word_vocab_path', str, 'dataset/Vocab/BERT/', 'LM Vocab path')
    tokenizer_args.add_arg('cxg_vocab_path', str, 'dataset/Vocab/CxG/', 'LM Vocab path')
    tokenizer_args.add_arg('do_lower_case', bool, True, 'Lower case the elememts')

    # Pre-trained Model Params
    pretrained_args = ArgumentGroup(parser, 'pretrained', 'Pre-trained Model Settings')
    pretrained_args.add_arg('lm_group', str, 'BERT', 'Pre-trained language model group, e.g., BERT/RoBERTa')
    pretrained_args.add_arg('use_lm', bool, True, 'Whether Model Use pre-trained language models')
    pretrained_args.add_arg('lm_path', str, 'bert-base-uncased', 'Pre-trained model path')
    pretrained_args.add_arg('lm_hidden_size', int, 768, 'HiddenSize of PLM')
    pretrained_args.add_arg('output_hidden_states', bool, True, 'Output PLM hidden states at token level')
    pretrained_args.add_arg('finetune', bool, True, 'Finetune Or freeze PLM')

    # Training Params
    train_args = ArgumentGroup(parser, 'train', 'Training Settings')
    train_args.add_arg('batch_size', int, 32, 'Batch size for training, depending on the memory size of your GPU')
    train_args.add_arg('shuffle', bool, True, 'DataLoader shuffle params, should be True when training')
    train_args.add_arg('droplast', bool, False, 'Whether to drop rest data for dataloader')
    train_args.add_arg('lr', float, 2e-5, 'Learning rate')
    train_args.add_arg('wd', float, 1e-2, 'Weight decay')
    train_args.add_arg('max_grad_norm', float, 1.0, 'Gradient clipping')
    train_args.add_arg('num_epoch', int, 50, 'Epoch param')
    train_args.add_arg('warmup_ratio', int, 0.06, 'Warm Up Steps Phase')
    train_args.add_arg('print_step', int, 5, 'Training Print Steps')
    train_args.add_arg('eval_step', int, 50, 'Evaluating Steps')
    train_args.add_arg('scheduler', bool, False, 'Whether to apply scheduler for training')

    args = parser.parse_args()
    return args


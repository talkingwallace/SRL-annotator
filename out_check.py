import json

import database

labeled_keys = ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'loc', 'tmp', 'prp']


def out_check(file_path, project_name='default'):
    """
    check the basic rules of output files
    """
    dm = database.DataManager(project_name, file_path)
    sent2id = dm.data['sent2id']
    f = open(file_path, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        record = json.loads(line)
        srl, sent = record['srl'], record['sent']
        sent_id = sent2id[sent]
        seq_sent = []
        for word in sent.split(' '):
            if word != '<SEP>':
                seq_sent.append(word)
        sent_lens = len(seq_sent)
        for srl_item in srl:
            pred, args = int(srl_item['pred']), srl_item['args']
            pred_args_spans = []
            for arg_key in args.keys():
                arg_v = args[arg_key]
                arg_v_s, arg_v_e = int(arg_v[0]), int(arg_v[1])
                pred_args_spans.append(range(arg_v_s, arg_v_e))
                # pred not in args span
                if pred in range(arg_v_s, arg_v_e + 1):
                    print('error {}: pred {}({}) in \'{}\' span'.format(sent_id, pred, seq_sent[pred], arg_key))
                # out of index
                if pred >= sent_lens or arg_v_s >= sent_lens or arg_v_e >= sent_lens:
                    print('error {}: out of index occurred in pred {}({})'.format(sent_id, pred, seq_sent[pred]))
                if arg_v_e - arg_v_s >= 20:
                    print('Warning {}: arg span len exceeds 20. pred {}({})'.format(sent_id, pred, seq_sent[pred]))
            # overlap arg spans
            tmp_check_span = []
            for args_span in pred_args_spans:
                if len(set(tmp_check_span).intersection(args_span)) != 0:
                    print('error {}: spans overlapping occurred in pred {}({}) arg ({}, {})'.format(
                        sent_id, pred, seq_sent[pred], args_span[0], args_span[-1]))
                tmp_check_span = list(set(tmp_check_span).difference(set(args_span)))


out_check('./result/result1578122401.txt')

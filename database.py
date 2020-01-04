import shelve
from shelve import DbfilenameShelf
import os
import pandas as pd
import time
import json

"""
Important key in shelve:
id2sent: unique Id set for all sentences
sent2id: ~
todo: set of sent Id, record id of sentences to be annotated
annotations: a pandas data frame which store annotations 
"""


def start_a_project(file_path, project_name='default', ):
    data_name = project_name
    if os.path.exists(data_name):
        os.rmdir(data_name)
    data = shelve.open(data_name, writeback=True)

    f = open(file_path, 'r', encoding='utf-8')
    sent_set = set()
    sents = f.read().split('\n')
    for sent in sents:
        if sent != '':
            sent_set.add(sent)

    data['id2sent'] = {hash(v): v for idx, v in enumerate(sent_set)}
    data['sent2id'] = {v: hash(v) for idx, v in enumerate(sent_set)}
    data['annotation'] = pd.DataFrame({'sentid': [], 'pred': [], 'args': [], 'sent': []})
    # 'timestamp':[]
    data['done'] = set()
    data.sync()

    return data


def start_a_task(data: DbfilenameShelf, sent_ids: set):
    assert sent_ids.issubset(set(data['id2sent'].keys()))
    data['todo'] = sent_ids


def save_annotations(data: DbfilenameShelf, sent_id: int, pred_idx: int, arg: dict):
    assert sent_id in data['id2sent']

    new_row = pd.DataFrame({'sentid': [sent_id], 'pred': [pred_idx], 'args': [arg], 'sent': [data['id2sent'][sent_id]]})
    data['annotation'] = data['annotation'].append(new_row)
    data.sync()


def commit(data: DbfilenameShelf, sent_id):
    data['done'].add(sent_id)
    print(sent_id, 'added into done')
    data.sync()


def load_database(project_name: str):
    if os.path.exists(project_name + '.dat'):
        data = shelve.open(project_name, writeback=True)
    elif os.path.exists(project_name + '.db'):
        data = shelve.open(project_name, writeback=True)
    else:
        data = None
    return data


def check_all_annotation(data: DbfilenameShelf):
    return data['annotation']


def output_annotations(data: DbfilenameShelf):
    df: pd.DataFrame = data['annotation']
    out_name = './result/' + 'result' + str(int(time.time())) + '.txt'
    outf = open(out_name, 'a+', encoding='utf-8')
    a = df.reset_index()
    sent_id_set = set(a['sentid'])
    new_record = {}
    total_pred = 0
    for sent_id in sent_id_set:
        new_record['sentid'] = sent_id
        srl_list = []
        same_id_df = a[a['sentid'] == sent_id]
        for i, row in same_id_df.iterrows():
            srl_tmp_pred = set([d['pred'] for d in srl_list])
            tmp_pred = int(row['pred'])
            # remove flag
            remove_pred = False
            if 'arg0' in row['args'].keys() and row['args']['arg0'][0] == -100:
                remove_pred = True
            if tmp_pred not in srl_tmp_pred:
                if remove_pred:
                    continue
                tmp_dict = {}
                tmp_dict['pred'] = int(row['pred'])
                tmp_dict['args'] = row['args']
                srl_list.append(tmp_dict)
                total_pred += 1
            else:
                for rev_i, d in enumerate(srl_list):
                    if d['pred'] == tmp_pred:
                        if not remove_pred:
                            d['args'] = row['args']
                            continue
                        else:
                            del srl_list[rev_i]
                            continue
        new_record['srl'] = srl_list
        new_record['sent'] = same_id_df.iloc[0]['sent']
        json_str = json.dumps(new_record, ensure_ascii=False)
        outf.write(json_str + '\n')
    outf.close()
    print('total predicates: ' + str(total_pred))


class DataManager(object):

    def __init__(self, project_name, file_path=None, ):
        self.data = load_database(project_name)
        if self.data is None:
            self.data = start_a_project(file_path, project_name)
        self.total_sent = len(set(self.data['id2sent'].keys()))
        self.done_num = len(self.data['done'])
        self.all_sent_id = list(set(self.data['id2sent'].keys()))
        # self.to_do = list(set(self.data['id2sent'].keys()).difference(self.data['done']))
        self.cur_idx = len(self.data['done'])

    def fetch_current(self):
        return self.all_sent_id[self.cur_idx]

    def fetch_prev(self):
        if self.cur_idx > 0:
            self.cur_idx -= 1
            return self.all_sent_id[self.cur_idx]
        else:
            return -1

    def fetch_next(self):
        if self.cur_idx >= self.done_num:
            print('Just can review the labeled sentences!')
            self.cur_idx = self.done_num
            return self.all_sent_id[self.cur_idx]
        else:
            self.cur_idx += 1
            return self.all_sent_id[self.cur_idx]

    def fetch_by_index(self, index):
        # fetch by sent_id first
        index = int(index)
        if index in set(self.all_sent_id):
            self.cur_idx = self.all_sent_id.index(index)
            return index
        # fetch by index next
        if 0 <= index <= self.done_num:
            self.cur_idx = index
            return self.all_sent_id[index]
        else:
            print('The index should between 0 and {}'.format(self.done_num))
            self.cur_idx = self.done_num
            return self.all_sent_id[self.done_num]

    def commit(self, sent_id=None):
        # sent_id = self.to_do[self.cur_idx]
        if sent_id is None:
            sent_id = self.all_sent_id[self.cur_idx]
        commit(self.data, sent_id)
        self.cur_idx += 1
        self.done_num = len(self.data['done'])

    def save(self, sent_id: int, pred_idx: int, arg: dict):
        save_annotations(self.data, sent_id, pred_idx, arg)

    def drop(self, send_id):
        pass

    def modify(self, sent_id):
        pass

    def search_by_keyword(self, keyword):
        df = self.data['annotation']
        return df[df['sent'].apply(lambda x: keyword in x)]

    def search_by_arg(self, arg_name: str, arg_span=None):
        df = self.data['annotation']
        return df[df['args'].apply(lambda x: arg_name in x)]

    def search_by_pred(self, pred: str):
        df = self.data['annotation']
        return df[
            df[['pred', 'sent']].apply(lambda x: x['sent'].replace('<SEP> ', '').split(' ')[int(x['pred'])] == pred,
                                       axis=1)]

    def get_all_pred(self, ):
        df = self.data['annotation']
        return df[['pred', 'sent']].apply(lambda x: x['sent'].replace('<SEP> ', '').split(' ')[int(x['pred'])], axis=1)

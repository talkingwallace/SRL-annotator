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

def start_a_project(file_path,project_name='default',):

    data_name = project_name
    if os.path.exists(data_name):
        os.rmdir(data_name)
    data = shelve.open(data_name,writeback=True)

    f = open(file_path,'r',encoding='utf-8')
    sents = f.read().split('\n')
    if sents[-1] == '':
        sents = sents[:-1]
    sents = set(sents)

    data['id2sent'] = {hash(v):v for idx,v in enumerate(sents)}
    data['sent2id'] = {v:hash(v) for idx,v in enumerate(sents)}
    data['annotation'] = pd.DataFrame({'sentid':[],'pred':[],'args':[],'sent':[]})
    # 'timestamp':[]
    data['done'] = set()
    data.sync()

    return data

def start_a_task(data:DbfilenameShelf,sent_ids:set):

    assert sent_ids.issubset(set(data['id2sent'].keys()))
    data['todo'] = sent_ids


def save_annotations(data:DbfilenameShelf,sent_id:int,pred_idx:int,arg:dict):

    assert sent_id in data['id2sent']

    new_row = pd.DataFrame({'sentid':[sent_id],'pred':[pred_idx],'args':[arg],'sent':[data['id2sent'][sent_id]]})
    # 'timestamp':[str(time.time())]
    data['annotation'] = data['annotation'].append(new_row)
    data.sync()

def commit(data:DbfilenameShelf,sent_id):
    data['done'].add(sent_id)
    print(sent_id,'added into done')
    data.sync()


def load_database(project_name:str):

    if not os.path.exists(project_name+'.dat'):
        return None
    data = shelve.open(project_name,writeback=True)
    return data

def check_all_annotation(data:DbfilenameShelf):
    return data['annotation']

def output_annotations(data:DbfilenameShelf):
    df:pd.DataFrame = data['annotation']
    out_name = './result/' + 'result' + str(int(time.time())) + '.txt'
    outf = open(out_name, 'a+', encoding='utf-8')
    a = df.reset_index()
    sent_id_set = set(a['sentid'])
    new_record = {}
    for sent_id in sent_id_set:
        new_record['sentid'] = sent_id
        srl_list = []
        same_id_df = a[a['sentid'] == sent_id]
        for i, row in same_id_df.iterrows():
            srl_tmp_pred = set([d['pred'] for d in srl_list])
            tmp_pred = int(row['pred'])
            if tmp_pred not in srl_tmp_pred:
                tmp_dict = {}
                tmp_dict['pred'] = int(row['pred'])
                tmp_dict['args'] = row['args']
                srl_list.append(tmp_dict)
            else:
                for d in srl_list:
                    if d['pred'] == tmp_pred:
                        d['args'] = row['args']
        new_record['srl'] = srl_list
        new_record['sent'] = same_id_df.iloc[0]['sent']
        json_str = json.dumps(new_record, ensure_ascii=False)
        outf.write(json_str + '\n')
    outf.close()

class DataManager(object):

    def __init__(self,project_name,file_path=None,):

        self.data = load_database(project_name)
        if self.data is None:
            self.data = start_a_project(file_path,project_name)
        self.todo = list(set(self.data['id2sent'].keys()).difference(self.data['done']))
        self.cur_idx = 0

    def fetch_next(self,):
        return self.todo[self.cur_idx]

    def commit(self,):

        sent_id = self.todo[self.cur_idx]
        commit(self.data, sent_id)
        self.cur_idx += 1

    def save(self,sent_id:int,pred_idx:int,arg:dict):
        save_annotations(self.data,sent_id,pred_idx,arg)


if __name__ == '__main__':

    # data = start_a_project(file_path='./to_annotate/dev2.txt')
    # data = load_database('default')
    datamanager = DataManager('default')
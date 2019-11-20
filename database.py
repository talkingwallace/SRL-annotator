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
    data['annotation'] = pd.DataFrame({'sentid':[],'pred':[],'args':[],'timestamp':[]})
    data['done'] = set()
    data.sync()

    return data

def start_a_task(data:DbfilenameShelf,sent_ids:set):

    assert sent_ids.issubset(set(data['id2sent'].keys()))
    data['todo'] = sent_ids


def save_annotations(data:DbfilenameShelf,sent_id:int,pred_idx:int,arg:dict):

    assert sent_id in data['id2sent']

    new_row = pd.DataFrame({'sentid':[sent_id],'pred':[pred_idx],'args':[arg],'timestamp':[str(time.time())]})
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

def output_annotations():
    pass

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
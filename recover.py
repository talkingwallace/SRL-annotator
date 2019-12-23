import database
import json


def recover(file_path, original_data_path, project_name='default'):
    """
    recover data from json output file
    """
    dm = database.DataManager(project_name, original_data_path)
    sent2id = dm.data['sent2id']
    f = open(file_path, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        record = json.loads(line)
        srl, sent = record['srl'], record['sent']
        sentid = sent2id[sent]
        for srl_item in srl:
            pred, arg = srl_item['pred'], srl_item['args']
            dm.save(sentid, pred, arg)
        dm.commit(sentid)


recover('xu_result.txt', 'to_annotate/xu.txt', 'xu')

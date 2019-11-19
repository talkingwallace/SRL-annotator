import argparse
import json
import re
import database as db
from shelve import DbfilenameShelf

spliter = lambda x: x.strip().split(',')
punctuation = ['。', '，', '？', '&', '！', '@', '；', '（', '）', '、']


def get_annotated_num(out_file):
    return len(out_file.readlines())


def main(data:DbfilenameShelf):

    print('=' * 50)
    todo = set(data['id2sent'].keys()).difference(data['done'])
    for sentid in todo:

        print('{} Sentences to go'.format(len(todo)))
        record = data['id2sent'][sentid]
        record = record.split(' ')
        i = 0
        conversation = ''
        for word in record:
            # conversation = conversation.split(' ')
            # conversation = [word + '(' + str(i + j) + ')' if word not in punctuation else word
            #                 for (j, word) in enumerate(conversation)]
            # i += len(conversation)
            # conversation = ' '.join(conversation)
            if word in punctuation:
                conversation += word
                continue
            if word == '<SEP>':
                conversation += '\n'
                continue

            conversation += word+'({}) '.format(i)
            i += 1

        print(conversation)
        item_dict = dict()
        item_dict['id'] = i
        item_dict['srl'] = list()
        flag = True
        while flag:
            pred = input('Enter the predicate index:')
            if re.match('^\d+$', pred):
                tmp_dict = dict()
                pred = int(pred)
                arg0 = input('Enter ARG0 start and end index (split by ,):')
                arg1 = input('Enter ARG1 start and end index (split by ,):')
                arg2 = input('Enter ARG2 start and end index (split by ,):')
                arg3 = input('Enter ARG3 start and end index (split by ,):')
                arg4 = input('Enter ARG4 start and end index (split by ,):')
                tmp = input('Enter TMP start and end index (split by ,):')
                loc = input('Enter LOC start and end index (split by ,):')
                prp = input('Enter PRP start and end index (split by ,):')
                tmp_dict['pred'] = pred
                if arg0:
                    tmp_dict['arg0'] = (int(spliter(arg0)[0]), int(spliter(arg0)[1]))
                if arg1:
                    tmp_dict['arg1'] = (int(spliter(arg1)[0]), int(spliter(arg1)[1]))
                if arg2:
                    tmp_dict['arg2'] = (int(spliter(arg2)[0]), int(spliter(arg2)[1]))
                if arg3:
                    tmp_dict['arg3'] = (int(spliter(arg3)[0]), int(spliter(arg3)[1]))
                if arg4:
                    tmp_dict['arg4'] = (int(spliter(arg4)[0]), int(spliter(arg4)[1]))
                if tmp:
                    tmp_dict['tmp'] = (int(spliter(tmp)[0]), int(spliter(tmp)[1]))
                if loc:
                    tmp_dict['loc'] = (int(spliter(loc)[0]), int(spliter(loc)[1]))
                if prp:
                    tmp_dict['prp'] = (int(spliter(prp)[0]), int(spliter(prp)[1]))
                item_dict['srl'].append(tmp_dict)

            else:
                print('Invalid value {}'.format(pred))
            while True:
                next_pred = input('Are there other predicates [Y/n]')
                if next_pred.lower() == 'n':
                    for dic in item_dict['srl']:
                        pred_idx = dic['pred']
                        dic.pop('pred')
                        db.save_annotations(data,sentid,pred_idx,dic,commit=True)
                    flag = False
                    break
                if next_pred.lower() == 'y' or next_pred.lower() is None:
                    break


if __name__ == '__main__':

    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-project_name", type=str, required=True, default='default')
    arg_parse.add_argument("-file_path", type=str, help='Please specify the input file, if a project is not created'
                                                      , required=False)

    config = arg_parse.parse_args()
    file_path = config.file_path
    project_name = config.project_name

    # file_path = r'E:\tencent_nlp\SRL-annotator\to_annotate\dev2.txt'
    # project_name = 'default'

    data = db.load_database(project_name)
    if data is None:
        data = db.start_a_project(file_path,project_name)

    main(data)

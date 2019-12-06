import os
import pandas as pd

from IPython.core.display import display, HTML

from database import DataManager
import traceback

verbs = None
if os.path.exists('./to_annotate/verb.txt'):
    verb_f = open('./to_annotate/verb.txt', 'r', encoding='utf-8')
    verbs = verb_f.read().split('\t\n')[:-1]


def search_by_index(dm: DataManager, index):
    pass


def search_by_pred(dm: DataManager, pred: str):
    res = dm.search_by_pred(pred)


def load_data(dm, sentid):
    data = dm.data
    punctuation = ['。', '，', '？', '&', '！', '@', '；', '（', '）', '、']
    record = data['id2sent'][sentid]
    record = record.split(' ')
    i = 0
    conversation = ''
    predicate_suggests = []
    sent_words = []
    for word in record:
        if word in punctuation:
            conversation += word
            i += 1
            sent_words.append(word)
            continue
        if word == '<SEP>':
            conversation += '<br>'
            continue
        new_append = word + '({}) '.format(i)
        sent_words.append(word)
        if verbs and word in verbs:
            predicate_suggests.append(new_append)
            new_append = '<b>' + new_append + '</b>'
        conversation += new_append
        i += 1
    display(HTML(conversation))
    print('possible predicate:')
    print(predicate_suggests)
    if sentid in data['done']:
        print('Done labels:')
        done_labels_df: pd.DataFrame = data['annotation']
        selected_df = done_labels_df[done_labels_df['sentid'] == sentid]
        for i, row in selected_df.iterrows():
            try:
                pred = int(row['pred'])
                args = row['args']
                args_str = 'pred: {}({})\t'.format(sent_words[pred], pred)
                for arg in args.keys():
                    arg_b_index, arg_e_index = args[arg][0], args[arg][1]
                    if arg_b_index == -1:
                        args_str += '{}: {}\t'.format(arg, '我(-1)')
                    elif arg_b_index == -2:
                        args_str += '{}: {}\t'.format(arg, '你(-2)')
                    else:
                        args_str += '{}: {}({},{})\t'.format(arg, ''.join(sent_words[arg_b_index:arg_e_index + 1]),
                                                             arg_b_index, arg_e_index)
                print(args_str)

            except:
                print('Error occurs in done labels. Please check!')
                traceback.print_exc()


def display_all(dm: DataManager, box_list: list):
    for box in box_list:
        display(box)
    print('progress:{}/{}'.format(dm.cur_idx, dm.total_sent))

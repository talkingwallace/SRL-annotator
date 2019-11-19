import argparse
import json
import re

spliter = lambda x: x.strip().split(',')


def main():
    print('=' * 50)
    in_file = open(in_path, 'r', encoding='utf-8')
    out_file = open(out_path, 'a+', encoding='utf-8')

    start_index = 0  # get from out file's length

    lines = in_file.readlines()
    for i in range(start_index, len(lines)):
        record = json.loads(lines[i].strip())
        conversations = record['conversation']
        document = ''.join(conversations).strip().split(' ')
        document = [word + '_' + str(i) for (i, word) in enumerate(document)]
        print('Sentences {}/{}'.format(i + 1, len(lines)))
        print(' '.join(document))
        item_dict = dict()
        item_dict['id'] = i
        item_dict['srl'] = list()
        while True:
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
            next_pred = input('Are there other predicates [Y/n]')
            if next_pred.lower() == 'n':
                out_file.write(json.dumps(item_dict))
                break


if __name__ == '__main__':
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-in_path", type=str, help='Please specify the input file.', required=True)
    arg_parse.add_argument("-out_path", type=str, required=False, default='out.txt')
    arg_parse.add_argument('-author', type=str, required=True)

    config = arg_parse.parse_args()
    in_path = config.in_path
    out_path = config.out_path
    main()

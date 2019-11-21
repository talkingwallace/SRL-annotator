import json

def combine_conv(conv:list):

    """
    merge conversations into one string
    """

    full_sent = ''
    for sent in conv:
        if sent[-1] != ' ':
            sent += ' '
        full_sent += sent + '<SEP> '
    return full_sent[:-1]

def format_transform(in_name,out_name):
    out = out_name
    a = open(in_name, 'r', encoding='utf-8')
    lines = a.read().split('\n')
    out_f = open(out, 'w', encoding='utf-8')
    for l in lines[:-1]:
        try:
            dic = json.loads(l)
            key = 'conversation' if 'history' not in dic else 'history'
            sent = combine_conv(dic[key])
            out_f.write(sent + '\n')
        except:
            pass
    out_f.close()
    a.close()

def gather(in_list:list):
    result = []
    for name in in_list:
        f = open(name,'r',encoding='utf-8')
        string = f.read()
        data = string.split('\n')[:-1]
        result += data
        f.close()
    return result

def split(data,ratio=0.25,):
    total = len(data)
    len_ = int(total*ratio) + 1
    a = []
    up = total
    while up >= 0:
        a.append(up)
        up -= len_
    a.append(0)
    a = list(reversed(a))

    out_idx = 0
    for start,end in zip(a[:-1],a[1:]):
        data_frac = data[start:end]
        out_f = open(str(out_idx)+'.txt','w',encoding='utf-8')
        for sent in data_frac:
            out_f.write(sent+'\n')
        out_idx += 1
        out_f.close()
    print('done')

if __name__ == '__main__':
    # in_name = ['dev.txt','test_1.txt','test_2.txt','train.txt']
    # out_name = ['dev_.txt','test_1_.txt','test_2_.txt','train_.txt']
    # divide_name = ['chen.txt','wu.txt','xu.txt','song.txt']
    # for in_,out_ in zip(in_name,out_name):
    #     format_transform(in_,out_)
    # all_data = gather(out_name)
    # split(all_data,0.25)

    f = open(r'C:\Users\Administrator\SRL-annotator\to_annotate\chen.txt','r',encoding='utf-8')
    a = f.read()

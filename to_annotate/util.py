import json
def combine_conv(conv:list):

    """
    merge conversations into one string
    """

    full_sent = ''
    for sent in conv:
        if sent[-1] != ' ':
            sent += ' '
        full_sent += sent
    return full_sent[:-1]

if __name__ == '__main__':
    out = 'dev2.txt'
    a = open('dev.txt','r',encoding='utf-8')
    lines = a.read().split('\n')
    out_f = open(out,'w',encoding='utf-8')
    for l in lines[:-1]:
        dic = json.loads(l)
        key = 'conversation' if 'history' not in dic else 'conversation'
        sent = combine_conv(dic[key])
        out_f.write(sent+'\n')
    out_f.close()
    a.close()
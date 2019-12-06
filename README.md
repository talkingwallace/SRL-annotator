# Guide

- open 'interface.ipynb' using jupyter notebook

- you can modify line 'dm = db.DataManager('default','./to_annotate/dev2.txt')'. The first parameter is the name of 
  
  project, the second is the path of file in which sentences are separated by '\n'
  
- execute code in the cell(ALT+ENTER) to start

- The format of output records (json list):
``{'sentid': sent_id, 'srl': [{'pred': 0, 'args':{'arg0': [], 'arg1': []}}, {'pred': 1, ...}, {'pred': 2, ...}, ...], 'sent': sentence}``

用法说明:

- Pred submit 每标注完一个pred后点击，自动保存标注记录

- Sentence finish 标注完一个句子后点击，并直接跳转到下一个句子

- Output result to json 输出到外部文件

- prev 查看前一个句子

- next 查看后一个已标注句子，无法查看未标注句子

- jump to 跳转到第n个句子，0<= n <= 当前待标记句子index(已标记句子总数)；若n>当前待标记句子index，跳转到待标记句子

- 修改： 若某pred标记错误，想修改该pred的标注信息，直接重新标注一遍该pred并pred submit以及sentence finish即可完成

如果发现有多条未标记句子，属于正常现象，因为前期数据存储结构的设计问题，导致之前标记的有些数据不是按顺序出现，并不影响最后的标注效果。
这种情况也可以通过一直pred submit，完成句子标记后不点sentence finish，直接next到下一条句子即可解决。该bug后续将会解决。
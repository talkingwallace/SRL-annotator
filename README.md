# Guide

- open 'interface.ipynb' using jupyter notebook

- you can modify line 'dm = db.DataManager('default','./to_annotate/dev2.txt')'. The first parameter is the name of 
  
  project, the second is the path of file in which sentences are separated by '\n'
  
- execute code in the cell(ALT+ENTER) to start

- The format of output records (json list):
``{'sentid': sent_id, 'srl': [{'pred': 0, 'args':{'arg0': [], 'arg1': []}}, {'pred': 1, ...}, {'pred': 2, ...}, ...], 'sent': sentence}``
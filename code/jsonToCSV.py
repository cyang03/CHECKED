#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 23:50:56 2020

@author: phabby
"""

import json
import csv
import glob

result = []
for f in glob.glob('*.json'):
    with open(f,'r') as infile:
        try:
            result.append(json.load(infile))
        except ValueError:
            print(f)

with open('merge_total.json','w', encoding = 'utf8') as outfile:
    json.dump(result, outfile, ensure_ascii=False)
    
with open('merge_total.json') as file:
    data = json.load(file)

f = csv.writer(open('total.csv','w',newline=''))
f.writerow(['label','id','date','user_name','user_id','text','pic_url','video_url','comments_num','repost_num','like_num'])
for data in data:
    f.writerow([data['label'],
                data['id'],
                data['date'],
                data['user_name'],
                data['user_id'],
                data['text'],
                data['pic_url'],
                data['video_url'],
                data['comments_num'],
                data['repost_num'],
                data['like_num']])
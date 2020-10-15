#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as r
from bs4 import BeautifulSoup
import json
import time
from urllib import parse
import re

keywords = ['冠状病毒','新冠肺炎','新冠','疫情','疫区','传染','感染','确诊','死亡病例','输入病例','输入性传播','世界卫生组织','世卫','钟南山','张文宏','李文亮','福奇','口罩','试剂盒','核酸检测','疫苗','抗体','火神山','雷神山','隔离','封城','防控','群体免疫','健康码','健康宝','战疫','抗疫','援鄂','coronavirus','sars-cov-2','covid','who','cdc']
#pastkey = []
headers = {
        'cookie': '',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        
	}


def get_first_part_weibos():
    for key in keywords:
        
         page = 1;
         params = {
                 'pids': 'Pl_Official_MyProfileFeed__27',
                 'is_search': '1',
                 'visible': '0',
                 'is_tag': '0',
                 'profile_ftype': '1',
                 'page':page,
                 'is_ori': '1',
                 'is_forward': '1',
                 'is_text': '1',
                 'is_pic': '1',
                 'is_video': '1',
                 'key_word': key,
                 'start_time': '2019-12-01',
                 'end_time': '2020-08-31',
                 'is_search': '1',
                 'is_searchadv': '1',
                 'ajaxpagelet': '1',
                 'ajaxpagelet_v6': '1'}
         
         url = 'https://weibo.com/rmrb?'+parse.urlencode(params)
         res =r.get(url=url,headers=headers,params=params,allow_redirects=False,timeout = 20)
         
         temp = str(res.text).replace('<script>parent.FM.view(','')
         json_string = temp.replace(')</script>','')
         
         data = json.loads(json_string)
         soup = BeautifulSoup(data['html'],'html.parser')
         
         parse_weibo(soup)
         
         pagebar = 0 
         
         while(1):
             if soup.select_one('p.text > i.W_loading'):
                 time.sleep(10)
                 print('sleep 5')
                 soup = get_next_part_weibos(key,pagebar,page)
                 pagebar = pagebar + 1
            
             elif soup.select_one('div.W_pages > a.next'):
                page = page + 1
                soup = get_next_page_weibos(key,page)
                pagebar = 0
            
             else:
                break
            
             time.sleep(1)
         time.sleep(10)
         
def get_next_page_weibos(key,page):
    next_page_params = {'pids': 'Pl_Official_MyProfileFeed__27',
                        'is_search': '1',
                        'visible': '0',
                        'is_tag': '0',
                        'profile_ftype': '1',
                        'page':page,
                        'is_ori': '1',
                        'is_forward': '1',
                        'is_text': '1',
                        'is_pic': '1',
                        'is_video': '1',
                        'key_word': key,
                        'start_time': '2019-12-01',
                        'end_time': '2020-08-31',
                        'is_search': '1',
                        'is_searchadv': '1',
                        'ajaxpagelet': '1',
                        'ajaxpagelet_v6': '1'}
    
    next_page_url = 'https://weibo.com/rmrb?'+parse.urlencode(next_page_params)
    next_page_res =r.get(url=next_page_url,headers=headers,params=next_page_params,allow_redirects=False,timeout=20)
    time.sleep(5)
    print('sleep 5')
    
    if next_page_res.status_code in [302,504]:
        time.sleep(40)
        next_page_res =r.get(url=next_page_url,headers=headers,params=next_page_params,allow_redirects=False)
        
    
    temp = str(next_page_res.text).replace('<script>parent.FM.view(','')
    json_string = temp.replace(')</script>','')
    
    data = json.loads(json_string)
    soup = BeautifulSoup(data['html'],'html.parser')
    parse_weibo(soup)
    
    return soup

def get_next_part_weibos(key,pagebar,page):
    next_part_params = {
            'ajwvr': '6',
            'domain': '100206',
            'is_ori': '1',
			'is_forward': '1',
			'is_text': '1',
			'is_pic': '1',
			'is_video': '1',
			'key_word': key,
			'start_time': '2019-01-01',
			'end_time': '2020-08-31',
			'is_search': '1',
			'is_searchadv': '1',
			'pagebar': str(pagebar),
			'pl_name': 'Pl_Official_MyProfileFeed__27',
			'id': '1002062803301701',
			'script_uri': '/rmrb',
			'feed_type': '0',
			'page': str(page),
			'pre_page': str(page),
			'domain_op': '100206',
			'profile_ftype': '1',
			'is_tag': '0'
				}
    next_part_url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?'+parse.urlencode(next_part_params)
    next_part_res = r.get(url=next_part_url,params=next_part_params,headers=headers,allow_redirects=False)
    time.sleep(10)
    
    if next_part_res.status_code in [302,504]:
        time.sleep(40)
        next_part_res = r.get(url=next_part_url,params=next_part_params,headers=headers,allow_redirects=False)
        
    
    next_part_json = json.loads(next_part_res.text)
    next_part_soup = BeautifulSoup(next_part_json['data'],'html.parser')
    
    parse_weibo(next_part_soup)
    return next_part_soup

def check_num(s):
    if s in ['转发','评论','赞']:
        return '0'
    else:
        return s
    
def get_first_page_comments(mid):
    comments = []
    comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+mid+'&from=singleWeiBo'
    
    comment_params = {
        'ajwvr': '6',
		'id': mid,
		'from': 'singleWeiBo'}

    res = r.get(url=comment_url,params=comment_params,headers=headers)
    temp_json = json.loads(res.text)
    soup = BeautifulSoup(temp_json['data']['html'],'html.parser')
    
    for comment in soup.select('div[node-type="root_comment"]'):
        comment_dict = {
                "id":"",
                "date":"",
                "user_name":"",
                "user_id":"",
                "text":"",
                "pic_url":""
                }
        
        comment_dict['id'] = str(comment['comment_id'])
        raw_date = comment.select_one('div.WB_func > div.WB_from').string
        if raw_date[0:4] == '2019':
            comment_dict['date'] = '2019-'+ raw_date.replace('月', '-').replace('日', '')
        else:
            comment_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        comment_dict['user_name'] = comment.select_one('div.WB_text > a').string
        comment_dict['user_id'] = str(comment.select_one('div.WB_text > a')['href']).split('/')[-1]
        for child in comment.select_one('div.list_con > div.WB_text').children:
            if str(child).startswith('：'):
                comment_dict['text'] = str(child)[1:].strip()
                break
        if comment.select_one('li[action-type="comment_media_img"] > img'):
            comment_dict["pic_url"] = 'https:'+comment.select_one('li[action-type="comment_media_img"] > img')['src']
            
        comments.append(comment_dict)

        
    
    num = 1
    while(1):
        time.sleep(1)
        param_string = ''
        if soup.select_one('div[node-type="comment_loading"]'):

            param_string = soup.select_one('div[node-type="comment_loading"]')['action-data']
            
        elif soup.select_one('a[action-type="click_more_comment"]'):
            param_string = soup.select_one('a[action-type="click_more_comment"]')['action-data']
            
        else:
            break
        
        if num > 257:
            time.sleep(25)
            break
        
        num = num + 1
        param_lst=re.compile('=(.*?)&').findall(param_string)
        next_page_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'+param_string+'&from=singleWeiBo'
        paramters = {
            'ajwvr': '6',
			'id': param_lst[0],
			'root_comment_max_id':param_lst[1],
			'root_comment_max_id_type':param_lst[2],
			'root_comment_ext_param':param_lst[3],
			'page': param_lst[4],
			'filter': param_lst[5],
			'sum_comment_number':param_lst[6],
			'from': 'singleWeiBo'}
        
        try:
             __res = r.get(url=next_page_url,params=paramters,headers=headers,allow_redirects=False)

             temp_json2 = json.loads(__res.text)
             soup2 = BeautifulSoup(temp_json2['data']['html'],'html.parser')
             comments = comments + get_next_page_comments(soup2)
             soup = soup2
        except:
            print('comment error: get a rest')
            time.sleep(65)
            break
    
    return comments

def get_next_page_comments(soup):
    comments = []
    
    for comment in soup.select('div[node-type="root_comment"]'):
        comment_dict = {
                "id":"",
                "date":"",
                "user_name":"",
                "user_id":"",
                "text":"",
                "pic_url":""
                }
        comment_dict['id'] = str(comment['comment_id'])
        raw_date = comment.select_one('div.WB_func > div.WB_from').string
        if raw_date[0:4] == '2019':
            comment_dict['date'] = '2019-'+ raw_date.replace('月', '-').replace('日', '')
        else:
            comment_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        comment_dict['user_name'] = comment.select_one('div.WB_text > a').string
        comment_dict['user_id'] = str(comment.select_one('div.WB_text > a')['href']).split('/')[-1]
        
        for child in comment.select_one('div.list_con > div.WB_text').children:
            if str(child).startswith('：'):
                comment_dict['text'] = str(child)[1:].strip()
                break
        if comment.select_one('li[action-type="comment_media_img"] > img'):
            comment_dict["comment_pic_url"] = 'https:'+comment.select_one('li[action-type="comment_media_img"] > img')['src']
        
        comments.append(comment_dict)
        #time.sleep(1)
        
    return comments

def get_reposts(mid):
    reposts = []
    
    s = r.Session()
    url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+mid
    
    params = {
            'ajwvr': '6',
            'id': mid}
    res = s.get(url=url,params=params,headers=headers,allow_redirects=False)

    temp = json.loads(res.text)
    
    soup2 = BeautifulSoup(temp['data']['html'],'html.parser')
    total_page = temp['data']['page']['totalpage']
    
    if not(soup2.select('div[action-type="feed_list_item"]')):
        return reposts
    
    for repost in soup2.select('div[action-type="feed_list_item"]'):
        repost_dict = {
                "id":"",
                "date":"",
				"user_name":"",
				"user_id":"",
				"text":"",
                "pic_url":[]}
        
        repost_dict['id'] = str(repost['mid'])
        raw_date = repost.select_one('div.WB_func > div.WB_from').get_text()
        if raw_date[0:4] == '2019':
            repost_dict['date'] = '2019-'+ raw_date.replace('月', '-').replace('日', '')
        else:
            repost_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        repost_dict['user_name'] = repost.select_one('div.WB_text > a').string
        repost_dict['user_id'] = str(repost.select_one('div.WB_text > a')['href']).split('/')[-1]
        repost_dict['text'] = repost.select_one('span[node-type="text"]').get_text()
        
        if repost.select('li[action-type="comment_media_img"] > img'):
            for repost_pic in repost.select('li[action-type="comment_media_img"] > img'):
                repost_dict['pic_url'].append('https:'+ repost_pic['src'])
                
        reposts.append(repost_dict)

   
    if soup2.select_one('div.between_line'):
        max_id = soup2.select_one('div.between_line').next_sibling.next_sibling['mid']
    else:
        max_id = soup2.select('div[action-type="feed_list_item"]')[0]['mid']
            
    page = 1
    for i in range(total_page-1):
        time.sleep(1)
        page = page + 1
        next_reposts_url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+mid+'&max_id='+max_id+'&page='+str(page)
        print(next_reposts_url)
        next_reposts_params = {
                'ajwvr': '6',
                'id': mid,
                'max_id': max_id,
                'page': str(page)}
        if page > 277:
            time.sleep(28)
            break
        
        try:
            
            next_reposts_res = s.get(url=next_reposts_url,params=next_reposts_params,headers=headers,allow_redirects=False)
            temp_json = json.loads(next_reposts_res.text)
            soup3 = BeautifulSoup(temp_json['data']['html'],'html.parser')
            
            for __repost in soup3.select('div[action-type="feed_list_item"]'):
                repost_dict2 = {
                        "id":"",
                        "date":"",
                        "user_name":"",
                        "user_id":"",
                        "text":"",
                        "pic_url":[]}

                repost_dict2['id'] = str(__repost['mid'])
                raw_date = __repost.select_one('div.WB_func > div.WB_from').get_text()
                if raw_date[0:4] == '2019':
                    repost_dict2['date'] = '2019-'+ raw_date.replace('月', '-').replace('日', '')
                else:
                    repost_dict2['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
                repost_dict2['user_name'] = __repost.select_one('div.WB_text > a').string
                repost_dict2['text'] = __repost.select_one('span[node-type="text"]').get_text()
                
                if __repost.select('li[action-type="comment_media_img"] > img'):
                    for __repost_pic in __repost.select('li[action-type="comment_media_img"] > img'):
                        repost_dict2['pic_url'].append('https:'+ __repost_pic['src'])
    
                reposts.append(repost_dict2)
        except:
            print("repost error: get a rest")
            time.sleep(68)
            break
            
            
    return reposts

def parse_weibo(soup):
    num = 0
    for weibo in soup.select('div[action-type="feed_list_item"]'):
        num = num + 1
       
        weibo_data={
                "label" : "real",
                'id':"",
				"date":"",
				"user_name":"人民日报",
				"user_id":"2803301701",
				"text":"",
				"pic_url":[],
				"video_url":"",
				"comments_num":"",
				"repost_num":"",
				"like_num":"",
				"comments":[],
				"reposts":[]}
        
        weibo_data['id'] = weibo['mid']
        weibo_data['date'] = weibo.select_one('a[node-type="feed_list_item_date"]')['title']
        if weibo.select_one('a[action-type="fl_unfold"]'):

            full_text_params = {
                    'ajwvr': '6',
                    'mid': weibo_data['id'],
                    'is_settop': '',
                    'is_sethot': '',
                    'is_setfanstop': '',
                    'is_setyoudao': '',
                    'is_from_ad': '0'}
            full_text_url = 'https://weibo.com/p/aj/mblog/getlongtext?'+parse.urlencode(full_text_params)
            full_text_res = r.get(url=full_text_url,params=full_text_params,headers=headers)
            
            try:
                full_text_res.raise_for_status()
                full_text_json = json.loads(full_text_res.text)
                full_text_soup = BeautifulSoup(full_text_json['data']['html'],'html.parser')
                weibo_data['text'] = full_text_soup.get_text().strip()
                print(weibo_data['text'])
                '''for key in pastkey:
                    if key in weibo_data['text']:
                        have_keyword = have_keyword + 1
                        
                if have_keyword != 0:
                    continue'''
            except:
                weibo_data['text'] = weibo.select_one('div[node-type="feed_list_content"]').get_text().strip()
                print(weibo_data['text'])
                '''for key in pastkey:
                    if key in weibo_data['text']:
                        have_keyword = have_keyword + 1
                        #break
                if have_keyword != 0:
                    continue'''
        else:
            weibo_data['text'] = weibo.select_one('div[node-type="feed_list_content"]').get_text().strip()
            print(weibo_data['text'])
            '''for key in pastkey:
                if key in weibo_data['text']:
                    have_keyword = have_keyword + 1
                    #break
            if have_keyword != 0:
                continue'''
        if weibo.select('li[action-type="fl_pics"]'):
            for pic in weibo.select('li[action-type="fl_pics"] > img'):
                weibo_data['pic_url'].append('https:'+pic['src'])
        elif weibo.select_one('li[action-type="feed_list_media_img"]'):
            __pic = weibo.select_one('li[action-type="feed_list_media_img"] img')
            weibo_data['pic_url'].append('https:'+__pic['src'])
        else:
            print('\t\t图片url获取结果：该微博没有图片')
            
        if weibo.select_one('li[node-type="fl_h5_video"]'):
            try:
                video_source = weibo.select_one('li[node-type="fl_h5_video"]')['video-sources']
                encoded_video_url=re.compile('=(.*?)=').findall(video_source)[0]
                weibo_data['video_url'] = parse.unquote(parse.unquote(encoded_video_url))
            except KeyError:
                print('存在直播内容，跳过')
        else:
            print('\t\t视频url获取结果：该微博没有视频')
        weibo_data['comments_num'] = check_num(weibo.select('span[node-type="comment_btn_text"] em')[-1].string)
        weibo_data['repost_num'] = check_num(weibo.select('span[node-type="forward_btn_text"] em')[-1].string)
        weibo_data['like_num'] = check_num(weibo.select('span[node-type="like_status"] em')[-1].string)
        
        json_str = json.dumps(weibo_data,ensure_ascii=False)
        with open(weibo_data['id']+'.json', 'w') as json_file:
            json_file.write(json_str)
        
        if eval(weibo_data['comments_num']) > 0:
            weibo_data['comments'] = get_first_page_comments(weibo_data['id'])
            
        json_str = json.dumps(weibo_data,ensure_ascii=False)
        with open(weibo_data['id']+'.json', 'w') as json_file:
            json_file.write(json_str)

        if eval(weibo_data['repost_num']) > 0:
            weibo_data['reposts'] = get_reposts(weibo_data['id'])
            
        print('转发写入json文件...')
        json_str = json.dumps(weibo_data,ensure_ascii=False)
        with open(weibo_data['id']+'.json', 'w') as json_file:
            json_file.write(json_str)
        
        time.sleep(35)



get_first_part_weibos()

            
            
        
    
    
        
        
         
         
         
         
         
         

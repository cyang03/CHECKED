#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests as r
from bs4 import BeautifulSoup
import json
import time
from urllib import parse
import re

keywords = ['冠状病毒','新冠肺炎','新冠','疫情','疫区','传染','感染','确诊','死亡病例','输入病例','输入性传播','世界卫生组织','世卫','钟南山','张文宏','李文亮','福奇','口罩','试剂盒','核酸检测','疫苗','抗体','火神山','雷神山','隔离','封城','防控','群体免疫','健康码','健康宝','战疫','抗疫','援鄂','coronavirus','sars-cov-2','covid','who','cdc']
headers = {
        'cookie': '',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        
	}

def get_reports():

    for page in range(1,60):
        url = 'https://service.account.weibo.com/index?type=5&status=0&page='+str(page)
        params = {
                'type': '5',
                'status': '4',
                'page': str(page)
                }
        res = r.get(url=url,params=params,headers=headers)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text,'html.parser')
        temp = str(soup.select('script')[-1]).replace('<script>STK && STK.pageletM && STK.pageletM.view(','')
        json_string = temp.replace(')</script>','')
        data = json.loads(json_string)
        soup2 = BeautifulSoup(data['html'],'html.parser')
 
        num = 0 
        for item in soup2.select('div.m_table_tit > a'):      
            num = num + 1
            
            report_link = 'https://service.account.weibo.com'+item['href']
            
            rid = item['href'].replace('/show?rid=','')
            params2 = {
                    'rid':rid
                    }
            res2 = r.get(url=report_link,headers=headers,params=params2)

            res.encoding = res.apparent_encoding
            soup3 = BeautifulSoup(res2.text,'html.parser')

            _temp = str(soup3.select('script')[-6]).replace('<script>STK && STK.pageletM && STK.pageletM.view(','')
            json_string2 = _temp.replace(')</script>','')
   
            data2 = json.loads(json_string2)
            soup4 = BeautifulSoup(data2['html'],'html.parser')
            
            if soup4.select_one('p.publisher > a'):
                org_weibo_url = soup4.select_one('p.publisher > a')['href']
                get_weibo_info(org_weibo_url)
            else:
                print('微博原文不存在')
                continue

def check_num(s):
    if s in ['转发','评论','赞']:
        return '0'
    else:
        return s
    
def get_weibo_info(org_weibo_url):
    time.sleep(9)
    url = org_weibo_url.replace('http','https') + '?type=comment'
    params = {
            'type': 'comment'
            }
    res = r.get(url=url,headers=headers,params=params,timeout=30)
    print('\t\t正在请求微博内容，状态码为{}'.format(res.status_code))
    soup = BeautifulSoup(res.text,'html.parser')
    
    script_item = ''
    for temp_item in soup.select('script')[-4:]:
        if 'pl.content.weiboDetail.index' in str(temp_item):
            script_item = str(temp_item)
            break
        
    temp = script_item.replace('<script>FM.view(','')
    json_string = temp.replace(')</script>','')
    data = json.loads(json_string,strict=False)
    
    soup2 = BeautifulSoup(data['html'],'html.parser')

    weibo_content = soup2.select_one('div[node-type="feed_list_content"]').get_text()
    have_keyword = 0
    for key in keywords:
        if key in weibo_content:
            have_keyword = 1
            break
    if have_keyword == 1:
        print(weibo_content)
        full_data = {
                    "label" : "fake",
                    'id':"",
					"date":"",
					"user_name":"",
					"user_id":"",
					"text":"",
					"pic_url":[],
					"video_url":"",
					"comments_num":"",
					"repost_num":"",
					"like_num":"",
					"comments":[],
					"reposts":[]
				}
        full_data['id'] = str(soup2.select_one('div[node-type="root_child_comment_build"]')['mid'])
        full_data['date'] = soup2.select_one('a[node-type="feed_list_item_date"]')['title']
        full_data['user_name'] = soup2.select('div.WB_info > a')[0].string
        full_data['user_id'] = str(soup2.select('div.WB_info > a')[0]['href'].split('/')[-1])
        full_data['text'] = weibo_content.strip()
        
        if soup2.select('li[action-type="fl_pics"]'):
            for pic in soup2.select('li[action-type="fl_pics"] > img'):
                full_data['pic_url'].append('https:'+pic['src'])
        else:
            print('该微博没有图片')
        
        if soup2.select_one('li[node-type="fl_h5_video"]'):
            video_source = soup2.select_one('li[node-type="fl_h5_video"]')['video-sources']
            encoded_video_url=re.compile('=(.*?)=').findall(video_source)[0]
            full_data['video_url'] = parse.unquote(parse.unquote(encoded_video_url))
        else:
            print('该微博没有视频')
            
        full_data['comments_num'] = check_num(soup2.select('span[node-type="comment_btn_text"] em')[-1].string)
        full_data['repost_num'] = check_num(soup2.select('span[node-type="forward_btn_text"] em')[-1].string)
        full_data['like_num'] = check_num(soup2.select('span[node-type="like_status"] em')[-1].string)
        
        if eval(full_data['comments_num']) > 0:
            full_data['comments'] = get_first_page_comments(full_data['id'])
        
        if eval(full_data['repost_num']) > 0:
            full_data['reposts'] = get_reposts(full_data['id'])
        
        json_str = json.dumps(full_data,ensure_ascii=False)
        with open(full_data['id']+'.json', 'w') as json_file:
            json_file.write(json_str)
    
    else:
        print('不存在关键词')
        
def get_first_page_comments(mid):
    comments = []

    comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+mid+'&from=singleWeiBo'
    comment_params = {
		'ajwvr': '6',
		'id': mid,
		'from': 'singleWeiBo',
		}
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
        comment_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        comment_dict['user_id'] = str(comment.select_one('div.WB_text > a')['href']).split('/')[-1]
        comment_dict['user_name'] = comment.select_one('div.WB_text > a').string
        
        for child in comment.select_one('div.list_con > div.WB_text').children:
            if str(child).startswith('：'):
                comment_dict['text'] = str(child).strip()
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
			'from': 'singleWeiBo'
			}
            __res = r.get(url=next_page_url,params=paramters,headers=headers,allow_redirects=False)
            temp_json2 = json.loads(__res.text)
            soup2 = BeautifulSoup(temp_json2['data']['html'],'html.parser')
            comments = comments + get_next_page_comments(soup2)
            soup = soup2
            
    return comments

def get_next_page_comments(soup):
    time.sleep(5)
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
        comment_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        comment_dict['user_id'] = str(comment.select_one('div.WB_text > a')['href']).split('/')[-1]
        comment_dict['user_name'] = comment.select_one('div.WB_text > a').string
        for child in comment.select_one('div.list_con > div.WB_text').children:
            if str(child).startswith('：'):
                comment_dict['text'] = str(child).strip()
                break
        if comment.select_one('li[action-type="comment_media_img"] > img'):
            comment_dict["pic_url"] = 'https:'+comment.select_one('li[action-type="comment_media_img"] > img')['src']
            
        comments.append(comment_dict)
        
    return comments

def get_reposts(mid):
    reposts = []
    s = r.Session()

    url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+mid
    params = {
		'ajwvr': '6',
		'id': mid
	}
    res = s.get(url=url,params=params,headers=headers,allow_redirects=False)
    
    temp = json.loads(res.text)
    soup2 = BeautifulSoup(temp['data']['html'],'html.parser')
    total_page = temp['data']['page']['totalpage']
    
    if not(soup2.select('div[action-type="feed_list_item"]')):
        return reposts
    
    for repost in soup2.select('div[action-type="feed_list_item"]'):
        time.sleep(1)
        repost_dict = {
					"id":"",
                    "date":"",
					"user_name":"",
					"user_id":"",
					"text":"",
                    "pic_url":[]
				}
        repost_dict['id'] = str(repost['mid'])
        raw_date = repost.select_one('div.WB_func > div.WB_from').get_text()
        repost_dict['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
        repost_dict['user_id'] = str(repost.select_one('div.WB_text > a')['href']).split('/')[-1]
        repost_dict['user_name'] = repost.select_one('div.WB_text > a').string
        repost_dict['text'] = repost.select_one('span[node-type="text"]').get_text()
        
        if repost.select('li[action-type="comment_media_img"] > img'):
            for repost_pic in repost.select('li[action-type="comment_media_img"] > img'):
                repost_dict['pic_url'].append('https:'+ repost_pic['src'])                
        
        reposts.append(repost_dict)

    if soup2.select_one('div.between_line'):
        max_id = soup2.select_one('div.between_line').next_sibling.next_sibling['mid']
        print('存在热门转发，max_id为{}'.format(max_id))
    else:
        max_id = soup2.select('div[action-type="feed_list_item"]')[0]['mid']
        
    page = 1
    for i in range(total_page-1):
        page = page + 1
        next_reposts_url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+mid+'&max_id='+max_id+'&page='+str(page)
        print(next_reposts_url)
        next_reposts_params = {
			'ajwvr': '6',
			'id': mid,
			'max_id': max_id,
			'page': str(page)
		}
        next_reposts_res = s.get(url=next_reposts_url,params=next_reposts_params,headers=headers,allow_redirects=False)
        time.sleep(4)
        temp_json = json.loads(next_reposts_res.text)
        soup3 = BeautifulSoup(temp_json['data']['html'],'html.parser')
        
        for __repost in soup3.select('div[action-type="feed_list_item"]'):
            repost_dict2 = {
                    "id":"",
                    "date":"",
                    "user_name":"",
                    "user_id":"",
                    "text":"",
                    "pic_url":[]
                    }
            repost_dict2['id'] = str(__repost['mid'])
            raw_date = __repost.select_one('div.WB_func > div.WB_from').get_text()
            repost_dict2['date'] = '2020-0'+ raw_date.replace('月', '-').replace('日', '')
            repost_dict2['user_name'] = __repost.select_one('div.WB_text > a').string
            repost_dict2['user_id'] = str(__repost.select_one('div.WB_text > a')['href']).split('/')[-1]
            repost_dict2['text'] = __repost.select_one('span[node-type="text"]').get_text()
            
            if __repost.select('li[action-type="comment_media_img"] > img'):
                for __repost_pic in __repost.select('li[action-type="comment_media_img"] > img'):
                    repost_dict2['pic_url'].append('https:'+ __repost_pic['src'])
            
            reposts.append(repost_dict2)
            
    return reposts
        
get_reports()
            
            
        
        
    
            
            
            

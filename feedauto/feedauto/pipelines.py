# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import os
from os import path
from datetime import datetime as dt
import json
import scrapy
from feedauto.spiders.message_manager import MessageManager
import subprocess

class FeedautoPipeline(object):
    json_filepath=""
    def open_spider(self, spider):
        # スクレイピングを始めるときに呼び出される
        save_data_path = self.get_save_data_path()
        filename = self.get_filename()
        self.json_filepath = "%s/%s.json" % (save_data_path, filename)
        self.output_file(output_text="[\n", filepath=self.json_filepath, opentype='w')

    def close_spider(self, spider):
        # スクレイピングが完了したときに呼び出される
        f = open(self.json_filepath, 'r').read()
        f = f.rstrip(",\n")
        output_text = f+"]"
        self.output_file(output_text=output_text, filepath=self.json_filepath, opentype='w')
        try:
            data = json.loads(output_text)
        except Exception:
            text = "エラー:JSON変換"
            print(text)
        max_count = 20
        text = output_text
        dicts = json.loads(text)
        hacker_data = []
        github_data = []
        for v in dicts:
            if v["site"] == "github":
                github_data.append(v)
            else:
                hacker_data.append(v)
        hacker_data = sorted(hacker_data, key=lambda x:(x["score"], x["time"]), reverse=True)
        hacker_data_num = len(hacker_data)
        if hacker_data_num % 5 == 0:
            text = "今日の分を送るね！\n\n"
        elif hacker_data_num % 5 == 1:
            text = "よーし！今日のだよ！\n\n"
        elif hacker_data_num % 5 == 2:
            text = "みてみて！\n\n"
        elif hacker_data_num % 5 == 3:
            text = "どーかな！\n\n"
        else:
            text = "いいでしょ！\n\n"
        category_dicts = {
            "IT": [],
            "Medium": [],
            "Market": [],
           # "Student": [],
            "UI/UX": [],
            "Other": [],
        }
        for k,val in category_dicts.items():
            for v in hacker_data:
                if k == "Other":
                    if not v["category"]:
                        category_dicts[k].append(v)
                else:
                    if v["category"] == k:
                        category_dicts[k].append(v)
        for k,val in category_dicts.items():
            if len(val) == 0:
                continue
            max_point = 0
            for v in val:
                if max_point < v["score"]:
                    max_point = v["score"]
            text += "*[ %s ]* [top %d point]\n" % (k, max_point)
            for i,v in enumerate(val):
                url = str(v["url"])
                if not url:
                    continue
                if i >= max_count:
                    break
                t = int(v["time"])
                d = dt.fromtimestamp(t)
                d = d.strftime("%H:%M")
                title = self.__translation(v["title"])
                #text += "*(%s) %s*\n" % (str(v["score"]), str(d))
                text += "<%s|・%s>\n" % (url, title)
            text += "\n"
        text += "*[ GitHubトレンド ]*\n"
        for i,v in enumerate(github_data):
            if i >= 5:
                break
            title = self.__translation(v["title"])
            if not title:
                text += "%s\n" % v["url"]
            else:
                text += "<%s|・%s>\n" % (v["url"], title)
        print(text)
        MessageManager().send_to_slack(text)

    def __translation(self, text):
        t = ""
        try:
            args = ['/usr/local/bin/trans', '-brief', str(text)]
            t = subprocess.check_output(args)
            t = t.decode('utf-8')
        except:
            t = str(text)
        t = t.replace("\n", "")
        t = t.replace(" ", "")
        t = t.replace("　", "")
        return t

    def process_item(self, item, spider):
        # 非同期的にitemを取得したときに呼び出される
        json_text = json.dumps(dict(item), ensure_ascii=False, sort_keys=True, indent=4)
        json_text = json_text+",\n"
        self.output_file(output_text=json_text, filepath=self.json_filepath, opentype='a')
        return item

    def get_filename(self):
        # file名を返す
        today_str = dt.now().strftime('%Y-%m-%d')
        filename = '%s-%s' % ("feed", today_str)
        return filename

    def get_save_data_path(self):
        # 保存するディレクトリの作成とpathを返す
        save_data_path = ""
        day_dir_str = dt.now().strftime('%Y/%m/%d')
        APP_ROOT = path.dirname(path.abspath( __file__ ))
        save_data_path = APP_ROOT+"/data/"+day_dir_str
        if not os.path.exists(save_data_path):
            os.makedirs(save_data_path)
        return save_data_path

    def output_file(self, output_text="", filepath="", opentype=""):
        # ファイルに出力
        with open(filepath, opentype) as f:
            f.write(output_text)


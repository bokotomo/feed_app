# -*- coding: utf-8 -*-
import urllib.request
import json
import smtplib

class MessageManager:
    def send_to_slack(self, text):
        # スラックにメッセージを送る
        url = "" 
        method = "POST"
        param = {
            "payload": {
                'channel': 'feed-auto',
                'username': 'Serval',
                'text': text
            }
        }
        self.send_http_request(url=url, method=method, param=param)

    def get_today_news(self):
        # スラックにメッセージを送る
        url = "http://proport.me" 
        method = "POST"
        param = {
            "OK":"OK"
        }
        self.send_http_request(url=url, method=method, param=param)

    def asend_to_slack(self, text):
        # スラックにメッセージを送る
        url = "" 
        method = "POST"
        param = {
            "payload": {
                'channel': 'feed-auto',
                'username': 'Serval',
                'text': text
            }
        }
        self.send_http_request(url=url, method=method, param=param)

    def send_http_request(self, url="", method="", param={}):
        # httpリクエストを送る
        response_body = ""
        encoded_param = urllib.parse.urlencode(param).encode(encoding='utf-8')
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(param).encode("utf-8")
        try :
            with urllib.request.urlopen(url=url, data=encoded_param) as response:
                response_body = response.read().decode("utf-8")
        except ValueError :
            print("アクセスに失敗しました。")
        return response_body

if __name__ == "__main__":
    text = "<https://alert-system.com/alerts/1234|Click here> for details!"
    MessageManager().send_to_slack(text)
    #MessageManager().get_today_news()


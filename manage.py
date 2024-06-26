from flask import Flask, render_template, request
import requests
import json
import os
app = Flask(__name__)

os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

@app.route('/api')
def api():
    # return '''{"status":"yes"}'''
    pg = request.args.get('pg', '')
    wd = request.args.get('wd', '')
    # res = json.loads(requests.get("https://api.okzy.tv/api.php/provide/vod/at/json/?ac=detail&wd="+wd).text)
    res = json.loads(requests.get("https://49zyw.com/api.php/provide/vod/?ac=detail&wd="+wd).text)
    
    

    for i in res["list"]:
        i["m3u8"] = []
        i["mp4"] = []

        if i["vod_down_url"] != "":
            for j in i["vod_down_url"].split("#"):
                res_data = j.split("$")
                if res_data[1][-3:] == "mp4":
                    i["mp4"].append(res_data)
                
                #规则
                if len(res_data) > 2:
                    for k in res_data:
                        if k[-3:] == "mp4":
                            cu_str  = ["播放",k]
                            i["mp4"].append(cu_str) 
                else:
                    if res_data[1][-3:] == "mp4":
                        i["mp4"].append(res_data)

        if i["vod_play_url"] != "":
            for j in i["vod_play_url"].split("#"):
                res_data = j.split("$")
                #规则
                if len(res_data) > 2:
                    for k in res_data:
                        if k[-4:] == "m3u8":
                            cu_str  = ["播放",k]
                            i["m3u8"].append(cu_str) 
                else:
                    try:
                        if res_data[1][-4:] == "m3u8":
                            i["m3u8"].append(res_data)
                    except:
                        pass
    
    return res

@app.route('/')
def index():
    # 可以获取 链接
    return render_template('movie.html')
@app.route('/test')
def test():
    # 可以获取 链接
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

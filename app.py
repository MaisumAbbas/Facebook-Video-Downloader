from flask import Flask, render_template, request, redirect
from datetime import datetime
from tqdm import tqdm
import ctypes
import requests
import re
import os
import easygui
    
app = Flask(__name__)

@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('index.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        fbUrl = request.form['fbUrl']
        #value jari hai print ni hori
        if fbUrl != '':
            if request.form['quality'] == '':
                pass
            elif request.form['quality'] == 'HD':
                download_video("HD")
            elif request.form['quality'] == 'SD':
                download_video("SD")
            elif request.form['quality'] == 'MP3':
                download_audio("SD")
            return redirect("/", code=302)
        else:
            return redirect("/", code=302)

def download_video(quality):
    """Download the video in HD or SD quality"""
    print(f"\nDownloading the video in {quality} quality... \n")
    url = request.form['fbUrl']
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        ctypes.windll.user32.MessageBoxW(0, "Kindly Provide a Valid Facebook Video URL", "Error", 0)
        return redirect("/", code=302)

    _qualityhd = re.search('hd_src:"https', html)
    _qualitysd = re.search('sd_src:"https', html)
    _hd = re.search('hd_src:null', html)
    _sd = re.search('sd_src:null', html)

    list = []
    _thelist = [_qualityhd, _qualitysd, _hd, _sd]
    for id,val in enumerate(_thelist):
        if val != None:
            list.append(id)
    
    if main(list, quality) == True:
        return redirect("/", code=302)

    if re.search(rf'{quality.lower()}_src:"(.+?)"', html) is not None:
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
    else:
        ctypes.windll.user32.MessageBoxW(0, "The requested video is private.", "Error", 0)
        return redirect("/", code=302)

    file_size_request = requests.get(video_url, stream=True)
    file_size = int(file_size_request.headers['Content-Length'])
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
    with open(filename + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    ctypes.windll.user32.MessageBoxW(0, "Video Downloaded Successfully", "Success", 0)

def download_audio(quality):
    """Download the audio in MP3 quality"""
    print(f"\nDownloading the audio in MP3 quality... \n")
    url = request.form['fbUrl']
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

    if x:
        html = requests.get(url).content.decode('utf-8')
    else:
        ctypes.windll.user32.MessageBoxW(0, "Kindly Provide a Valid Facebook Video URL", "Error", 0)
        return redirect("/", code=302)

    _qualityhd = re.search('hd_src:"https', html)
    _qualitysd = re.search('sd_src:"https', html)
    _hd = re.search('hd_src:null', html)
    _sd = re.search('sd_src:null', html)

    list = []
    _thelist = [_qualityhd, _qualitysd, _hd, _sd]
    for id,val in enumerate(_thelist):
        if val != None:
            list.append(id)
    
    if re.search(rf'{quality.lower()}_src:"(.+?)"', html) is not None:
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
    else:
        ctypes.windll.user32.MessageBoxW(0, "The requested video is private.", "Error", 0)
        return redirect("/", code=302)

    video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    file_size = int(file_size_request.headers['Content-Length'])
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
    with open(filename + '.mp3', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    ctypes.windll.user32.MessageBoxW(0, "Audio Downloaded Successfully", "Success", 0)

#check HD and SD Availability Check - ERROR
def main(list, quality):
    try:
        if quality == 'HD' and 1 in list and 2 in list:
            ctypes.windll.user32.MessageBoxW(0, "Oops! The video is not available in HD quality. Kindly choose another format.", "Error", 0)
            return True
        return False       

    except(KeyboardInterrupt):
        print("\nProgramme Interrupted")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
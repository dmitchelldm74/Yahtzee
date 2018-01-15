import random, math, json, sys, os, datetime, http.client, mimetypes, shutil, urllib.request, urllib.parse, socket
from threading import Thread
import tkinter as tk
from tkinter import messagebox

def download_url(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def find_data_file(*args, datapath=False):
    if hasattr(sys, '_MEIPASS'):
        datadir = "C:\\Program Files\\Yahtzee"
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, *args)
    
def assets_initialize():
    if hasattr(sys, '_MEIPASS'):
        assets_path = lambda base="": os.path.join(sys._MEIPASS, "assets")
        images_path = lambda base: os.path.join(base, "images")
        data_path = lambda base: os.path.join(base, "data")
        info_path = lambda base: os.path.join(base, "info")
        core_path = lambda base: os.path.join(base, "core")
        dfpath = lambda base="": find_data_file(base)
        dfassets = dfpath("assets")
        #print(os.listdir(dfpath("assets")))
        if not os.path.exists(dfpath("assets")):
            shutil.move(assets_path(), dfpath())
        for p in (images_path, data_path, info_path, core_path):
            try:
                if not os.path.exists(p(dfassets)):
                    shutil.move(p(assets_path()), dfassets)
            except:
                print("Non-Existent: %s"%p(dfassets))
        #print(os.listdir(dfpath()))
        #print(os.listdir(dfpath("assets")))
        
def check_internet():
    try:
        if len(socket.gethostbyname('www.google.com')) != 0:
            return True
    except Exception as e:
        return False

def check_update():
    try:
        url = '/'.join([REPO_URL, 'assets', 'info', 'release.txt'])
        print(url)
        info = json.loads(download_url(url))
        print(info, versioninfo["Version"], info["Version"])
        return versioninfo["Version"] != info["Version"] 
    except Exception as e:
        print(e)
        print('Update Checker Error')
    return False
    
def run_temp_module(path):
    script = os.path.basename(path)
    globals()[script.rsplit('.')[0]] = eval(compile(open(path,"r").read(), script, 'exec'), globals())
    
def update_file_handler(*args):
    open(find_data_file(*args), "w").write(download_url("/".join((REPO_URL,)+args)))

assets_initialize()
versioninfo = json.load(open(find_data_file("assets","info","release.txt"),"r"))
print(versioninfo)
REPO_URL = "https://raw.github.com/dmitchelldm74/Yahtzee/master"
INTERNET = check_internet()
if INTERNET:
    UPDATE = check_update()
    if UPDATE:
        messagebox.showinfo("Update Available", "Click ok to install.")
        for f in [("assets", "core", "main.py"), ("assets", "info", "release.txt")]:
            thread = Thread(target=update_file_handler, args=f)
            thread.start()
run_temp_module(find_data_file("assets", "core", "main.py"))
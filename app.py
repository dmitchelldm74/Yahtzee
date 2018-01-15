import random, math, json, sys, os, datetime, http.client, mimetypes, shutil, urllib.request, urllib.parse, socket
import tkinter as tk

def download_url(url):
    return urllib.request.urlopen(url).read()

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
        info = KV(download_url(os.path.join(REPO_URL, 'assets', 'info', 'release.txt')))
        print(info)
        return versioninfo["version"] != info["version"] 
    except:
        print('Update Checker Error')
    return False
    
def run_temp_module(path):
    script = os.path.basename(path)
    globals()[script.rsplit('.')[0]] = eval(compile(open(path,"r").read(), script, 'exec'), globals())

assets_initialize()
run_temp_module(find_data_file("assets","info","releasekvreader.py"))
REPO_URL = "https://github.com/dmitchelldm74/Yahtzee/master"
INTERNET = check_internet()
if INTERNET:
    UPDATE = check_update()
    if UPDATE:
        tkinter.messagebox.showinfo("Installing Update", "Click ok to install.")
versioninfo = KV(open(find_data_file("assets","info","release.txt"),"r").read())

run_temp_module(find_data_file("assets", "core", "main.py"))
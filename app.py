import random, math, json, sys, os, time, datetime, http.client, mimetypes, shutil, urllib.request, urllib.parse, socket
from threading import Thread
import webbrowser as wb
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
        info = json.loads(download_url(url))
        if info['Stable'] == 'True':
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
    
def update_handler():
    changes = json.loads(download_url('/'.join([REPO_URL, 'changes.txt'])))
    d = len(changes)+1
    dismiss = alertbox(root, "Downloading Update...")
    lbl = tk.Label(dismiss, text="", width=1, bg="green", fg="white", relief="groove")
    lbl.grid(row=dismiss._rowm.get(),column=0,columnspan=6)
    for i,f in enumerate(changes+[("assets", "info", "release.txt")]):
        try:
            if isinstance(f, (list, tuple)):
                update_file_handler(*f)
            elif f == "exe":
                open(os.path.join(os.getcwd(), "Yahtzee.exe"), "wb").write(urllib.request.urlopen('/'.join([REPO_URL, 'dist', "Yahtzee.exe"])).read())
        except Exception as e:
            print(e)
        p = i/d
        lbl.config(text=str(int(p*100))+"% Done", width=int(p*50))
    lbl.config(text="100% Done", width=50)
assets_initialize()
versioninfo = json.load(open(find_data_file("assets","info","release.txt"),"r"))
REPO_URL = "https://raw.github.com/dmitchelldm74/Yahtzee/master"
INTERNET = check_internet()
run_temp_module(find_data_file("assets", "core", "main.py"))
if INTERNET:
    UPDATE = check_update()
    if UPDATE:
        yesnobox(root, "Update Available", "Install Update?", Thread(target=update_handler, args=()).start)
root.mainloop()
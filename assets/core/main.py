def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    if(selector.find('https') == 0):
        h = http.client.HTTPSConnection(host)
    else:
        h = http.client.HTTPConnection(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    return response.read()

def post(url, fields):
    fields = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=fields)
    try:
        resp = urllib.request.urlopen(req).read()
        return resp
    except urllib.error.HTTPError as e:
        print("401 Error", e)
        return "File Error!"

def encode_multipart_formdata(fields, files):
    BOUNDARY_STR = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = bytes("\r\n","ASCII")
    L = []
    for (key, value) in fields:
        L.append(bytes("--" + BOUNDARY_STR,"ASCII"))
        L.append(bytes('Content-Disposition: form-data; name="%s"' % key,"ASCII"))
        L.append(b'')
        L.append(bytes(value,"ASCII"))
    for (key, filename, value) in files:
        L.append(bytes('--' + BOUNDARY_STR,"ASCII"))
        L.append(bytes('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename),"ASCII"))
        L.append(bytes('Content-Type: %s' % get_content_type(filename),"ASCII"))
        L.append(b'')
        L.append(value)
    L.append(bytes('--' + BOUNDARY_STR + '--',"ASCII"))
    L.append(b'')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=' + BOUNDARY_STR
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

dice_faces = [[],[(25,25)],[(40,10),(10,40)],[(40,10),(25,25),(10,40)],[(10,10),(40,10),(10,40),(40,40)],[(10,10),(40,10),(25,25),(10,40),(40,40)],[(10,10),(40,10),(10,25),(40,25),(10,40),(40,40)]]
class YahtzeeGame(tk.Frame):
    def __init__(self, root):
        self.root = root
        tk.Frame.__init__(self, root)
        self.reset_roll()
        self.upper_total = 0
        self.lower_total = 0
        self.score = {"upper":{},"lower":{}}
        self.turns = 0
        self.create_elements()
        
    def create_elements(self):
        row = Row()
        self._cvs = tk.Canvas(self, width=75*5, height=75)
        self._cvs.grid(row=row.get(),column=1,columnspan=5)
        self._rclbl = tk.Label(self)
        self._rclbl.grid(row=row.get(),column=1,columnspan=5)
        lbl = tk.Label(self, text="Upper Section", width=27, relief="groove")
        lbl.grid(row=row.get(),column=1,columnspan=2)
        for x,n in enumerate(["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "3 of a kind", "4 of a kind", "Full house", "Sm straight", "Lg straight", "YAHTZEE", "Chance"], 1):
            r = row.get()
            l = self.create_lbl_row(n,r,x)
            if x == 6:
                lbl = tk.Label(self, text="Lower Section", width=27, relief="groove")
                lbl.grid(row=row.get(),column=1,columnspan=2)
            elif x == 12:
                self._ytlbl = l
        lpt = ['_utlbl', '_ltlbl', '_gtlbl']
        for i,n in enumerate(["Upper Total", "Lower Total", "Grand Total"]):
            r = row.get()
            l = self.create_lbl_row(n,r,i+x)
            setattr(self, lpt[i], l)

    def create_lbl_row(self, n, r, i):
        lbl = tk.Label(self, text=n, width=10, relief="groove")
        lbl2 = tk.Label(self, width=10, relief="groove")
        lbl.grid(row=r, column=1)
        lbl2.grid(row=r, column=2)
        fn = lambda evt,i=i,lbl=lbl,lbl2=lbl2: self.add_score(i,lbl,lbl2)
        lbl.bind('<Button-1>', fn)
        lbl2.bind('<Button-1>', fn)
        return lbl2
    
    def roll_dice(self):
        n = random.choice([random.randint(1,6) for x in range(0,random.randint(3,14))])
        # Old less-random dice roller
        #return int(random.choice((random.randint(1,6), math.sqrt(random.randint(1,36)))))
        return n

    def show_roll(self):
        if self.roll_count > 0:
            self._cvs.delete(tk.ALL)
            for f in range(0, 5):
                if self.dice_save[f] == None:
                    d = self.roll_dice()
                else:
                    d = self.dice_save[f]
                self.dice_cache[f] = d
            self.redraw_dice()
            self.roll_count -= 1
            self._rclbl.config(text="Rolls Left: %d"%self.roll_count)
        
    def select_dice(self,f,d):
        if self.dice_save[f] == None:
            self.dice_save[f] = d
        else:
            self.dice_save[f] = None
        self.redraw_dice()
        
    def draw_dice(self, f,d,fill,outline):
        x = (f*75)+15
        r = self._cvs.create_rectangle(x, 25, x+50, 75, fill=fill)
        fn = lambda evt,f=f,d=d: self.select_dice(f,d)
        for face in dice_faces[d]:
            o = self._cvs.create_oval(x+face[0]-2.5, 22.5+face[1], x+face[0]+2.5, 27.5+face[1], outline=outline, fill=outline, width=2)
            self._cvs.tag_bind(o, "<Button-1>", fn)
        self._cvs.tag_bind(r, "<Button-1>", fn)
            
    def redraw_dice(self):
        self._cvs.delete(tk.ALL)
        for f,d in enumerate(self.dice_save):
            if d != None:
                self.draw_dice(f,d,"red","white") 
            else:
                self.draw_dice(f,self.dice_cache[f],"white","black")
                
    def draw_score_lbls(self):
        gt = self.upper_total+self.lower_total
        if self.upper_total >= 63:
            self._utlbl.config(text="%d+35=%d"%(self.upper_total, self.upper_total+35))
            gt += 35
        else:
            self._utlbl.config(text=self.upper_total)
        self._ltlbl.config(text=self.lower_total)
        self._gtlbl.config(text=gt)
        return gt
        
    def check_done(self):
        if self.turns == 13:
            messagebox.showinfo("Game Over!", "Score: %d" % self.draw_score_lbls())
            self.reset()
                
    def add_score(self,i,lbl,lbl2):
        dice = [self.dice_cache[x] if n == None else n for x,n in enumerate(self.dice_save)]
        if None not in dice:
            if len(set(dice)) == 1:
                s = self.score["lower"].get(12,0)
                c = 100
                if not s:
                    c = 50
                self.lower_total += c
                self.score["lower"][12] = s+c
                self._ytlbl.config(text=s+c)
            elif i in range(1,7) and self.score["upper"].get(i) == None:
                s = (dice.count(i))*i
                self.score["upper"][i] = s
                self.upper_total += s
                lbl2.config(text=s)
            elif i > 6 and self.score["lower"].get(i) == None:
                s = 0
                if i == 7 and same(dice):
                    s = sum(dice)
                elif i == 8 and same(dice, 4):
                    s = sum(dice)
                elif i == 9 and same(dice) and same(dice, 2):
                    s = 25
                elif i == 10 and get_consec(dice) >= 4:
                    s = 30
                elif i == 11 and get_consec(dice) == 5:
                    s = 40
                elif i == 13:
                    s = sum(dice)
                elif i > 13:
                    return
                self.score["lower"][i] = s
                self.lower_total += s
                lbl2.config(text=s)
            else:
                return
            self.reset_roll()
            self._rclbl.config(text="Rolls Left: %d"%self.roll_count)
            self._cvs.delete(tk.ALL)
            self.turns += 1
            #self.check_done()
        self.draw_score_lbls()
        
    def reset_roll(self):
        self.dice_save = [None]*5
        self.dice_cache = [None]*5
        self.roll_count = 3
       
    def clear(self):
        self._cvs.delete(tk.ALL)
        
    def reset(self):
        show = self._show
        self.__init__(self.root)
        getattr(self, show[0])(*show[1], **show[2])
        
    def grid(self, *args, **kwargs):
        self._show = ("grid", args, kwargs)
        tk.Frame.grid(self, *args, **kwargs)
        
    def pack(self, *args, **kwargs):
        self._show = ("pack", args, kwargs)
        tk.Frame.pack(self, *args, **kwargs)
            
def get_consec(li):
    li = list(set(sorted(li)))
    for l in (li, li[1:], li[:-1]):
        #print(l, list(range(l[0], l[-1]+1)))
        if l == list(range(l[0], l[-1]+1)):
            return len(l)
    return 0

def same(dice, i=3):
    return [x for x in dice if dice.count(x) == i] != []

class Row():
    def __init__(self):
        self.n = -1
    def get(self):
        self.n += 1
        return self.n
    
def dismiss_msg(frame):
    p = frame.master
    frame.destroy()
    p.update()
    
def alertbox(parent, text):
    aframe = tk.Frame(parent, relief="ridge", borderwidth=2)
    aframe._rowm = Row()
    lbl = tk.Label(aframe, text=text, font="default 18 bold")
    lbl.grid(row=aframe._rowm.get(), column=0, columnspan=3)
    lbl2 = tk.Label(aframe, text="Dismiss", font="default 14 underline", fg="blue")
    lbl2.grid(row=aframe._rowm.n, column=5, padx=10)
    lbl2.bind('<Button-1>', lambda evt,aframe=aframe: dismiss_msg(aframe))
    aframe.grid(row=0,column=0,columnspan=100) #parent._rowm.get()
    return aframe
    
def signinbox(parent):
    box = alertbox(parent, "Sign-In To Droplet")
    tk.Label(box, text="Username: ").grid(row=box._rowm.get(),column=0)
    w = 25
    ety = tk.Entry(box, width=w)
    ety.grid(row=box._rowm.n, column=1, columnspan=3)
    tk.Label(box, text="Password: ").grid(row=box._rowm.get(),column=0)
    ety2 = tk.Entry(box, width=w, show="*")
    ety2.grid(row=box._rowm.n, column=1, columnspan=3)
    sbt = tk.Button(box, text="Sign-In", command=lambda box=box,ety=ety,ety2=ety2: sign_in(box,ety,ety2))
    sbt.grid(row=box._rowm.get(), column=3)
    
def sign_in(box, ety, ety2):
    global gamedata
    i, i2 = ety.get(), ety2.get()
    if i != "" and i2 != "":
        gamedata["uname"] = i
        gamedata["pass"] = i2 
        gamedata.save()
    box.destroy()
    
def view_high_scores():
    global gamedata
    gamedata.comps = ["y236"]
    win = tk.Toplevel()
    row = Row()
    win._rowm = row
    if gamedata.no_credentials:
        signinbox(win)
    tk.Label(win, text="High Scores For Friend: ").grid(row=row.get(),column=0)
    ety = tk.Entry(win)
    ety.grid(row=row.n, column=0)
    frame = tk.Frame(win)
    tk.Button(win, text="GO", command=lambda ety=ety,frame=frame: comp_add(ety.get(),frame)).grid(row=row.n, column=2)
    frame.grid(row=row.get(), column=0, columnspan=6)
    tk.Label(frame, text="Rank", relief="groove").grid(row=row.get(), column=0)
    tk.Label(frame, text="Name", relief="groove").grid(row=row.n, column=1)
    tk.Label(frame, text="Score", relief="groove").grid(row=row.n, column=2)
    tk.Label(frame, text="Date", relief="groove").grid(row=row.n, column=3)
    update_high_score_frame(frame)
    win.mainloop()
    
def comp_add(user, frame):
    global gamedata
    gamedata.comps.append(user)
    update_high_score_frame(frame)
    
def update_high_score_frame(frame):
    global gamedata
    try:
        chart = gamedata.pull()
        for c in gamedata.comps:
            chart += gamedata.pull(owner=c)
        chart.sort(key=lambda x: x[1], reverse=True)
        row = frame.master._rowm
        for r,c in enumerate(chart,1):
            tk.Label(frame, text=r).grid(row=row.get(),column=0)
            tk.Label(frame, text=c[0]).grid(row=row.n,column=1)
            tk.Label(frame, text=c[1]).grid(row=row.n,column=2)
            tk.Label(frame, text=c[2]).grid(row=row.n,column=3)
    except:
        frame.master.destroy()
        alertbox(root, "Error Checking Scores!")
        
class GDAT(dict):
    def __init__(self, filename):
        dict.__init__(self)
        self.filename = filename
        self.game = None
        
    def save(self):
        try:
            json.dump(self, open(self.filename,"w"))
            return 1
        except:
            return 0
        
    def load(self):
        try:
            self.update(json.load(open(self.filename,"r")))
            return 1
        except:
            return 0
        
    def logout(self):
        self.pop("uname")
        self.pop("pass")
        self.save()
        signinbox(root)
            
    def pull(self, owner=None, fname="HighScores.ytz"):
        if not self.no_credentials:
            #print(self.get("uname") if owner == None else owner, 'o', fname)
            resp = "[]"
            #resp = post('http://localhost/cli/uploads', [("username", self.get("uname")), ("password", self.get("pass")), ("filename", fname), ("owner", self.get("uname") if owner == None else owner)])
            try:
                return json.loads(resp)
            except:
                pass
        return []
        
    def push(self, fname="HighScores.ytz"):
        if not self.no_credentials:
            #data = json.dumps(self.pull()+[[self.get("uname"), self.game.draw_score_lbls(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]])
            alertbox(root, "Score Bragged!")
            post('http://104.236.235.19/easy_send893b3', [("username", self.get("uname")), ("password", self.get("pass")), ('text', '%s is a BRAGGER! \n Yahtzee score: %d'%(self.get("uname"), self.game.draw_score_lbls()))])
            #post_multipart('104.236.235.19/easy_send893b3', '/upload', [("username", self.get("uname")), ("password", self.get("pass")), ('alert', 'false')], [("file", fname, str(data).encode('utf-8'))])
           
    def hide_scores(self, fname="HighScores.ytz"):
        if not self.no_credentials:
            post_multipart('104.236.235.19', '/upload', [("username", self.get("uname")), ("password", self.get("pass")), ('alert', 'false')], [("file", fname, "[]".encode('utf-8'))])
           
    @property
    def no_credentials(self):
        self.load()
        return False if "uname" in self and "pass" in self else True

root = tk.Tk()
root.title("Yahtzee")
row = Row()
root._rowm = row
f = find_data_file("assets", "data")
if not os.path.exists(f):
    os.makedirs(f)
gamedata = GDAT(find_data_file("assets", "data", "gamedata.json", datapath=True))
# FUTURE: TO FAR, Droplet not stable
if not os.path.exists(gamedata.filename) or gamedata.no_credentials:
    signinbox(root)
    row.get()
lbl = tk.Label(root, text="YAHTZEE", font="Arial 50 italic bold", fg="red")
game = YahtzeeGame(root)
gamedata.game = game
btnbar = tk.Frame(root)
buttons = {"New Game": game.reset}
if INTERNET:
    buttons.update({"#High Scores":view_high_scores, "Brag Score":gamedata.push, "#Hide Scores":gamedata.hide_scores})
    if gamedata.no_credentials:
        buttons["Login"] = lambda: signinbox(root)
    else:
        buttons["Logout"] = gamedata.logout
for x,b in enumerate(buttons):
    if not b.startswith("#"):
        btn = tk.Button(btnbar, text=b, command=buttons[b])
        btn.grid(row=1,column=x)
        buttons[b] = btn
btnbar.grid(row=row.get(),column=1)
btn = tk.Button(root, text="Roll Dice", command=game.show_roll, width=25, height=2)
lbl.grid(row=row.get(), column=1, columnspan=3)
game.grid(row=row.get(),column=1, columnspan=3)
btn.grid(row=row.get(),column=1,columnspan=6)
#icon handler
icopath = find_data_file('assets', 'images', 'icon.png')
imgicon = tk.PhotoImage(file=icopath)
root.tk.call('wm', 'iconphoto', root._w, imgicon)
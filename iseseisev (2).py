from tkinter import *
import random
from tkinter import ttk
import winsound


#loov ekraani
root = Tk()
root.geometry("900x1000") #window mõõdud
root.title("dogerererei mäng") #extra clutter
root.resizable(False, False)
menu = Menu(root)
root.config(menu=menu)

#lõuendi mõõdud
l = 800
k = 900

tabamus_valmis = True #kontrollib kas tabamu valmis et heli ei spämmiks

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate") #deferminate tähendab et täitub kindla protsendi võrra
progress.pack(pady=10) #paneb ekraanile, pady on kaugus progressi ja teiste elemnt vahel

progress["maximum"] = 100 # maks väärtus progbaril
progress["value"] = 0 # algväärtus progbaril

lõuend = Canvas(root, width = l, height = k, bg = "black")
lõuend.pack() # tenie valik oleks grid manager

# ruut = lõuend.create_rectangle(x, y, x+50, y+50, fill = "blue") #ruudu omadused, pikkus laius värv
pilt = PhotoImage(file="dogerer(2).png")
objekt = lõuend.create_image(100, 100, image=pilt)

##### LIIKUVAD PALLID!! #######
vastased = [] #list kuhu salvestatakse võik vastased
vastane = lõuend.create_oval(300, 300, 350, 350, fill="red") #esimene vastane
vastased.append(vastane)

###LIIKUMINE###
update_kiirus = 10 #pall liigub 3 pikslit iga 10 ms järel
vastase_kiirus = 3

xspeeds = [vastase_kiirus]
yspeeds = [vastase_kiirus]

def moveBall():
    for i in range(len(vastased)): # palli liikumine ja asukoha kt
        lõuend.move(vastased[i], xspeeds[i], yspeeds[i])
        (leftPos, topPos, rightPos, bottomPos) = lõuend.coords(vastased[i])
        if leftPos <= 0 or rightPos >= l: #kontrllib kas pall on jõudnud vasaku või parema äärde
            xspeeds[i] = -xspeeds[i] #palli suuna muut
        if topPos <= 0 or bottomPos >= k:
            yspeeds[i] = -yspeeds[i]
    lõuend.after(update_kiirus, moveBall)
moveBall() #kutsub funktiooni iga 10 millisekundi järel, loopib
##############################

objekt1 = lõuend.create_oval(400, 400, 300, 300, fill = "green")

def reset_tabamus(): #funktioon mis muudab muudab tabamuse heli tagasi true-ks aja mõõdudes
    global tabamus_valmis
    tabamus_valmis = True

#teeeme objektide jlõuendi bbox-i
def doge_äär_puude():
    doge_äär = lõuend.bbox(objekt) #lõendile annab objekti koordinaadid
    doge_vasak = doge_äär[0]
    doge_parem = doge_äär[2]
    doge_ülemine = doge_äär[1]
    doge_alumine = doge_äär[3]
    if doge_vasak < 0: 
        lõuend.move(objekt, 10, 0) #kui vasak äär on väiksem kui 0, liigutab objekti 10 pikslit paremale
    elif doge_ülemine < 0:
        lõuend.move(objekt, 0, 10)
    elif doge_parem > l:
        lõuend.move(objekt, -10, 0)
    elif doge_alumine > k:
        lõuend.move(objekt, 0, -10)

# Tuvastab kokkupõrke objektide vahel
def puutetuvastus():

    global tabamus_valmis
    
    d = lõuend.bbox(objekt)
    o = lõuend.bbox(objekt1)

    if (
        d[2] > o[0] and
        d[0] < o[2] and
        d[3] > o[1] and
        d[1] < o[3]
    ):
        

        winsound.PlaySound("püüe.wav", winsound.SND_ASYNC)

        # progress
        progress["value"] += 25
        if progress["value"] >= 100:
            progress["value"] = 0

            uus_vastane = lõuend.create_oval(300, 300, 350, 350, fill="red")
            vastased.append(uus_vastane) # lisab uues vastase listi

            xspeeds.append(random.choice([-3, 3])) # lisab suvalise kiiruse 3 või -3 uuele vastasele
            yspeeds.append(random.choice([-3, 3]))

        # suvaline uus asukoht
        uus_x = random.randint(50, l-50)
        uus_y = random.randint(50, k-50)

        vana = lõuend.coords(objekt1)
        vana_x = (vana[0] + vana[2]) / 2
        vana_y = (vana[1] + vana[3]) / 2

        dx = uus_x - vana_x
        dy = uus_y - vana_y

        lõuend.move(objekt1, dx, dy)

    else:
        for vastane in vastased: # kontrollib kõiki vastaseid listis
            v = lõuend.bbox(vastane)

            if (
                d[2] > v[0] and
                d[0] < v[2] and
                d[3] > v[1] and
                d[1] < v[3]
            ):
                progress["value"] = 0
                # tabamus.wav saab 1 sekundi delay
                if tabamus_valmis: # kontrollib kas tabamus on valmis et see heli ei spämmiks

                    tabamus_valmis = False # muudab falseks, reset tabamus def muudab jälle trueks
                    winsound.PlaySound("tabamus.wav", winsound.SND_ASYNC)
                    root.after(1000, reset_tabamus)

def colchek(): # kontrollib iga natukese aja tagant kas objektide ääred puutuvad
    puutetuvastus()
    root.after(100, colchek)

root.after(100, colchek)

#liigutab koordinaatide põhjal objekti
def vasak(event):
    x = -10
    y = 0
    lõuend.move(objekt, x, y)
    doge_äär_puude()


def parem(event):
    x = 10
    y = 0
    lõuend.move(objekt, x, y)
    doge_äär_puude()


def üles(event):
    x = 0
    y = -10
    lõuend.move(objekt, x, y)
    doge_äär_puude()


def alla(event):
    x = 0
    y = 10
    lõuend.move(objekt, x, y)
    doge_äär_puude()

    

#seob klaviatuuri noole klahvid liikumisega
root.bind("<Left>", vasak)
root.bind("<Right>", parem)
root.bind("<Up>", üles)
root.bind("<Down>", alla)

root.mainloop()
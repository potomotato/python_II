from tkinter import *
import random
from tkinter import ttk
import winsound

#loov ekraani
root = Tk()
root.geometry("800x900")

#lõuendi mõõdud
l = 800
k = 900


# näitab kaugel koordinaat on ekraani piirist. lisab koordinaadid ekraani keskele

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

progress["maximum"] = 100
progress["value"] = 0

lõuend = Canvas(root, width = l, height = k, bg = "black")
lõuend.pack() # tenie valik oleks grid manager

# ruut = lõuend.create_rectangle(x, y, x+50, y+50, fill = "blue") #ruudu omadused, pikkus laius värv
pilt = PhotoImage(file="dogerer(2).png")
objekt = lõuend.create_image(100, 100, image=pilt)

##### liikuv pall ######
vastane = lõuend.create_oval(300, 300, 400, 400, fill="red")

xspeed = yspeed = 5 # kiirus 5 pikslit 20 ms järel
def moveBall(): # palli liikumine ja asukoha kt
    global xspeed, yspeed # teeb globaalseks, et saaks muuta funkt sees
    lõuend.move(vastane, xspeed, yspeed)
    (leftPos, topPos, rightPos, bottomPos) = lõuend.coords(vastane)
    if leftPos <= 0 or rightPos >= l: #kontrllib kas pall on jõudnud vasaku või parema äärde
        xspeed = -xspeed #palli suuna muut
    if topPos <= 0 or bottomPos >= k:
        yspeed = -yspeed
    lõuend.after(20, moveBall) #kutsub funktiooni iga 20 millisekundi järel
lõuend.after(20, moveBall) # alustab loopimist
##############################

objekt1 = lõuend.create_oval(400, 400, 300, 300, fill = "green")

#teeeme objektide jlõuendi bbox-i
def doge_äär_puude():
    doge_äär = lõuend.bbox(objekt) #annab objektile ääre
    doge_vasak = doge_äär[0]
    doge_parem = doge_äär[2]
    doge_ülemine = doge_äär[1]
    doge_alumine = doge_äär[3]
    if doge_vasak < 0:
        lõuend.move(objekt, 10, 0)
    elif doge_ülemine < 0:
        lõuend.move(objekt, 0, 10)
    elif doge_parem > l:
        lõuend.move(objekt, -10, 0)
    elif doge_alumine > k:
        lõuend.move(objekt, 0, -10)

# Tuvastab kokkupõrke objektide vahel
def puutetuvastus():
    d = lõuend.bbox(objekt)
    o = lõuend.bbox(objekt1)

    if (
        d[2] > o[0] and
        d[0] < o[2] and
        d[3] > o[1] and
        d[1] < o[3]
    ):
        

        winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

        # progress
        progress["value"] += 10
        if progress["value"] >= 100:
            progress["value"] = 0

        # suvaline uus asukoht
        uus_x = random.randint(50, l-50)
        uus_y = random.randint(50, k-50)

        vana = lõuend.coords(objekt1)
        vana_x = (vana[0] + vana[2]) / 2
        vana_y = (vana[1] + vana[3]) / 2

        dx = uus_x - vana_x
        dy = uus_y - vana_y

        lõuend.move(objekt1, dx, dy)



#liigutab koordinaatide põhjal objekti
def vasak(event):
    x = -10
    y = 0
    lõuend.move(objekt, x, y)
    doge_äär_puude() # tuvastab, kas objekti bbox puutub lõuendi äärega
    puutetuvastus()

def parem(event):
    x = 10
    y = 0
    lõuend.move(objekt, x, y)
    doge_äär_puude()
    puutetuvastus()

def üles(event):
    x = 0
    y = -10
    lõuend.move(objekt, x, y)
    doge_äär_puude()
    puutetuvastus()

def alla(event):
    x = 0
    y = 10
    lõuend.move(objekt, x, y)
    doge_äär_puude()
    puutetuvastus()

#seob klaviatuuri noole klahvid liikumisega
root.bind("<Left>", vasak)
root.bind("<Right>", parem)
root.bind("<Up>", üles)
root.bind("<Down>", alla)

root.mainloop()
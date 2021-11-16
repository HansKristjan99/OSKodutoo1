#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# Näiteprogramm protsessoriaja planeerijate visualiseerimiseks
# algne autor Sten-Oliver Salumaa
# refaktoreerinud ja muidu muutnud Meelis Roos
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import copy
import random


def mäluJärjend():
    rida = []
    tulemus = []
    for i in range(50):
        rida.append("-")
    for i in range(10):
        tulemus.append(rida)
    return tulemus


def puhasta():
    tahvel.delete('all')


# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
# 1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1

def joonista(jarjend, protsessid):
    puhasta()
    tahvel.create_text(20, 20, text="Etapp   ", font=("arial", 7, "bold"))
    tahvel.create_text(60, 20, text="Lisatud", font=("arial", 7, "bold"))
    tahvel.create_text(60, 30, text="Protsess", font=("arial", 7, "bold"))
    varvid = {"-": "white", "B": "red", 'C': "green", 'D': "royal blue", 'E': "cyan", 'F': "yellow", 'G': "magenta",
              'H': 'orange', 'I': 'salmon', 'J': 'purple', "A": 'wheat1', 'flag': "white"}
    for j in range(len(jarjend)):
        eelmise_loppx = 80
        try:
            tahvel.create_text(55, 40 + j * 15 + 13 / 2.0,
                               text=protsessid[j][2] + ": " + str(protsessid[j][0]) + "," + str(protsessid[j][1]))
            tahvel.create_text(20, 40 + j * 15 + 13 / 2.0, text=j)

        except:
            pass
        if jarjend[j][0] == "flag":
            tahvel.create_text(120 + 0.45 * 16, 40 + j * 15 + 13 / 2.0, text="Ei mahu mällu")
            break
        for i in range(len(jarjend[j])):
            tahvel.create_rectangle(eelmise_loppx, 40 + j * 15, eelmise_loppx + 0.9 * 16, 40 + j * 15 + 13,
                                    fill=varvid[jarjend[j][i]])
            tahvel.create_text(eelmise_loppx + 0.45 * 16, 40 + j * 15 + 13 / 2.0, text=jarjend[j][i])
            eelmise_loppx += 0.9 * 16


# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = int(hakkliha[0])
        kestus = int(hakkliha[1])
        valjund.append([saabumine, kestus])
    return valjund


# otsustab, millist järjendit teha kahetasemeliseks massiiviks
def massiiviMeister():
    jarjend = []
    if var.get() == 1:
        return massiiviks(predef1)
    elif var.get() == 2:
        return massiiviks(predef2)
    elif var.get() == 3:
        return massiiviks(predef3)
    elif var.get() == 4:
        try:
            return massiiviks(kasutaja_jarjend.get())
        except:
            messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja muster!")
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)


# näitealgoritmi realisatsioon
# saab ette listi kaheelemendilistest lidtidest
# tagasitab paari väljundlistist ja keskmisest ooteajast
# ise midagi ei joonista
def LIFO(jarjend):
    return (mäluJärjend(), 0)


def jarjendileTahed(jarjend):
    tahed = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i in range(len(jarjend)):
        jarjend[i] = [jarjend[i][0], jarjend[i][1], tahed[i]]
    return jarjend


'''def firstFit(jarjend):
    valjund = mäluJärjend()
    eelminerida = valjund[0]
    for i in range(len(jarjend)):
        # Kustutame lõppenud protsessid
        valjund[i] = copy.deepcopy(eemaldaVanad(jarjend, eelminerida, i))
        taht = jarjend[i][2]
        pikkus = jarjend[i][0]
        valjund[i], kasmahtus = firstFitAbi(taht, pikkus, valjund[i])
        eelminerida = copy.deepcopy(valjund[i])
        if not kasmahtus:
            for j in range(i, len(valjund)):
                valjund[j][0] = "flag"
    return valjund
'''


def eemaldaVanad(protsessiJärjend, valjundirida, ajahetk):
    for i in range(len(protsessiJärjend)):
        if protsessiJärjend[i][1] + i == ajahetk:
            for j in range(len(valjundirida)):
                if valjundirida[j] == protsessiJärjend[i][2]:
                    valjundirida[j] = "-"
    return valjundirida


def firstFit(taht, pikkus, väljundirida):
    mahub = False
    for i in range(len(väljundirida) + 1 - pikkus):
        mahub = False
        if väljundirida[i] == "-":
            mahub = True
            for j in range(pikkus):
                if väljundirida[i + j] != "-":
                    mahub = False
        if mahub:
            for h in range(i, i + pikkus):
                väljundirida[h] = taht
            break
    return väljundirida, mahub


def randomFit(taht, pikkus, väljundirida):
    i = 0
    mahub = False
    algus = 0
    voimalikud_kohad = []
    while i < len(väljundirida) - pikkus + 1:
        # Vaatame, kas tükk mahuks siia
        if väljundirida[i] == "-":
            algus = i
            mahub = True
            # Uurime, kas tükk mahuks vahemikku [algus,algus+pikkus]
            for j in range(pikkus):
                if väljundirida[algus + j] != "-":
                    mahub = False
                    break
            if mahub:
                voimalikud_kohad.append((algus, algus + pikkus))
                mahub = False
            # Suurendame i-d, kuni jõuame uue tühja kohani
            while i < len(väljundirida) and (väljundirida[i] == "-"):
                i += 1
        else:
            i += 1

    if len(voimalikud_kohad) > 0:
        algus, lopp = random.choice(voimalikud_kohad)
        for i in range(algus, lopp):
            väljundirida[i] = taht
        return väljundirida, True
    else:
        return väljundirida, False


def lastFit(taht, pikkus, väljundirida):
    i = 0
    mahub = False
    algus = 0
    voimalikud_kohad = []
    while i<len(väljundirida)-pikkus +1:
        #Vaatame, kas tükk mahuks siia
        if väljundirida[i]=="-":
            algus = i
            mahub = True
            #Uurime, kas tükk mahuks vahemikku [algus,algus+pikkus]
            for j in range(pikkus):
                if väljundirida[algus + j] != "-":
                    mahub = False
                    break
            if mahub:
                voimalikud_kohad.append((algus, algus+pikkus))
                mahub = False
            # Suurendame i-d, kuni jõuame uue tühja kohani
            while i < len(väljundirida) and (väljundirida[i] == "-"):
                i += 1
        else:
            i+=1

    if len(voimalikud_kohad)>0:
        algus, lopp = voimalikud_kohad[-1]
        for i in range(algus, lopp):
            väljundirida[i]= taht
        return väljundirida, True
    else:
        return väljundirida, False

def bestFit(taht, pikkus, väljundirida):
    i = 0
    mahub = False
    algus = 0
    voimalikud_kohad = []
    while i < len(väljundirida) - pikkus + 1:
        # Vaatame, kas tükk mahuks siia
        if väljundirida[i] == "-":
            algus = i
            mahub = True
            # Uurime, kas tükk mahuks vahemikku [algus,algus+pikkus]
            for j in range(pikkus):
                if väljundirida[algus + j] != "-":
                    mahub = False
                    break
            # Suurendame i-d, kuni jõuame uue tühja kohani
            while i < len(väljundirida) and (väljundirida[i] == "-"):
                i += 1
            if mahub:
                voimalikud_kohad.append((algus, i))
        else:
            i += 1

    if len(voimalikud_kohad) > 0:
        lyhim =99999
        for i in voimalikud_kohad:
            print(i, "suurus:" + str(i[1] - i[0]))
            if (i[1]-i[0])<lyhim:
                lyhim = i[1]-i[0]
                algus, lopp = i[0],i[1]
        for i in range(algus, algus+pikkus):
            väljundirida[i] = taht
        return väljundirida, True
    else:
        return väljundirida, False


def worstFit(taht, pikkus, väljundirida):
    i = 0
    mahub = False
    algus = 0
    voimalikud_kohad = []
    while i < len(väljundirida) - pikkus + 1:
        # Vaatame, kas tükk mahuks siia
        if väljundirida[i] == "-":
            algus = i
            mahub = True
            # Uurime, kas tükk mahuks vahemikku [algus,algus+pikkus]
            for j in range(pikkus):
                if väljundirida[algus + j] != "-":
                    mahub = False
                    break
            # Suurendame i-d, kuni jõuame uue tühja kohani
            while i < len(väljundirida) and (väljundirida[i] == "-"):
                i += 1
            if mahub:
                voimalikud_kohad.append((algus, i))
        else:
            i += 1

    if len(voimalikud_kohad) > 0:
        pikim = -1
        for i in voimalikud_kohad:
            print(i, "suurus:" + str(i[1] - i[0]))
            if (i[1] - i[0]) > pikim:
                pikim = i[1] - i[0]
                algus, lopp = i[0], i[1]
        for i in range(algus, algus + pikkus):
            väljundirida[i] = taht
        return väljundirida, True
    else:
        return väljundirida, False


def kasuvalija(jarjend, algoritm):
    valjund = mäluJärjend()
    eelminerida = valjund[0]
    for i in range(len(jarjend)):
        # Kustutame lõppenud protsessid
        valjund[i] = copy.deepcopy(eemaldaVanad(jarjend, eelminerida, i))
        taht = jarjend[i][2]
        pikkus = jarjend[i][0]
        if algoritm == "random-fit":
            valjund[i], kasmahtus = randomFit(taht, pikkus, valjund[i])
        elif algoritm == "first-fit":
            valjund[i], kasmahtus = firstFit(taht, pikkus, valjund[i])
        elif algoritm == "last-fit":
            valjund[i], kasmahtus = lastFit(taht, pikkus, valjund[i])
        elif algoritm == "best-fit":
            valjund[i], kasmahtus = bestFit(taht, pikkus, valjund[i])
        elif algoritm == "worst-fit":
            valjund[i], kasmahtus = worstFit(taht, pikkus, valjund[i])
        eelminerida = copy.deepcopy(valjund[i])
        if not kasmahtus:
            for j in range(i, len(valjund)):
                valjund[j][0] = "flag"
    return valjund


def jooksuta_algoritmi(algoritm):
    jarjend = jarjendileTahed(massiiviMeister())
    valjund = kasuvalija(jarjend, algoritm)
    joonista(valjund, jarjend)


predef1 = "0,5;6,9;6,5;15,10"
predef2 = "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1"
predef3 = "5,6;6,9;11,3;12,7"

# GUI
raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("800x440")

var = IntVar()
var.set(1)
Radiobutton(raam, text="Esimene", variable=var, value=1).place(x=10, y=40)
Radiobutton(raam, text="Teine", variable=var, value=2).place(x=10, y=70)
Radiobutton(raam, text="Kolmas", variable=var, value=3).place(x=10, y=100)
Radiobutton(raam, text="Enda oma", variable=var, value=4).place(x=10, y=130)

silt_vali = ttk.Label(raam, text="Vali või sisesta järjend (kujul 1,10;4,2;12,3;13,2)")
silt_vali.place(x=10, y=10)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=120, y=40)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=120, y=70)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=120, y=100)

silt_run = ttk.Label(raam, text="Algoritmi käivitamiseks klõpsa nupule")
silt_run.place(x=10, y=160)

silt_tahvel = ttk.Label(raam, text="Käsil olevad protsessid:")
silt_tahvel.place(x=450, y=10)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.place(x=120, y=130, height=25, width=240)

tahvel = Canvas(raam, width=800, height=220, background="white")
tahvel.place(x=0, y=220)

randomfit_nupp = ttk.Button(raam, text="random-fit", command=lambda: jooksuta_algoritmi("random-fit"))
randomfit_nupp.place(x=10, y=190, height=25, width=80)

firstfit_nupp = ttk.Button(raam, text="first-fit", command=lambda: jooksuta_algoritmi("first-fit"))
firstfit_nupp.place(x=100, y=190, height=25, width=80)

lastfit_nupp = ttk.Button(raam, text="last-fit", command=lambda: jooksuta_algoritmi("last-fit"))
lastfit_nupp.place(x=190, y=190, height=25, width=80)

bestfit_nupp = ttk.Button(raam, text="best-fit", command=lambda: jooksuta_algoritmi("best-fit"))
bestfit_nupp.place(x=280, y=190, height=25, width=80)

worstfit_nupp = ttk.Button(raam, text="worst-fit", command=lambda: jooksuta_algoritmi("worst-fit"))
worstfit_nupp.place(x=370, y=190, height=25, width=80)

puhasta_nupp = ttk.Button(raam, text="Puhasta väljund", command=lambda: puhasta())
puhasta_nupp.place(x=500, y=190, height=25, width=130)

text = Text(raam, width=25, height=9)
text.place(x=450, y=30)

raam.mainloop()

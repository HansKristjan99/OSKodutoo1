#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# Näiteprogramm protsessoriaja planeerijate visualiseerimiseks
# algne autor Sten-Oliver Salumaa
# refaktoreerinud ja muidu muutnud Meelis Roos
import copy
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from collections import deque


def puhasta():
    tahvel.delete('all')


# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def joonista(jarjend):
    puhasta()
    eelmise_loppx = 20
    kaugus = 0
    for i in range(len(jarjend)):
        protsess = jarjend[i][0]
        kestus = jarjend[i][1]
        kujund = tahvel.create_rectangle(eelmise_loppx, 60, eelmise_loppx + kestus * 16, 100, fill="green")
        keskpaik = eelmise_loppx + kestus * 8
        protsessi_id = tahvel.create_text(keskpaik, 80, text=protsess)
        m = tahvel.create_text(eelmise_loppx, 110, text=str(kaugus))
        kaugus += kestus
        eelmise_loppx += kestus * 16
    m = tahvel.create_text(eelmise_loppx, 110, text=str(kaugus))


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
    valjund = []
    counter = 1
    jarg = 0
    kogu_ooteaeg = 0
    # paneb protsesse vajalikku järjekorda
    for p in sorted(jarjend, reverse=True):
        saabumine = p[0]
        kestus = p[1]
        if saabumine > (jarg):
            # kui kahe protsessi vahel on "auk", siis jäetakse sinna delay näitamiseks õige pikkusega tühik
            valjund.append([" ", saabumine - jarg])
            valjund.append(["P" + str(counter), kestus])
            jarg = saabumine + kestus
            counter += 1
        else:
            # vaatab, kui kaua konkreetne protsess oma järge ootas
            if saabumine < jarg:
                kogu_ooteaeg += jarg - saabumine
            # väljundlisti kirjutatakse protsess koos nime ja kestusega
            valjund.append(["P" + str(counter), kestus])
            jarg += kestus
            counter += 1
    # arvutan keskmise ooteaja
    keskm_ooteaeg = round(kogu_ooteaeg / len(jarjend), 2)
    return (valjund, keskm_ooteaeg)
#first come first serve algoritmi interpretatsioon
#võtab sisendiks protsesside listi kaheelemendilistest listidest
#tagasitab paari väljundlistist ja keskmisest ooteajast
def FCFS(jarjend):
    valjund = []
    counter = 1
    jarg = 0
    kogu_ooteaeg = 0
    jarjend.sort()
    # paneb protsesse vajalikku järjekorda
    for p in jarjend:
        saabumine = p[0]
        kestus = p[1]
        if saabumine > (jarg):
            # kui kahe protsessi vahel on "auk", siis jäetakse sinna delay näitamiseks õige pikkusega tühik
            valjund.append([" ", saabumine - jarg])
            valjund.append(["P" + str(counter), kestus])
            jarg = saabumine + kestus
            counter += 1
        else:
            # vaatab, kui kaua konkreetne protsess oma järge ootas
            if saabumine < jarg:
                kogu_ooteaeg += jarg - saabumine
            # väljundlisti kirjutatakse protsess koos nime ja kestusega
            valjund.append(["P" + str(counter), kestus])
            jarg += kestus
            counter += 1
    # arvutan keskmise ooteaja
    keskm_ooteaeg = round(kogu_ooteaeg / len(jarjend), 2)
    return (valjund, keskm_ooteaeg)

#Väljutatõrjuv SJF - eelistab väiksema protsessoriajaga protsesse suurematele
#võtab sisendiks protsesside listi kaheelemendilistest listidest
#tagasitab paari väljundlistist ja keskmisest ooteajastt
def SRTF(jarjend):
    jarjend_orig = copy.deepcopy(jarjend)
    valjund = []
    n = len(jarjend)
    valmis = 0
    t = 0
    suurTaisArv = 99999999
    lyhimaindeks = 0
    check = False
    counter = 1
    kogu_ooteaeg = 0
    for i in (jarjend):
        i.append("P" + str(counter))
        counter += 1
    while valmis != n:
        for j in range(n):
            if (jarjend[j][0] <= t) and (jarjend[j][1] < suurTaisArv) and jarjend[j][1] > 0:
                suurTaisArv = jarjend[j][1]
                lyhimaindeks = j
                check = True
        if not check:
            t += 1
            if len(valjund) == 0:
                valjund.append([" ", 1])
                continue
            if valjund[-1][0] == " ":
                valjund[-1][1] += 1
            else:
                valjund.append([" ", 1])
            continue
        if check:
            t += 1
            jarjend[lyhimaindeks][1] -= 1
            if jarjend[lyhimaindeks][1] == 0:
                valmis += 1
                kogu_ooteaeg += t - jarjend_orig[lyhimaindeks][0] - jarjend_orig[lyhimaindeks][1]
                suurTaisArv = 99999999
            if len(valjund) == 0:
                valjund.append([jarjend[lyhimaindeks][2], 1])
                continue
            if valjund[-1][0] == jarjend[lyhimaindeks][2]:
                valjund[-1][1] += 1
            else:
                valjund.append([jarjend[lyhimaindeks][2], 1])
        check = False
    keskmine_ooteaeg = kogu_ooteaeg / len(jarjend_orig)
    return valjund, keskmine_ooteaeg

#round robin ajakvandiga 3
#võtab sisendiks protsesside listi kaheelemendilistest listidest
#tagasitab paari väljundlistist ja keskmisest ooteajast
def RR3(jarjend):
    t = 0
    q = deque()
    valjund = []
    eemaldatavad = []
    valmis = False
    kogu_ooteaeg = 0
    for i in range(len(jarjend)):
        jarjend[i].append("P" + str(i + 1))
    jarjend_orig = copy.deepcopy(jarjend)
    while not valmis:
        for i in range(len(jarjend)):
            if jarjend[i][0] <= t:
                eemaldatavad.append(jarjend[i])
        for i in eemaldatavad:
            jarjend.remove(i)
        eemaldatavad.reverse()
        q.extendleft(eemaldatavad)
        eemaldatavad.clear()
        if len(q) == 0:
            t += 1
            if len(valjund) == 0:
                valjund.append([" ", 1])
                continue
            if valjund[-1][0] == " ":
                valjund[-1][1] += 1
            else:
                valjund.append([" ", 1])
            continue
        else:
            protsess = q.popleft()
            if protsess[1] > 3:
                t += 3
                protsess[1] -= 3
                if len(valjund) == 0:
                    valjund.append([protsess[2], 3])
                    q.append(protsess)
                    continue
                if valjund[-1][0] == protsess[2]:
                    valjund[-1][1] += 3
                else:
                    valjund.append([protsess[2], 3])
                q.append(protsess)
            elif protsess[1] <= 3:
                t += protsess[1]
                for vanaProtsess in jarjend_orig:
                    if protsess[2] == vanaProtsess[2]:
                        kogu_ooteaeg += t - vanaProtsess[0] - vanaProtsess[1]
                if len(valjund) == 0:
                    valjund.append([protsess[2], protsess[1]])
                    continue
                if valjund[-1][0] == protsess[2]:
                    valjund[-1][1] += protsess[1]
                else:
                    valjund.append([protsess[2], protsess[1]])
        if len(jarjend) == 0 and len(q) == 0:
            valmis = True
    keskmine_ooteaeg = kogu_ooteaeg / len(jarjend_orig)
    return valjund, keskmine_ooteaeg
#Kahe prioriteediga FCFS - kaks eraldi järjekorda qHigh ja qLow - tegutsevad vastavalt väikeste ja suurte protsessoriaegadega
#võtab sisendiks protsesside listi kaheelemendilistest listidest
#tagasitab paari väljundlistist ja keskmisest ooteajast
def FCFS2L(jarjend):
    t = 0
    qHigh = deque()
    qLow = deque()
    valjund = []
    eemaldatavad = []
    valmis = False
    kogu_ooteaeg = 0
    for i in range(len(jarjend)):
        jarjend[i].append("P" + str(i + 1))
    jarjend_orig = copy.deepcopy(jarjend)
    while not valmis:
        #lisame vastavalt pikkustele käimasolevad protsessid qhigh või qlow järjekorda
        for i in range(len(jarjend)):
            if jarjend[i][0] <= t:
                if jarjend[i][1] > 3:
                    qLow.append(jarjend[i])
                else:
                    qHigh.append(jarjend[i])
                eemaldatavad.append(jarjend[i])
        #eemaldame käimasolevad protsessid järjekorrast.
        for i in eemaldatavad:
            jarjend.remove(i)
        eemaldatavad.clear()
        #kui mõlemad on tühjad, ootame ühe sekundi
        if len(qHigh) == 0 and len(qLow) == 0:
            t += 1
            if len(valjund) == 0:
                valjund.append([" ", 1])
                continue
            if valjund[-1][0] == " ":
                valjund[-1][1] += 1
            else:
                valjund.append([" ", 1])
            continue
        #tegutseme enne kõrge prioriteediga järjekorraga
        #lähme tsükli päisesse tagasi, kui seal leidus protsess
        #lisame väljundisse ühe ajaühiku vastavat protsessi
        elif len(qHigh) > 0:
            t += 1
            qHigh[0][1] -= 1
            if len(valjund) == 0:
                valjund.append([qHigh[0][2], 1])
                if qHigh[0][1] == 0:
                    for vanaProtsess in jarjend_orig:
                        if qHigh[0][2] == vanaProtsess[2]:
                            kogu_ooteaeg += t - vanaProtsess[0] - vanaProtsess[1]
                    qHigh.popleft()
                continue
            if valjund[-1][0] == qHigh[0][2]:
                valjund[-1][1] += 1
            else:
                valjund.append([qHigh[0][2], 1])
            if qHigh[0][1] == 0:
                for vanaProtsess in jarjend_orig:
                    if qHigh[0][2] == vanaProtsess[2]:
                        kogu_ooteaeg += t - vanaProtsess[0] - vanaProtsess[1]
                qHigh.popleft()
            continue
        #Kui siia jõuame, siis pole kõrge prioriteediga protsesse
        #lisame väljundisse ühe ajaühiku järjekorra esimest protsessi
        elif len(qLow) > 0:
            if qLow[0][1]<0:
                break
            t += 1
            qLow[0][1] -= 1
            if len(valjund) == 0:
                valjund.append([qLow[0][2], 1])
                if qLow[0][1] == 0:
                    for vanaProtsess in jarjend_orig:
                        if qLow[0][2] == vanaProtsess[2]:
                            kogu_ooteaeg += t - vanaProtsess[0] - vanaProtsess[1]
                    qLow.popleft()
                continue
            if valjund[-1][0] == qLow[0][2]:
                valjund[-1][1] += 1
            else:
                valjund.append([qLow[0][2], 1])
            if qLow[0][1] == 0:
                for vanaProtsess in jarjend_orig:
                    if qLow[0][2] == vanaProtsess[2]:
                        kogu_ooteaeg += t - vanaProtsess[0] - vanaProtsess[1]
                qLow.popleft()
        if len(jarjend) == 0 and len(qLow) == 0 and len(qHigh) == 0:
            valmis = True
    keskmine_ooteaeg = kogu_ooteaeg / len(jarjend_orig)
    return valjund, keskmine_ooteaeg


def massiiviTeavitaja(massiiv):
    text.delete(1.0, END)
    for jupp in massiiv:
        text.insert(INSERT, str(jupp) + "\n")


def kasuvalija(jarjend, algoritm):
    if algoritm == "LIFO":
        return LIFO(jarjend)
    elif algoritm == "FCFS":
        return FCFS(jarjend)
    elif algoritm == "SRTF":
        return SRTF(jarjend)
    elif algoritm == "RR3":
        return RR3(jarjend)
    elif algoritm == "FCFS2L":
        return FCFS2L(jarjend)


def jooksuta_algoritmi(algoritm):
    jarjend = massiiviMeister()
    massiiviTeavitaja(jarjend)
    (valjund, ooteaeg) = kasuvalija(jarjend, algoritm)
    joonista(valjund)
    keskm_oot = tahvel.create_text(80, 40, text="Keskmine ooteaeg:  " + str(ooteaeg))


predef1 = "0,5;6,9;6,5;15,10"
predef2 = "0,2;0,4;12,4;15,5;21,10"
predef3 = "5,6;6,9;11,3;12,7"

# GUI
raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("800x400")

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

tahvel = Canvas(raam, width=800, height=180, background="white")
tahvel.place(x=0, y=220)

LIFO_nupp = ttk.Button(raam, text="LIFO", command=lambda: jooksuta_algoritmi("LIFO"))
LIFO_nupp.place(x=10, y=190, height=25, width=80)

FCFS_nupp = ttk.Button(raam, text="FCFS", command=lambda: jooksuta_algoritmi("FCFS"))
FCFS_nupp.place(x=100, y=190, height=25, width=80)

SRTF_nupp = ttk.Button(raam, text="SRTF", command=lambda: jooksuta_algoritmi("SRTF"))
SRTF_nupp.place(x=190, y=190, height=25, width=80)

RR3_nupp = ttk.Button(raam, text="RR3", command=lambda: jooksuta_algoritmi("RR3"))
RR3_nupp.place(x=280, y=190, height=25, width=80)

FCFS2L_nupp = ttk.Button(raam, text="2x FCFS", command=lambda: jooksuta_algoritmi("FCFS2L"))
FCFS2L_nupp.place(x=370, y=190, height=25, width=80)

puhasta_nupp = ttk.Button(raam, text="Puhasta väljund", command=lambda: puhasta())
puhasta_nupp.place(x=500, y=190, height=25, width=130)

text = Text(raam, width=25, height=9)
text.place(x=450, y=30)

raam.mainloop()

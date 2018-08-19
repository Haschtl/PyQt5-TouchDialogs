# -*- encoding: utf-8 -*-

import math
from random import randint
import traceback
import json
import subprocess
import threading
import sys
import time
import datetime

def temp2str(temp):
    return str(temp)+' °C'


def TwoTemp2str(temp_actual, temp_target):
    if temp_target == 0:
        return str(temp_actual)+' °C'
    else:
        return str(temp_actual)+'/'+str(temp_target)+' °C'


def calcHoleCorrection(t, R):
    r2 = (t+math.sqrt(t*t+4*R*R))/2
    return r2


def calcAllHoleCorrections(t):
    liste = []
    for R in range(2, 164, 2):
        r2 = calcHoleCorrection(t, R/10)
        liste = liste+[[R/10, r2]]

    return liste


def tryExc(fun, exc=None):
    try:
        a = fun
        return a, None
    except:
        tb = traceback.format_exc()
        print(tb)
        a = exc
        return a, tb


def random_color(self):
    i = randint(0, 6)
    if i == 0:
        return 'green'
    elif i == 1:
        return 'white'
    elif i == 2:
        return 'yellow'
    elif i == 3:
        return 'purple'
    elif i == 4:
        return 'grey'
    elif i == 5:
        return 'orange'
    elif i == 6:
        return 'violet'


def load_config(path="data/config.json"):
    with open(path, encoding="UTF-8") as jsonfile:
        config = json.load(jsonfile, encoding="UTF-8")
    return config


def save_config(config, path="data/config.json"):
    with open(path, 'w', encoding="utf-8") as fp:
        json.dump(config, fp)


def cmd(command):
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    stdout_value = proc.communicate()[0]
    return str(stdout_value.decode("utf-8"))


def ifNotNull(iffer, elser, nuller=None):
    try:
        if iffer is not None:
            return iffer
        else:
            return elser
    except:
        return elser


def timeFormat(elap):
    elap_h = int(elap//3600)
    elap = elap-elap_h*3600
    elap_m = int(elap//60)
    elap = elap-elap_m*60
    elap_s = int(elap)
    if elap_h < 0:
        elap_h = '-'
        elap_m = '-'
        elap_s = '-'
    elap_h = str(elap_h)
    elap_m = str(elap_m)
    elap_s = str(elap_s)
    return elap_h+"h "+elap_m+"m "+elap_s+"s "


def timeFormatS(elap):
    elap_h = int(elap//3600)
    elap = elap-elap_h*3600
    elap_m = int(elap//60)
    elap = elap-elap_m*60
    elap_s = int(elap)
    if elap_h < 0:
        strung = '-'
    else:
        if elap_h > 0:
            elap_h = str(elap_h)
            elap_m = str(elap_m)
            strung = elap_h+"h "+elap_m+"m"
        elif elap_m > 0:
            elap_m = str(elap_m+1)
            strung = elap_m+"m"
        else:
            elap_s = str(elap_s)
            strung = "~"+elap_s+"s"
    return strung


def timeFormatS2(elap):
    elap_h = int(elap//3600)
    elap = elap-elap_h*3600
    elap_m = int(elap//60)
    elap = elap-elap_m*60
    elap_s = int(elap)
    if elap_h < 0:
        strung = '-'
    else:
        if elap_h > 0:
            elap_h = str(elap_h)
            elap_m = str(elap_m)
            strung = elap_h+":"+elap_m+":"+str(elap_s)
        elif elap_m > 0:
            elap_m = str(elap_m)
            strung = elap_m+":"+str(elap_s)
        else:
            elap_s = str(elap_s)
            strung = "~"+elap_s+"s"
    return strung


def costEstimation(FlengthM, timeH):
    config = load_config()
    pi = 3.14159
    pricePerMeter = float(config["global"]["filamentprice"]/1000 * config["global"]["filamentdensity"]*(pi*(0.175/2)*(0.175/2))*100)
    pricePerHour = float(config["global"]["powerprice"])
    price = round(float(FlengthM)*pricePerMeter+float(timeH)*pricePerHour, 2)
    return price


class Commander(object):
    def __init__(self, cmd=""):
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.running = True
        self.com = threading.Thread(target=self.run)
        self.com.start()
        self.out = ""

    def run(self):
        while self.running:
            self.out = self.process.stdout.read(1)
            if self.out == '' and self.process.poll() is not None:
                self.running = False
            if self.out != '':
                sys.stdout.write(self.out)
                sys.stdout.flush()


def dictDelete(dict, keys=["",""]):
    for key in keys:
        if key in dict:
            del dict[key]
    return dict

english = ["display","date","type","name","size","gcodeAnalysis","estimatedPrintTime","filament","length","volume", "print", "failure", "success", "last"]
deutsch = ["Name", "Datum", "Typ", "Name", "Größe [MB]", "GCODE-Analyse","Geschätzte Druckdauer", "Filament", "Länge", "Volumen", "Druck", "Fehldrucke", "Erfolge","Zuletzt gedruckt"]
def dictTranslate(dictionary, origlang=[""], newlang=[""]):
    # origlang = english
    # newlang = deutsch
    if len(origlang) == len(newlang):
        for idx, word in enumerate(origlang):
            print(word)
            try:
                if word in dictionary:
                    print("dict: " + word+ "type:" + str(type(dictionary[word])))
                    print(dictionary[word])
                    if isinstance(dictionary[word], dict):
                        subdict = dictTranslate(dictionary[word],origlang, newlang)
                        dictionary.pop(word)
                        dictionary[newlang[idx]] = subdict
                    else:
                        dictionary[newlang[idx]] = dictConvert(dictionary.pop(word), newlang[idx])
            except:
                tb = traceback.format_exc()
                print(tb)
    else:
        print("both language lists must have same length")
    return dictionary

def dictConvert(element, elementname):
    if elementname in ["Datum", "Zuletzt gedruckt"]:
        element = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(element))
    elif elementname == "Größe [MB]":
        element = element/1000/1000
    elif elementname == "Geschätzte Druckdauer":
        element = str(datetime.timedelta(seconds=element))
    elif elementname == "Länge":
        element = str(element)+"mm"
    elif elementname == "Volumen":
        element = str(element)+"mm³"

    return element

def dict2HTML(dictionary, cssClass='', pre='<html><head><title>Title of the document</title></head><body>', post='</body></html>'):
        ''' pretty prints a dictionary into an HTML table(s) '''
        if isinstance(dictionary, str):
            return '<td>' + dictionary + '</td>'
        s = [pre+'<table ']
        if cssClass != '':
            s.append('class="%s"' % (cssClass))
        s.append('>\n')
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                s.append('<tr>\n  <td valign="top"><strong>%s</strong></td>\n' % str(key))
                if isinstance(value, dict):
                    if key == 'picture' or key == 'icon':
                        s.append('  <td valign="top"><img src="%s"></td>\n' % dict2HTML(value, cssClass))
                    else:
                        s.append('  <td valign="top">%s</td>\n' % dict2HTML(value, cssClass))
                elif isinstance(value, list):
                    s.append("<td><table>")
                    for i in value:
                        s.append('<tr><td valign="top">%s</td></tr>\n' % dict2HTML(i, cssClass))
                    s.append('</table>')
                else:
                    if key == 'picture' or key == 'icon':
                        s.append('  <td valign="top"><img src="%s"></td>\n' % value)
                    else:
                        s.append('  <td valign="top">%s</td>\n' % value)
                s.append('</tr>\n')
        elif isinstance(dictionary, list):
            for key, value in enumerate(dictionary):
                s.append('<tr>\n  <td valign="top"><strong>%s</strong></td>\n' % str(key))
                if isinstance(value, dict):
                    if key == 'picture' or key == 'icon':
                        s.append('  <td valign="top"><img src="%s"></td>\n' % dict2HTML(value, cssClass))
                    else:
                        s.append('  <td valign="top">%s</td>\n' % dict2HTML(value, cssClass))
                elif isinstance(value, list):
                    s.append("<td><table>")
                    for i in value:
                        s.append('<tr><td valign="top">%s</td></tr>\n' % dict2HTML(i, cssClass))
                    s.append('</table>')
                else:
                    if key == 'picture' or key == 'icon':
                        s.append('  <td valign="top"><img src="%s"></td>\n' % value)
                    else:
                        s.append('  <td valign="top">%s</td>\n' % value)
                s.append('</tr>\n')
        s.append('</table>'+post)
        return '\n'.join(s)

def timeConvert(timeS):
    timeS = float(timeS)
    return time.strftime("%d.%b.%Y %H:%M", time.gmtime(timeS))

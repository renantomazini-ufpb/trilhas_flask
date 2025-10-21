from flask import Flask, url_for, render_template, request, send_file  
import glob                                                            
import json

from urllib.parse import quote_plus
from urllib.parse import unquote_plus
import os

from io import BytesIO
from mutagen import File

from ExtraScripts.minutagem import *



app = Flask(__name__)                                

@app.route("/sounds")                               
def sounds():                                       
    music = request.args.get('music')               
    path = f"static/{music}"                       
    return send_file(path, mimetype="audio/mp3")   

def trocar(stringA):
    stringB = stringA.replace("\\", "/")
    stringA = stringB.replace("musicPlayer/", "")
    print("trocrando " + stringA)
    return stringA

@app.route("/")                                                     
def home():                                                         
    musiclist = glob.glob("musicPlayer/static/musics/*.mp3")        
    musicJ = [                                                      
        {'filename': mi.split("/")[-1],
         "coverURL": url_for('coverImage', music=trocar(mi)),
         #"coverURL": url_for('coverImage', music=quote_plus(trocar(mi))),
        #"coverURL": "/static/images/No_cover.JPG", #('/coverImage', music=trocar(mi)), #Os metadados sumiram!
         'length' : sec2minString(File(mi).info.length),                             
         "fileUrl": url_for('sounds', music=mi.split('/')[-1]),
         'Tags' : None}     
        for mi in musiclist]                                        
    print(musicJ)
    
    for i in range(len(musicJ)):
        tag = File(musiclist[i])
        if('TIT2' in tag.keys()):
            musicJ[i]['Tags'] = {'TIT2':tag['TIT2'].text[0], 'TPE1':tag['TPE1'].text[0]}
    return render_template("home.html",                             
                           musicJ=musicJ,                           
                           musicJson=json.dumps(musicJ))





@app.route("/coverImage")
def coverImage():
    # Corrige a decodificação do parâmetro da URL
    cover_path = unquote_plus(request.args.get("music")).replace("\\", "/")

    # Garante caminho absoluto correto
    if not cover_path.startswith("musicPlayer/"):
        cover_path = os.path.join("musicPlayer", cover_path)

    print(f"Capa path final: {cover_path}")

    if not os.path.exists(cover_path):
        print(f"Arquivo não encontrado: {cover_path}")
        return app.send_static_file('images/No_cover.JPG')

    try:
        cover = File(cover_path)
        if cover and cover.tags and "APIC:" in cover.tags:
            imgcover = cover.tags["APIC:"].data
            strIO = BytesIO(imgcover)
            strIO.seek(0)
            return send_file(strIO, mimetype="image/jpeg")
    except Exception as e:
        print(f"Erro ao ler capa: {e}")

    return app.send_static_file('images/No_cover.JPG')



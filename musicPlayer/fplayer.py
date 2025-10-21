from flask import Flask, url_for, render_template, request, send_file  
import glob                                                            
import json

from urllib.parse import unquote
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
    return stringA

@app.route("/")                                                     
def home():                                                         
    musiclist = glob.glob("musicPlayer/static/musics/*.mp3")        
    musicJ = [                                                      
        {'filename': mi.split("/")[-1],
         "coverURL": "/static/images/No_cover.JPG", #('/coverImage', music=trocar(mi)), #Os metadados sumiram!
         'length' : sec2minString(File(mi).info.length),                             
         "fileURL": url_for('sounds', music=mi.split('/')[-1]),
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
    cover_path = unquote(request.args["music"]).replace("\\", "/")
    
    return app.send_static_file('/static/images/No_cover.JPG')

    if not os.path.exists(cover_path):
        print(f"File not found: {cover_path}")
        return app.send_static_file('/static/images/No_cover.JPG')
    
    try:
        cover = File(cover_path)
        print(f"Trying to open: {cover_path}")
        if "APIC:" in cover.tags:
            imgcover = cover.tags["APIC:"].data
            strIO = BytesIO()
            strIO.write(imgcover)
            strIO.seek(0)
            return send_file(strIO, mimetype="image/jpg")
    except Exception as e:
        print(f"Error reading cover image: {e}")
    
    return app.send_static_file('/static/images/No_cover.JPG')                                              

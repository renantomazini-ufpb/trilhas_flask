from flask import Flask, url_for, render_template, request, send_file  
import glob                                                            
import json                                                            





app = Flask(__name__)                                

@app.route("/sounds")                               
def sounds():                                       
    music = request.args.get('music')               
    path = f"static\\{music}"                       
    return send_file(path, mimetype="audio\\mp3")   

@app.route("/")                                                     
def home():                                                         
    musiclist = glob.glob("musicPlayer 0.1/static/musics/*.mp3")        
    musicJ = [                                                      
        {'filename': mi.split("/")[-1],                             
         "fileURL": url_for('sounds', music=mi.split('/')[-1])}     
        for mi in musiclist]                                        
    print(musicJ)                                                   
    return render_template("home.html",                             
                           musicJ=musicJ,                           
                           musicJson=json.dumps(musicJ))            

if(__name__== "__main__"):                                          
    app.run()                                                       

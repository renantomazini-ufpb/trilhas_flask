from flask import Flask

app = Flask(__name__) # instanciar uma classe Flask

@app.route("/")  # rota onde conteúdo de execução será gerado, as rotas são as urls geradas
def oiMundo():
    return "Oi, mundo!"

if(__name__=="__main__"):
    app.run() # roda o projeto

#ao rodar com 'python oiMundo.py' a saída será:
# running on http://127.0.0.1:5000


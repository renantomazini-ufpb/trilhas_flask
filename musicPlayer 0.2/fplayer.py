from flask import Flask, url_for, render_template, request, send_file  # importa classes e funções do Flask necessárias para criar a app, gerar URLs, renderizar templates, acessar parâmetros da requisição e enviar arquivos
import glob                                                            # módulo para buscar arquivos usando padrões (wildcards)
import json                                                            # módulo para serializar e desserializar JSON

# glob permite encontrar arquivos e pastas  # comentário explicativo adicional
# render template permite a conversa de Jinja e python  # comentário explicativo adicional
# função home será exibida na URL raiz do aplicativo, retornando render template, com parâmetro do template a ser renderizado  # comentário adicional

app = Flask(__name__)                                # instancia a aplicação Flask; __name__ ajuda o Flask a localizar recursos e templates

@app.route("/sounds")                               # define uma rota HTTP para o caminho /sounds que chamará a função abaixo quando acessada
def sounds():                                       # função que trata requisições para /sounds
    music = request.args.get('music')               # lê o parâmetro de query string 'music' da requisição (ex: /sounds?music=nome.mp3)
    path = f"static\\{music}"                       # monta o caminho do arquivo local a partir do nome passado; usa barra invertida no Windows
    return send_file(path, mimetype="audio\\mp3")   # envia o arquivo localizado em path como resposta com o tipo MIME para áudio MP3

@app.route("/")                                                     # define a rota raiz do site (página inicial)
def home():                                                         # função que renderiza a página inicial
    musiclist = glob.glob("musicPlayer 0.1/static/musics/*.mp3")        # busca todos os arquivos .mp3 dentro de musicPlayer/static/musics/ e retorna uma lista de caminhos completos
    musicJ = [                                                      # inicia uma lista por compreensão que conterá dicionários com informações de cada música
        {'filename': mi.split("/")[-1],                             # extrai apenas o nome do arquivo do caminho completo separando por '/' e pegando a última parte
         "fileURL": url_for('sounds', music=mi.split('/')[-1])}     # gera a URL para a rota 'sounds', passando o nome do arquivo como parâmetro 'music'
        for mi in musiclist]                                        # para cada caminho 'mi' encontrado em musiclist
    print(musicJ)                                                   # imprime no console a lista de dicionários (útil para depuração)
    return render_template("home.html",                             # renderiza o template HTML chamado home.html
                           musicJ=musicJ,                           # passa a lista de dicionários musicJ para o template (variável disponível no Jinja)
                           musicJson=json.dumps(musicJ))            # também passa uma string JSON das músicas (útil para consumo via JavaScript no template)

if(__name__== "__main__"):                                          # verifica se o script está sendo executado diretamente (não importado como módulo)
    app.run()                                                       # inicia o servidor de desenvolvimento do Flask com configurações padrão (escuta em localhost:5000)

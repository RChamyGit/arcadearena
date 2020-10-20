from flask import Flask, session, Markup, Response
from flask import request, render_template, url_for, redirect, flash, send_file, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from passlib.hash import sha256_crypt
from dbconnect import connection, check_user_Login, check_user_ID,UpdateQuerySqlMulti3,SelectSqlMultiORDER, SelectSql, UpdateQuerySql,SelectSqlShort, InsertSql, SelectSqlAll,SelectSqlMulti,SelectSqlMulti3,UpdateQuerySqlMulti
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from twitch import TwitchClient
import json
import random
from flask_socketio import *
from testeCallofduty import getuser
dataDia = str(datetime.now().strftime("%d/%m/%Y"))
hora = str(datetime.now().strftime("%H:%M:%S"))
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'my_love_dont_try'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, logger=True)
############ METODOS APLICADOS ####################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def invoice(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'invoice' in session:
            return f(*args, **kwargs)
        else:
            flash("Nao possui nenhum pedido")
            return redirect(url_for('dashboard'))
    return wrap
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Precisa fazer o Login")
            return redirect(url_for('LoginClientes'))
    return wrap
def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))
def convert(list):
    return tuple(list)

##### CRIAR PARTIDAS #####


############ METODOS APLICADOS ####################
############ INDEX ####################
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # c, conn = connection()
        return render_template('index.html')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
#################################### ROTAS DIRETAS ####################################
##### LOGOUT #####
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('Voce esta saindo do APP! Obrigado', 'logout')
    return redirect(url_for('index'))
##### PAGINA ERRO 404 #####
@app.errorhandler(404)
def pag_not_found(e):
    return render_template("404.html")
##### LOGIN #####
@app.route('/area-Login/', methods=['GET', 'POST'])
def LoginClientes():
    return render_template('area-Login.html')
##### RECUPERA SENHA #####
@app.route('/page_forgot_password', methods=['GET', 'POST'])
def email_forgot():
    return render_template('redirect.html')
##### ENVIAR FOTO DO SERVIDOR #####
@app.route('/transfer/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    if filename == None:
        filename = 'teste'
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
##### DASHBOARD #####
@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if request.method == "GET":
        return render_template('dashboard.html')
    if request.method == "POST":
        return render_template('dashboard.html')
##### CANAL PLACAR #####
@app.route('/streaming/placar/channel1', methods=['GET', 'POST'])
def channel1():
    return render_template('canal_placar.html')
#################################### ROTAS DE TRABALHO ####################################


##### REGISTER SQUAD #####
@app.route('/registerSquad', methods=['GET', 'POST'])
def registerSquad():
    lista_players = []
    if request.method == "POST":
        squad = request.form['squadName']
        checkSquadvalid = SelectSql('players', 'squad', squad)
        if checkSquadvalid == 0:
            InsertSql({'nome': squad}, 'squads')
            c = SelectSql('squad', 'nome', squad)
            idsquad = c[0][0]
            player1 = request.form['player1']
            player2 = request.form['player2']
            player3 = request.form['player3']
            lista_players.append(player1)
            lista_players.append(player2)
            lista_players.append(player3)
            for player in lista_players:
                myDict = {}
                myDict.update({
                    'squad': squad,
                    'idsquad': idsquad,
                    'player': player,
                })
                InsertSql(myDict, 'players')

            print('Add Squad ao Banco de Dados')
        if checkSquadvalid > 0:
            print('Squad Já Existe Cadastrada')
        return redirect(url_for('dashboard'))

##### REGISTRAR CAMPEONATO #####
@app.route('/registerCampeonato', methods=['GET', 'POST'])
def registerCampeonato():
    # lista_players = []
    if request.method == "POST":
        campeonatoName = request.form['nomeCategoria']
        checkSquadvalid = SelectSql('campeonatos_ativos', 'nome', campeonatoName)
        print(checkSquadvalid)
        if checkSquadvalid == False:
            modalidade = request.form['modalidade']
            bracket = int(request.form['bracket'])
            regras = request.form['regras']
            myDict = {}
            myDict.update({
                'modalidade': modalidade,
                'nome': campeonatoName,
                'bracket': bracket,
                'data': dataDia,
                'regras': regras,
                'status': bracket,
            })
            InsertSql(myDict, 'campeonatos_ativos')
            print('Add Campeonato ao Banco de Dados')
            idCampeonato = SelectSql('campeonatos_ativos', 'nome', campeonatoName)
            for item in idCampeonato:
                id = item[0]
            return redirect(url_for('bracketSetup', idCampeonato=id))
        if checkSquadvalid != False:
            print('Campeonato Já Existe Cadastrada')
            return redirect(url_for('dashboard'))


##### CRIAR A BRACKET #####
@app.route('/bracketSetup/<idCampeonato>', methods=['GET', 'POST'])
def bracketSetup(idCampeonato):
    if request.method == "GET":
        campeonato = SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', idCampeonato)
        if campeonato != False:
            print('não existe brecket montado')
            for item in campeonato:
                fasedeGrupos = item[6]
                regras = item[8]
                nomeCampeonato = item[1]
                bracket = item[7]
                return render_template('bracketSetup.html',
                                       infoCampeonato=campeonato,
                                       idCampeonato=idCampeonato,
                                       fasedeGrupos=fasedeGrupos,
                                        bracket = int(bracket),
                                        nomeCampeonato=nomeCampeonato,
                                       regras=regras)
        else:
            return redirect(url_for('dashboard'))

##### MOSTRAR A BRACKETLIST #####
@app.route('/campeonatoSetup/<nomeCampeonato>/<idCampeonato>', methods=['GET', 'POST'])
def bracketList(nomeCampeonato,idCampeonato):
    if request.method == 'GET':
        partidas_online = SelectSqlShort('partidas_online', 'idcampeonatos_ativos', idCampeonato, 'score')
        print(partidas_online)
        if partidas_online == False:
            return redirect(url_for('bracketSetup', idCampeonato=idCampeonato))
        if partidas_online != False:
            print('ja existe bracket montado')
            return render_template('bracketList.html',
                                   infoCampeonato=SelectSql('campeonatos_ativos', 'idcampeonatos_ativos',idCampeonato),
                                   games = partidas_online)


##### CONTROLADORES DE PARTIDAS #####
@app.route('/streaming/<grupo>/<idcampeonato>/<idregra>', methods=['GET', 'POST'])
def streamingPartida(grupo,idcampeonato,idregra):
    # url = f'/{campeonato}/{grupo}/{idSquads}'
    # print('teste')
    if request.method == "GET":
        listaSquad = []
        jogadores =[]
        # sub = []
        # print(grupo)
        if 'grupo' in grupo:
            round = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'grupo',grupo)
            for i in round:
                listaSquad.append(i[3])
                nomeCampeonato = i[23]
        else:
            id = grupo.split(',')
            listaSquad.append(id[0])
            listaSquad.append(id[1])
            round = []
            for id in listaSquad:
                select = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'idsquad', id)
                round.append(select[0])
                for i in round:
                    nomeCampeonato = i[23]
                    grupo = 'oitavas'


        print(round)

        regras = SelectSql('regras', 'idregras',idregra)
        print(listaSquad)
        print(grupo)
        for idSquad in listaSquad:
            players = SelectSql('players','idsquad',idSquad)
            jogadores.append(players)
        print(jogadores)
        return render_template('stream.html',listaSquad=listaSquad,round=round,regras=regras,players=jogadores,grupo=grupo,nomeCampeonato=nomeCampeonato,idcampeonato=idcampeonato)


#################################### ROTAS DE SOCKETIO ####################################


@socketio.on('receber partida')
def handle_my_custom_event(data):
    # print(data)
    emit('partida', data, broadcast=True)


@socketio.on('encerrar partida')
def closePartidas(data):
    for i in data:
        print(i['idsquad'])
        myDict = ({
                'status': i['status'],
                'R1J1': i['score_1'],
                'R1J2': i['score_2'],
                'R1J3': i['score_3'],
                'R2J1': i['score_oitava_1'],
                'R2J2': i['score_oitava_2'],
                'R3J1': i['score_quarta_1'],
                'R3J2': i['score_quarta_2'],
                'R4J1': i['score_semi_1'],
                'R4J2': i['score_semi_2'],
                'FINAL_J1': i['score_final_1'],
                'FINAL_J2': i['score_final_2'],
                 'posicao':  i['posicao'],
                'jogo_ativo': i['jogo_ativo'],
                'grupo': i['grupo']
            })

        UpdateQuerySql(myDict,'partidas_online','idsquad',i['idsquad'])
        # if int(i['idsquad']) == int(segundoLugar):
        #     myDict = ({
        #         'status': i['status'],
        #         'R1J1': i['score_1'],
        #         'R1J2': i['score_2'],
        #         'R1J3': i['score_3'],
        #         'R2J1': i['score_oitava_1'],
        #         'R2J2': i['score_oitava_2'],
        #         'R3J1': i['score_quarta_1'],
        #         'R3J2': i['score_quarta_2'],
        #         'R4J1': i['score_semi_1'],
        #         'R4J2': i['score_semi_2'],
        #         'FINAL_J1': i['score_final_1'],
        #         'FINAL_J2': i['score_final_2'],
        #         'posicao':  i['posicao'],
        #         'jogo_ativo':i['jogo_ativo'],
        #         'grupo': i['grupo']
        #     })
        #
        #     UpdateQuerySql(myDict, 'partidas_online', 'idsquad', i['idsquad'])

    # emit('Insert partida', data, broadcast=True)
    # return redirect(url_for('streamingPartida', grupo='', idcampeonato='', idregra=''))

@socketio.on('check Activison')
def Activision(data):
    nrPlayer = data[0]
    tagName = str(data[1])
    IdActvision = str(data[2])
    plataform = str(data[3])
    dataPlayer = getuser(IdActvision,plataform)
    # print(dataPlayer)
    #
    if tagName == '':
        tagName = nrPlayer
    if dataPlayer == str('False'):
        databack = [{'mensagem':'Este Usuário não foi encontrado!'}]
        socketio.emit('Activison negado', databack)
    else:
        dataPlayer.update({
                'player': nrPlayer,
                'tagName': tagName,
            })
        socketio.emit('Activison response', dataPlayer)

@socketio.on('insert Squad')
def InsertSquad(data):
    InsertSql({'squadName': data[3],'nome':data[3]},'squads')
    c = SelectSql('squads', 'squadName', data[3])
    idsquad = c[0][0]

    for player in data[0:3]:
        myDict = ({
            'squad': data[3],
            'idsquad': idsquad,
            'player': player['tagName'],
            'activisionID':player['username'],
            'kills': player['Kills'],
            'wins': player['Wins'],
            'top5': player['TopFive'],
            'deaths': player['Deaths'],
            'KD': player['K/D Ratio'],
            'level':player['level'],
            'plataforma':player['plataform'],
        })
        InsertSql(myDict, 'players')
    socketio.emit('players response')

@socketio.on('dashboard items')
def dash_items():
    print('atualizar Dashboard...')
    data = []
    data.append(SelectSqlAll('modalidades'))
    data.append(SelectSqlAll('regras'))
    campeonatos = SelectSqlAll('campeonatos_ativos')
    if campeonatos != False:
        data.append(campeonatos)
    else:
        data.append([''])
    squads = SelectSqlAll('squads')
    if squads != False:
        data.append(SelectSqlAll('squads'))
    else:
        data.append([''])
    socketio.emit('dashboard response', data)

@socketio.on('bracket setup')
def dash_items():
    data = []
    data.append(SelectSqlAll('squads'))
    # data.append(SelectSqlAll('regras'))

    socketio.emit('bracket setup response', data)
@socketio.on('submit bracket')
def bracket_mount(data):
    idcampeonato = data[0]
    fasedeGrupos= data[1]
    regras = data[2]
    nomeCampeonato = data[3]
    listaSquad= data[4:]
    # limiter = len(listaSquad)
    random.shuffle(listaSquad)
    teste = list(chunker_list(listaSquad, int(fasedeGrupos)))
    for c in range(len(list(teste))):
        grupo = f'grupo {c + 1}'
        for myDict in teste[c]:
            myDict.update({
                            'braket': int(fasedeGrupos),
                            'grupo': grupo,
                            'idcampeonatos_ativos': idcampeonato,
                            'nomeCampeonato': nomeCampeonato,
                            'score':0,
                            'regras':regras,
                            'status': fasedeGrupos,
                            'braket': fasedeGrupos,
                        })
            make_partidas(myDict)
    mensagem = [nomeCampeonato]
    socketio.emit('salved', mensagem)

def make_partidas(myDict):
    if int(myDict['status']) == 1:
        myDict.update({'jogo_ativo':'R2J1','R2J1':0,'R2J2': 0})
    if int(myDict['status']) == 8:
        myDict.update({'jogo_ativo':'R1J1','R1J1': 0,'R1J2': 0,'R1J3': 0})
    if int(myDict['status']) == 16:
        myDict.update({'jogo_ativo':'R1J1','R1J1': 0,'R1J2': 0,'R1J3': 0})
    InsertSql(myDict, 'partidas_online')







if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app, port=5002, debug=True)
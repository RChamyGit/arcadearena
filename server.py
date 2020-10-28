from flask import Flask, session, Markup, Response
from flask import request, render_template, url_for, redirect, flash, send_file, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from passlib.hash import sha256_crypt
from dbconnect import connection, check_user_Login, check_user_ID,UpdateQuerySqlMulti3,SelectSqlMultiORDER,UpdateQuerySqlMultiINSERTS, SelectSql, UpdateQuerySql,SelectSqlShort, InsertSql, SelectSqlAll,SelectSqlMulti,SelectSqlMulti3,UpdateQuerySqlMulti
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory


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
socketio = SocketIO(app, async_handlers=True)
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

@app.route('/streaming/placar/card', methods=['GET', 'POST'])
def cards():
    return render_template('player_overlay.html')


@app.route('/streaming/placar/versus', methods=['GET', 'POST'])
def versus():
    return render_template('versus.html')
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
# @app.route('/dataBase', methods=['GET', 'POST'])
# def allDataBase():
#     if request.method == "POST":
#         rf = request.form
#         for keys in rf.keys():
#             data = keys
#         loaded_json = json.loads(data)
#         idcampeonato = loaded_json['idcampeonato']
#         partidas_online = SelectSqlShort('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'score')
#         return make_response(jsonify(partidas_online), 200)
#


@app.route('/campeonatoSetup/<nomeCampeonato>/<idCampeonato>', methods=['GET', 'POST'])
def bracketList(nomeCampeonato,idCampeonato):
    if request.method == 'GET':
        partidas_online = SelectSqlShort('partidas_online', 'idcampeonatos_ativos', idCampeonato, 'grupo')
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

        jogadores =[]
        listaIdPartidas = []
        text = grupo.split(',')
        listaSquad = text[1:]
        round = []
        for team in listaSquad:
            partida = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'idsquad', team)
            for i in partida:
                nomeCampeonato = i[23]
                jogo_ativo = i[26]
                listaIdPartidas.append(i[0])
                status = i[9]
                grupoInsert = i[22]
                round.append(i)


        # if 'grupo' in grupo:
        #     round = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'grupo',grupo)
        #     for i in round:
        #         listaSquad.append(i[3])
        #         nomeCampeonato = i[23]
        #         jogo_ativo = i[26]
        #         listaIdPartidas.append(i[0])
        #         status = i[9]
        # else:
        #     id = grupo.split(',')
        #     listaSquad.append(id[0])
        #     listaSquad.append(id[1])
        #     round = []
        #     for id in listaSquad:
        #         select = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'idsquad', id)
        #         round.append(select[0])
        #         for i in round:
        #             nomeCampeonato = i[23]
        #             grupo = 'oitavas'
        #             jogo_ativo = i[26]
        #             listaIdPartidas.append(i[0])
        regras = SelectSql('regras', 'idregras',idregra)
        for idSquad in listaSquad:
            players = SelectSql('players','idsquad',idSquad)
            jogadores.append(players)
        print(round)
        print(jogadores)
        return render_template('stream.html',
                               listaSquad=listaSquad,
                               listaPartidasID = listaIdPartidas,
                               round=round,
                               regras=regras,
                               jogo_ativo=jogo_ativo,
                               players=jogadores,
                               grupo=grupoInsert,
                               status=status,
                               nomeCampeonato=nomeCampeonato,
                               idcampeonato=idcampeonato)


@app.route('/streaming_finais/<time1>/<time2>/<status>/<idcampeonato>/<idregra>', methods=['GET', 'POST'])
def streamingPartida_finais(time1,time2,status,idcampeonato,idregra):
    # url = f'/{campeonato}/{grupo}/{idSquads}'
    print('teste')
    if request.method == "GET":
        listaSquad = []
        jogadores =[]
        listaIdPartidas = []
        partidas = []
        #
        # if 'grupo' in grupo:
        regras = SelectSql('regras', 'idregras', idregra)
        if int(status) == 1:
            timeA = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'posicao_R2',time1)
            timeB = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'posicao_R2', time2)
            partidas.append(timeA)
            partidas.append(timeB)
            listaSquad.append(timeA[0][3])
            listaSquad.append(timeB[0][3])
            nomeCampeonato = timeA[0][23]
        if int(status) == 2:
            timeA = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'posicao_R3',time1)
            timeB = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'posicao_R3', time2)
            partidas.append(timeA)
            partidas.append(timeB)
            listaSquad.append(timeA[0][3])
            listaSquad.append(timeB[0][3])
            nomeCampeonato = timeA[0][23]

        if int(status) == 3:
            timeA = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'posicao_R4',time1)
            timeB = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'posicao_R4', time2)
            partidas.append(timeA)
            partidas.append(timeB)
            listaSquad.append(timeA[0][3])
            listaSquad.append(timeB[0][3])
            nomeCampeonato = timeA[0][23]

        #     for i in round:
        #         listaSquad.append(i[3])
        #         nomeCampeonato = i[23]
        #         jogo_ativo = i[26]
        #         listaIdPartidas.append(i[0])
        #         status = i[9]
        # else:
        #     id = grupo.split(',')
        #     listaSquad.append(id[0])
        #     listaSquad.append(id[1])
        #     round = []
        #     for id in listaSquad:
        #         select = SelectSqlMulti('partidas_online', 'idcampeonatos_ativos', idcampeonato, 'idsquad', id)
        #         round.append(select[0])
        #         for i in round:
        #             nomeCampeonato = i[23]
        #             grupo = 'oitavas'
        #             jogo_ativo = i[26]
        #             listaIdPartidas.append(i[0])
        # regras = SelectSql('regras', 'idregras',idregra)
        print(listaSquad)
        for idSquad in listaSquad:
            players = SelectSql('players','idsquad',idSquad)
            jogadores.append(players)
        print(jogadores)
        return render_template('streaming.html',
                               listaSquad=listaSquad,
        #                        listaPartidasID = listaIdPartidas,
                               round=partidas,
                               regras=regras,
        #                        jogo_ativo=jogo_ativo,
                               players=jogadores,
                               grupo=[time1,time2],
                               status=status,
                               nomeCampeonato=nomeCampeonato,
                               idcampeonato=idcampeonato
                                      )

#################################### ROTAS DE SOCKETIO ####################################

@socketio.on('update')
def update(data):

    for each in data:
        if int(each['status']) == 8:
            UpdateQuerySqlMultiINSERTS('partidas_online','R1J1' ,each['score_1'],'R1J2',each['score_2'],'R1J3', each['score_3'],'idpartidas_online',each['id'])
        if int(each['status']) == 1:
            UpdateQuerySqlMultiINSERTS('partidas_online','R2J1' ,each['score_1'],'hora',dataDia,'R2J2',each['score_2'],'idpartidas_online',each['id'])
        if int(each['status']) == 2:
            UpdateQuerySqlMultiINSERTS('partidas_online','R3J1' ,each['score_1'],'hora',dataDia,'R3J2',each['score_2'],'idpartidas_online',each['id'])
        if int(each['status']) == 3:
            UpdateQuerySqlMultiINSERTS('partidas_online','R4J1' ,each['score_1'],'hora',dataDia,'R4J2',each['score_2'],'idpartidas_online',each['id'])

        # UpdateQuerySql(myDict,'partidas_online','idpartidas_online',each['id'])

    emit('times', data, broadcast=True)






@socketio.on('receber partida')
def handle_my_custom_event(data):
    emit('partida', data, broadcast=True)

@socketio.on('receber kills')
def handle_kills(data):
    emit('kills update', data, broadcast=True)
@socketio.on('receber rank')
def handle_rank(data):
    emit('rank update', data, broadcast=True)

@socketio.on('receber stage')
def handle_rank(data):
    emit('stage update', data, broadcast=True)

@socketio.on('receber player')
def handle_rank(data):
    emit('card', data, broadcast=True)

@socketio.on('encerrar partida')
def closePartidas(data):
    print(data)
    if int(data['status']) == 3:
        if data['grupo'] == 'S1S2' or data['grupo'] == 'S2S1':
            proximaPosicao = 'FF1'
        if data['grupo'] == 'S3S4' or data['grupo'] == 'S4S3':
            proximaPosicao = 'FF2'
        dictPrimeiroLugar = ({
            'posicao_R5': proximaPosicao,
            'jogo_ativo': 'R5J1',
            'status': '4',
            'R5J1': 0,
            'R5J2': 0
        })
        UpdateQuerySql(dictPrimeiroLugar, 'partidas_online', 'idpartidas_online', data['ganhador'])

    if int(data['status']) == 2:
        if data['grupo'] == 'Q1Q2' or data['grupo'] == 'Q2Q1':
            proximaPosicao = 'S1'
        if data['grupo'] == 'Q3Q4' or data['grupo'] == 'Q4Q3':
            proximaPosicao = 'S2'
        if data['grupo'] == 'Q5Q6' or data['grupo'] == 'Q6Q5':
            proximaPosicao = 'S3'
        if data['grupo'] == 'Q7Q8' or data['grupo'] == 'Q8Q7':
            proximaPosicao = 'S4'
        dictPrimeiroLugar = ({
            'posicao_R4': proximaPosicao,
            'jogo_ativo': 'R4J1',
            'status': '3',
            'R4J1': 0,
            'R4J2': 0
        })
        UpdateQuerySql(dictPrimeiroLugar, 'partidas_online', 'idpartidas_online', data['ganhador'])



    if int(data['status']) == 1:

        if data['grupo'] == 'A1B2' or data['grupo'] == 'B2A1':
            proximaPosicao = 'Q1'
        if data['grupo'] == 'A2B1' or data['grupo'] == 'B1A2':
            proximaPosicao = 'Q2'
        if data['grupo'] == 'C1D2' or data['grupo'] == 'D2C1':
            proximaPosicao = 'Q3'
        if data['grupo'] == 'D1C2' or data['grupo'] == 'C2D1':
            proximaPosicao = 'Q4'
        if data['grupo'] == 'E1F2' or data['grupo'] == 'F2E1':
            proximaPosicao = 'Q5'
        if data['grupo'] == 'F1E2' or data['grupo'] == 'E2F1':
            proximaPosicao = 'Q6'
        if data['grupo'] == 'G1H2' or data['grupo'] == 'H2G1':
            proximaPosicao = 'Q7'
        if data['grupo'] == 'H1G2' or data['grupo'] == 'G2H1':
            proximaPosicao = 'Q8'

        dictPrimeiroLugar = ({
            'posicao_R3': proximaPosicao,
            'jogo_ativo': 'R3J1',
            'status': '2',
            'R3J1': 0,
            'R3J2': 0
        })
        UpdateQuerySql(dictPrimeiroLugar, 'partidas_online', 'idpartidas_online', data['ganhador'])



    if int(data['status']) == 8:
        if data['grupo'] == 'grupo 1':
            netxGrupo = 'A'
        if data['grupo'] == 'grupo 2':
            netxGrupo = 'B'
        if data['grupo'] == 'grupo 3':
            netxGrupo = 'C'
        if data['grupo'] == 'grupo 4':
            netxGrupo = 'D'
        if data['grupo'] == 'grupo 5':
            netxGrupo = 'E'
        if data['grupo'] == 'grupo 6':
            netxGrupo = 'F'
        if data['grupo'] == 'grupo 7':
            netxGrupo = 'G'
        if data['grupo'] == 'grupo 8':
            netxGrupo = 'H'


        posicaoGanhador = netxGrupo+ '1'
        posicaoSegundo = netxGrupo + '2'

        dictPrimeiroLugar = ({
            'posicao_R2': posicaoGanhador,
            'jogo_ativo': 'R2J1',
            'status': '1',
            'R2J1' : 0,
            'R2J2':0

        })
        dictSegundoLugar = ({
            'posicao_R2': posicaoSegundo,
            'jogo_ativo': 'R2J1',
            'status': '1',
            'R2J1': 0,
            'R2J2': 0
        })
        UpdateQuerySql(dictPrimeiroLugar,'partidas_online','idpartidas_online',data['ganhador'])
        UpdateQuerySql(dictSegundoLugar, 'partidas_online', 'idpartidas_online', data['segundo'])

    emit('done', data, broadcast=True)

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
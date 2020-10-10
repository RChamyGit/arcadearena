from flask import Flask, session, Markup, Response
from flask import request, render_template, url_for, redirect, flash, send_file, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from passlib.hash import sha256_crypt
from dbconnect import connection, check_user_Login, check_user_ID, SelectSql, UpdateQuerySql, InsertSql, SelectSqlAll,SelectSqlMulti,SelectSqlMulti3,UpdateQuerySqlMulti
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from twitch import TwitchClient
import json
import random

from flask_socketio import *

from testeCallofduty import getuser

# mes = str(datetime.now().strftime("%B"))
# dia = str(datetime.now().strftime("%d-%B"))


dataDia = str(datetime.now().strftime("%d/%m/%Y"))
hora = str(datetime.now().strftime("%H:%M:%S"))

num_Os = []
user_online = []
app = Flask(__name__)

from twitchAPI.twitch import Twitch

# # create instance of twitch API
# twitch = Twitch('0pchn2lklol7r0zgsot6kszdoyfi0g', 'brr889niymrsgv9eslbvghxw4zqubg')
# twitch.authenticate_app([])
#
# # get ID of user
# user_info = twitch.get_users(logins=['raggaxe'])
# user_id = user_info['data'][0]['id']
#
# print(user_info)
#


mail_settings = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': 'rafael.figueiradafoz@gmail.com',
    'MAIL_PASSWORD': 'ttvjkembddcfqjxs'

}
app.config.update(mail_settings)

mail = Mail(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootpass@localhost/festa_facil'

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'my_love_dont_try'

socketio = SocketIO(app, logger=True)


############ METODOS APLICADOS ####################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


# @app.route('/refresh_placar', methods=['GET', 'POST'])
# def placar():
#     if request.method == "POST":
#         data_json = []
#         # loaded_json = json.loads(request.data)
#         # print(loaded_json)


############ ROTAS DIRETAS ####################
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('Voce esta saindo do APP! Obrigado', 'logout')
    return redirect(url_for('index'))


@app.errorhandler(404)
def pag_not_found(e):
    return render_template("404.html")


@app.route('/area-Login/', methods=['GET', 'POST'])
def LoginClientes():
    return render_template('area-Login.html')


@app.route('/page_forgot_password', methods=['GET', 'POST'])
def email_forgot():
    return render_template('redirect.html')


@app.route('/transfer/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    if filename == None:
        filename = 'teste'
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


############ ROTAS LOGIN / DASHBOARD ####################


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     error = ''
#     try:
#         if request.method == 'POST':
#             email = request.form['email']
#             password = request.form['password']
#             user = check_user_Login(email)
#             if user == False:
#                 flash(f'Login não encontrado, verifique se digitou corretamente "{email}" ', 'login')
#                 return redirect(url_for('LoginClientes'))
#             else:
#                 for person in user:
#                     id = person[0]
#                     check_password = person[2]
#                     nome = person[3]
#                     apelido = person[4]

#                     if sha256_crypt.verify(password, check_password):
#                         session['logged_in'] = True
#                         session['email'] = email
#                         session['Nome'] = f'{nome} {apelido}'
#                         session['ID_User'] = id
#                         return redirect(url_for('dashboard'))
#                     else:
#                         flash("Senha Errada, confira e tenta novamente", 'erro')
#                         return redirect(url_for('LoginClientes'))
#
#             # if email == "admin@admin.com" and password == "123456":
#             #     session['admin'] = True
#             #
#             #
#             #
#             #
#             #     return redirect(url_for('dashboard'))
#             #
#
#         return render_template("index.html", error=error)
#
#     except Exception as e:
#         # flash(e)
#         return render_template("clientes-Login.html", error=error)


############ ROTAS DE TRABALHO ####################

##### DASHBOARD #####


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    squadList = []
    if request.method == "GET":
        # players_select = SelectSqlAll('players')
        # partidas_online = SelectSqlAll('partidas_online')
        # modalidades = SelectSqlAll('modalidades')
        # campeonatos_online = SelectSqlAll('campeonatos_ativos')
        # regras = SelectSqlAll('regras')
        #
        # if campeonatos_online == 0:
        #     campeonatos_online = ''
        # for files in players_select:
        #     squadName = files[1]
        #     if squadName in squadList:
        #         pass
        #     else:
        #         squadList.append(squadName)
        # if partidas_online == False:
        #     partidas_online = ''
        # if partidas_online != False:
        #     faseGrupos = []
        #     superList = []
        #
        #     for item in partidas_online:
        #         grupo = item[22]
        #         nomeCampeonato = item[23]
        #
        #         if grupo not in faseGrupos:
        #             faseGrupos.append(grupo)
        #         else:
        #             pass
        #     i = 0
        #
        #     listaIds = []
        #     for g in faseGrupos:
        #
        #         selectGroup = SelectSql('partidas_online', 'grupo', g)
        #         for allid in selectGroup:
        #             ids = allid[0]
        #
        #             listaIds.append(ids)
        #         i = i + 1
        #         # print(listaIds)
        #         tempList = ({
        #             'select': selectGroup,
        #             'grupo': g,
        #             'id': i,
        #             'idSquads': listaIds,
        #             'campeonato': nomeCampeonato
        #         })
        #
        #         superList.append(tempList)
        # for sq in squadList:
        #     checkSquad = SelectSql('squads', 'nome', sq)
        #     if checkSquad == 0:
        #         InsertSql({'nome': sq}, 'squads')
        #     else:
        #         pass
        # return render_template('dashboard.html',
        #                        squadName=squadList,
        #                        partidaOnline=superList,
        #                        modalidades=modalidades,
        #                        regras=regras,
        #                        campeonatos_online=campeonatos_online)
        return render_template('dashboard.html')
    if request.method == "POST":
        return render_template('dashboard.html')


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


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


def convert(list):
    return tuple(list)





@app.route('/campeonatoSetup/<nomeCampeonato>/<idCampeonato>', methods=['GET', 'POST'])
def bracketList(nomeCampeonato,idCampeonato):
    if request.method == 'GET':
        data = []
        # bracketCheck = SelectSql('bracket', 'idcampeonatos_ativos', idCampeonato)
        partidas_online = SelectSql('partidas_online', 'idcampeonatos_ativos', idCampeonato)
        if partidas_online == False:
            return redirect(url_for('bracketSetup', idCampeonato=idCampeonato))
        if partidas_online != False:
            print('ja existe bracket montado')

            # bracketList = []
            # listGroup = []
            # grups = []
            # # rounds =  ['R1','R2','R3','R4','FINAL','SUBFINAL']

            for item in partidas_online:
            #     totalPosition = item[28].split('_')
            #     # print(totalPosition)
            #     round = totalPosition[0]
                bracket = item[9]
            #
            #
            #     data.append(item)

        # socketio.emit('braket mount', data)
            #     grupoNr = item[2].strip('grupo ')
            #     grupo = f'grupo {grupoNr}'
            #     totalPosition = item[12].split('_')
            #     # print(totalPosition)
            #     round = totalPosition[0]
            #     bracket = item[4]
            #
            #
            #
            #     if bracket == 1:
            #         if round != 'R1':
            #             print(round)
            #             bracketList.append(item)
            #
            #     if bracket != 1:
            #         if grupo not in listGroup:
            #             listGroup.append(grupo)
            #     for field in listGroup:
            #         subGrupo = []
            #         if field == grupo:
            #             subGrupo.append(item)
            #         bracketList.append(subGrupo)
            #
            # print(listGroup)
        # print(data)
            return render_template('bracketList.html',
                                   infoCampeonato=SelectSql('campeonatos_ativos', 'idcampeonatos_ativos',idCampeonato),
                                   partidas = partidas_online,
                                   bracket = bracket)
                               # round = round

                                           # bracket=bracketList,)

                        # print(round)
                        # print(posicao)
                        # print('')

            #
            #         # grups.append([{f'{grupo}':f'{item}'}])
            #
            #     else:
            #         pass
            # # print(grups)
            #
            # for field in listGroup:
            #     c, conn = connection()
            #     query = "SELECT * FROM bracket WHERE idcampeonatos_ativos = %s AND grupo = %s"
            #     values = (idCampeonato, field)
            #     c.execute(query, values)
            #     teste = c.fetchall()
            #     grups.append(teste)



        # return render_template('bracketList.html',
        #
        #                        infoCampeonato=SelectSql('campeonatos_ativos', 'idcampeonatos_ativos',idCampeonato),
        #                        bracket1=grups[0:4],
        #                        bracket2=grups[4:9],
        #                        check=check,
        #                        dia=dataDia)


@app.route('/bracketSetup/<idCampeonato>', methods=['GET', 'POST'])
def bracketSetup(idCampeonato):
    bracketCheck = SelectSql('bracket', 'idcampeonatos_ativos', idCampeonato)
    # print(f'bracketCheck: {bracketCheck}')
    if request.method == "GET":
        if bracketCheck == False:
            campeonato = SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', idCampeonato)
            if campeonato != False:
                print('não existe brecket montado')
                for item in campeonato:
                    fasedeGrupos = item[7]
                    regras = item[8]
                    nomeCampeonato = item[1]
                # print(nomeCampeonato)
                    return render_template('bracketSetup.html',
                                       infoCampeonato=campeonato,
                                       idCampeonato=idCampeonato,
                                       fasedeGrupos=fasedeGrupos,
                                        nomeCampeonato=nomeCampeonato,
                                       regras=regras)
        else:
            return redirect(url_for('dashboard'))
        #                                           # squadList=squad
                                   # )
        # if bracketCheck != False:
        #     print('ja existe bracket montado')
        #     for limite in bracketCheck:
        #         limiterGroup = limite[4]
        #     return redirect(url_for('bracketList', idCampeonato=idCampeonato, limite=limiterGroup))

    # if request.method == "POST":
    #     if bracketCheck == False:
    #         campeonato = SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', idCampeonato)
    #         for b in campeonato:
    #             braket = b[7]
    #             nomeCampeonato = b[1]
    #             regras = b[8]
    #             status = b[6]
    #         print(f'braket {braket}')
    #         # squad = SelectSqlAll('squads')
    #         limiter = int(request.form['equipesNumber'])
    #         print(f'limiter: {limiter}')
    #
    #         data = []
    #         squadSelect = []
    #         for post in request.form:
    #             if 'valueSquad_' in post:
    #                 data.append(post)
    #         for form in data:
    #             request_form = request.form[form]
    #
    #             squadSelect.append(request_form)
    #         print(f'SquadSelect: {squadSelect}')
    #
    #         random.shuffle(squadSelect)
    #         counter = len(squadSelect)
    #         print(f'SquadSelect MIXADAS: {squadSelect}')
    #         print(f'CONTADOR de SQUADS: {counter} SQUADs')
    #
    #         if counter < limiter:
    #             print('impossivel dividir ..... minimo 16 equipes')
    #             pass
    #         if counter >= limiter:
    #             teste = list(chunker_list(squadSelect, int(braket)))
    #             print(teste)
    #             myDict = {}
    #             for c in range(len(teste)):
    #                 grupo = f'grupo {c + 1}'
    #                 for sq in teste[c]:
    #                     # print(sq)
    #                     squadName = SelectSql('squads', 'idsquads', sq)
    #                     for jk in squadName:
    #                         name = jk[1]
    #                     myDict.update({
    #                         'braket': int(braket),
    #                         'grupo': grupo,
    #                         'idcampeonatos_ativos': idCampeonato,
    #                         'squad': sq,
    #                         'nomeCampeonato': nomeCampeonato,
    #                         'squadName': name,
    #                         'score': 0,
    #                         'regras': regras,
    #                         'status': status})
    #
    #                     InsertSql(myDict, 'bracket')
    #                     print(myDict)
    #
    #         # return render_template('bracketSetup.html', infoCampeonato=campeonato, squadList=squad)
    #         openBracket = SelectSql('bracket', 'idcampeonatos_ativos', idCampeonato)
    #
    #         for itens in openBracket:
    #             idbracket = itens[0]
    #             refGroup = itens[2]
    #             idSquad = itens[3]
    #             nameSquad = itens[5]
    #             status = itens[6]
    #             roundGroupsDict = ({
    #                 'idbracket': idbracket,
    #                 'idcampeonatos_ativos': idCampeonato,
    #                 'nomeCampeonato': nomeCampeonato,
    #                 'idsquad': idSquad,
    #                 'nome': nameSquad,
    #                 'status': status,
    #                 'grupo': refGroup,
    #                 'regras': regras,
    #                 'braket': braket
    #             })
    #
    #             if status == 'OITAVAS':
    #                 roundGroupsDict.update({
    #                     'jogo_ativo':'R2J1',
    #                 })
    #                 UpdateQuerySql({'jogo_ativo':'R2J1'},'bracket','squad',idSquad)
    #
    #             if status == 'GRUPOS':
    #                 roundGroupsDict.update({
    #                      'jogo_ativo':'R1J1',
    #                 })
    #                 UpdateQuerySql({'jogo_ativo': 'R1J1'}, 'bracket', 'squad', idSquad)
    #
    #             InsertSql(roundGroupsDict, 'partidas_online')
    #
    #         return redirect(url_for('bracketList', idCampeonato=idCampeonato))
    #     if bracketCheck != False:
    #         print('ja existe bracket montado')
    #         return redirect(url_for('bracketList', idCampeonato=idCampeonato))

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
            status = ''

            if bracket == 1:
                status = 'OITAVAS'
            if bracket == 8:
                status = 'GRUPOS'
            if bracket == 16:
                status = 'GRUPOS'

            print(bracket)
            print(status)
            myDict = {}
            myDict.update({
                'modalidade': modalidade,
                'nome': campeonatoName,
                'bracket': bracket,
                'data': dataDia,
                'regras': regras,
                'status': status,
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

@app.route('/iniciarPartida', methods=['GET', 'POST'])
def iniciarPartida():
    if request.method == "POST":
        nomeSquadA = request.form.get('nomeSquadA')
        categoria = request.form.get('categoriaPartida')
        cat = SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', categoria)
        for i in cat:
            tipo = i[1]
        if nomeSquadA != None:
            myDict = {'squadA': nomeSquadA,
                      'data': dataDia,
                      'tipo': tipo,
                      'status': 'ativo'
                      }
            InsertSql(myDict, 'partidas_online')
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))

def ScoreRanK(colocacaoPartida,killscount,rule,totalkills):
    fromRules = SelectSql('regras', 'idregras', rule)
    for key in fromRules:
        multiplicadorKill = int(key[6])
        primeiroLugar = int(key[1])
        segundoLugar = int(key[2])
        terceirooLugar = int(key[3])
        quarto_Decimo = int(key[4])
        decimoPrimeiro_decimoQuinto = int(key[5])
    if colocacaoPartida == 0 or colocacaoPartida > 15:
        scoreRank = 0
    if colocacaoPartida == 1:
        scoreRank = primeiroLugar
    if colocacaoPartida == 2:
        scoreRank = segundoLugar
    if colocacaoPartida == 3:
        scoreRank = terceirooLugar
    if 4 <= colocacaoPartida <= 10:
        scoreRank = quarto_Decimo
    if 11 <= colocacaoPartida <= 15:
        scoreRank = decimoPrimeiro_decimoQuinto


    scorePlayer = (killscount * multiplicadorKill) + scoreRank
    scoreEquipe = (totalkills * multiplicadorKill) + scoreRank
    # print(f'SCORE Ranking: {scoreRank}')
    # print(f'SCORE DO JOGADOR: {scorePlayer}')
    # print(f'SCORE DO EQUIPE: {scoreEquipe}')


    return scorePlayer, scoreEquipe





################### ESTE eh o STREAMMMMM ##############


# @app.route('/arcadeArena/<campeonato>/<grupo>/<idSquads>', methods=['GET', 'POST'])
# def placarConverte(campeonato, grupo, idSquads):
#     if request.method == "POST":
#         try:
#             count = 0
#             data = json.loads(request.data)
#             listaKills = []
#             colocacaoFinal = []
#             stage = ''
#             for item in data:
#                 for i in item:
#                     idSquad = item['idSquad']
#                     idcampeonato = item['idcampeonato']
#                     # print(item)
#                     if 'round' in item['name']:
#                         stage = item['value']
#                     if 'kills' in item['name']:
#                         idPlayer = item['name'].strip('kills')
#                         kills = item['value']
#                         myDict = ({
#                             'idplayer': idPlayer,
#                             'kills': kills,
#                         })
#                         if myDict not in listaKills:
#                             listaKills.append(myDict)
#                     else:
#                         for game in listaKills:
#                             game.update({
#                                 'jogo': item['name'],
#                                 'rank_partida': item['value']
#                             })
#
#             campeonato = SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', idcampeonato)
#             rule = ""
#             for rules in campeonato:
#                 rule = rules[8]
#             totalkills = 0
#             for g in listaKills:
#                 totalkills = totalkills + int(g['kills'])
#             for each in listaKills:
#                 killscount = int(each['kills'])
#                 colocacaoPartida = int(each['rank_partida'])
#                 jogo = each['jogo']
#                 print(f'Colocacao na partida : {colocacaoPartida}')
#                 scoreEquipe = ScoreRanK(colocacaoPartida,killscount,rule,totalkills)
#
#
#                 newDict = ({
#                     'kills': killscount,
#                     'score_partida': scoreEquipe[0],
#                     'score_equipe':scoreEquipe[1],
#                     'rank_partida':colocacaoPartida,
#                 })
#                 selectPoint = SelectSqlMulti('rank', 'idplayer', each['idplayer'], 'ativo', jogo)
#
#                 UpdateQuerySql({jogo: scoreEquipe[1]}, 'partidas_online', 'idsquad', idSquad)
#
#                 # print(selectPoint)
#                 idRankSelect = selectPoint[0][0]
#                 UpdateQuerySql(newDict,'rank','idrank',idRankSelect)
#                 # for num in SelectCountTotalScore:
#                 #     count = count + int(num[7])
#                 if stage != '':
#                     if stage == 'R1J1':
#                         next = 'R1J2'
#                     if stage == 'R1J2':
#                         next = 'R1J3'
#                     if stage == 'R1J3':
#                         next = 'R1J1'
#                     UpdateQuerySql({'jogo_ativo': next}, 'partidas_online', 'idsquad', idSquad)
#                     UpdateQuerySql({'jogo_ativo': next}, 'bracket', 'squad', idSquad)
#                     UpdateQuerySql({'ativo': 'no'}, 'rank', 'idrank', idRankSelect)
#                     nextPoint = SelectSqlMulti('rank', 'idplayer', each['idplayer'], 'jogo', next)
#                     idNextPoint = nextPoint[0][0]
#                     UpdateQuerySql({'ativo': next}, 'rank', 'idrank', idNextPoint)
#             data_json = []
#             SelectCountTotalScore = SelectSql('rank', 'idplayer', idPlayer)
#             # print(SelectCountTotalScore)
#             for yep in SelectCountTotalScore:
#                 count = count + int(yep[7])
#             UpdateQuerySql({'score_total': count}, 'rank', 'idSquad', idSquad)
#             UpdateQuerySql({'score':count}, 'bracket', 'squad', idSquad)
#             UpdateQuerySql({'score': count}, 'partidas_online', 'idsquad', idSquad)
#             return make_response(jsonify(data_json), 200)
#
#         except Exception as e:
#             print(f' ERROR: {str(e)}')
#             return (str(e))


def fillDictRAnk(idpartida_online,idplayer,idcampeonato,idSquad,player,squad,status,jogo,jogo_ativo):
    myDictRankIncialGrupos = ({
    'idpartida_online': idpartida_online,
    'idplayer': idplayer,
    'idcampeonato': idcampeonato,
    'idSquad': idSquad,
    'player': player,
    'kills': '0',
    'squad': squad,
    'score_equipe': 0,
    'status': status,
    'jogo': jogo,
    'rank_partida': 0,
    'score_partida': 0,
    'ativo': jogo_ativo,
    'score_total': 0
})
    return myDictRankIncialGrupos




@app.route('/streaming/<campeonato>/<grupo>/<fasedeGrupos>/<idcampeonato>/', methods=['GET', 'POST'])
def streamingPartida(campeonato, grupo,fasedeGrupos,idcampeonato):

    # url = f'/{campeonato}/{grupo}/{idSquads}'
    if request.method == "GET":
        listaSquad = []
        completa =[]
        sub = []
        select = SelectSqlMulti('partidas_online','idcampeonatos_ativos',idcampeonato,'grupo',grupo)
        # print(select)
        for i in select:
            idteam = i[3]
            listaSquad.append(idteam)
            jogo_ativo = i[26]
            check = SelectSqlMulti3('rank', 'idSquad', idteam, 'ativo', jogo_ativo,'idcampeonato',idcampeonato)
            # check = SelectSqlMulti('rank', 'idSquad', idteam, 'idcampeonato', idcampeonato)
            # print(check)
            if check == False:
                print('nao achou ranking')
                make_ranking(idteam, fasedeGrupos, idcampeonato)
                new = SelectSqlMulti3('rank', 'idSquad', idteam, 'ativo', jogo_ativo,'idcampeonato',idcampeonato)
                equipe = []
                for x in new:
                    Channel = x[15]
                    if Channel == None:
                        Channel = 'off'
                    # print(Channel)
                    myDict = ({
                        'idrank': str(x[0]),
                        'idpartida_online': x[1],
                        'idplayer': x[2],
                        'idcampeonato': x[8],
                        'idSquad': x[9],
                        'player': x[5],
                        'kills': x[3],
                        'squad': x[6],
                        'score_equipe': x[7],
                        'status': x[4],
                        'rank_partida': x[10],
                        'score_partida': x[11],
                        'jogo': str(x[12]),
                        'jogo_ativo': x[13],
                        'score_total': x[14]
                    })
                    equipe.append(myDict)
                completa.append(equipe)


            if check != False:
                print('ACHOU')
                equipe = []
                for x in check:
                    Channel = x[15]
                    if Channel == None:
                        Channel = 'off'
                    # print(Channel)
                    myDict = ({
                        'idrank': str(x[0]),
                        'idpartida_online': x[1],
                        'idplayer': x[2],
                        'idcampeonato': x[8],
                        'idSquad': x[9],
                        'player': x[5],
                        'kills': x[3],
                        'squad': x[6],
                        'score_equipe': x[7],
                        'status': x[4],
                        'rank_partida': x[10],
                        'score_partida': x[11],
                        'jogo': str(x[12]),
                        'jogo_ativo': x[13],
                        'score_total': x[14]
                    })
                    equipe.append(myDict)
                completa.append(equipe)




        return render_template('streaming.html',
                                   listaSquad=listaSquad,
                                   players=completa,
                                   campeonato=campeonato,
                                   idcampeonato=idcampeonato,
                                   grupo=grupo,
                                   channel1=Channel
                                   )
            #
            #
            #
            # print(equipe)









            # print(jogo_ativo)

        # print(listaSquad)
        # listaCompleta = []

        # checkRank2 = SelectSql('rank', 'idSquad', listaSquad[1])
        # checkRank = SelectSqlMulti('rank', 'idSquad', idSquad, 'idcampeonato', idcampeonato)
        # print(checkRank1)
        # if checkRank1 or checkRank2 == False:
        #     print('ok')
        #     # make_ranking(listaSquad,fasedeGrupos=fasedeGrupos,idcampeonato=idcampeonato)
        # for idSquad in listaSquad:
        #     checkRank = SelectSqlMulti('rank', 'idSquad', idSquad, 'idcampeonato', idcampeonato)
        #     if checkRank == False:
        #         print('nao tem ranking')
        #         # checkRank = make_ranking(idSquad, fasedeGrupos, idcampeonato)
        #     else:
        #         pass
        #     # print(idSquad)
        #     #     print('tem ranking')
        #     equipe = []
        #
        #     for i in checkRank:
        #         if i[13] != 'no':
        #                 # listaCompleta.append(i)
        #             jogo_ativo = i[13]
        #             # print(jogo_ativo)
        #             # print(i)
        #     selectRankingAtivo = SelectSqlMulti('rank', 'idSquad', idSquad, 'ativo', jogo_ativo)
        #
        #     # print(selectRankingAtivo)
        #     if checkRank == False:
        #         make_ranking()
        #         nomeSquad = SelectSql('squads', 'idsquads', idSquad)[0][1]
        #         print(nomeSquad)
        #
        #         # createRank(SelectSql('players', 'squad', nomeSquad), SelectSql('partidas_online', 'idsquad', idSquad),idSquad)
        #
            # jogo_ativo = SelectSql('partidas_online', 'idsquad', idSquad)[0][26]
            # streamStatusChannel = SelectSql('partidas_online', 'idsquad', idSquad)[0][27]
            # selectRankingAtivo = SelectSqlMulti('rank', 'idSquad', idSquad, 'ativo', jogo_ativo)
        #         # print(selectRankingAtivo)
        #     for x in selectRankingAtivo:
        #         streamStatusChannel = x[15]
        #         myDict = ({
        #                         'idrank': str(x[0]),
        #                         'idpartida_online': x[1],
        #                         'idplayer': x[2],
        #                         'idcampeonato': x[8],
        #                         'idSquad': x[9],
        #                         'player': x[5],
        #                         'kills': x[3],
        #                         'squad': x[6],
        #                         'score_equipe': x[7],
        #                         'status': x[4],
        #                         'rank_partida': x[10],
        #                         'score_partida': x[11],
        #                         'jogo': str(x[12]),
        #                         'jogo_ativo': x[13],
        #                         'score_total': x[14]
        #                     })
        #         equipe.append(myDict)
        #                 # print(equipe)
        #     listaCompleta.append(equipe)
        # # print(listaCompleta)
        #
        # # print(streamStatusChannel)


def rules(colocacaoPartida,idcampeonato):
    fromRules = SelectSql('regras', 'idregras',
                          SelectSql('campeonatos_ativos', 'idcampeonatos_ativos', idcampeonato)[0][8])
    for key in fromRules:
        multiplicadorKill = int(key[6])
        primeiroLugar = int(key[1])
        segundoLugar = int(key[2])
        terceirooLugar = int(key[3])
        quarto_Decimo = int(key[4])
        decimoPrimeiro_decimoQuinto = int(key[5])
    if colocacaoPartida == 0 or colocacaoPartida > 15:
        scoreRank = 0
    if colocacaoPartida == 1:
        scoreRank = primeiroLugar
    if colocacaoPartida == 2:
        scoreRank = segundoLugar
    if colocacaoPartida == 3:
        scoreRank = terceirooLugar
    if 4 <= colocacaoPartida <= 10:
        scoreRank = quarto_Decimo
    if 11 <= colocacaoPartida <= 15:
        scoreRank = decimoPrimeiro_decimoQuinto
    # print(scoreRank)
    return scoreRank, multiplicadorKill
def CountKillsSquad(idSquad):
    select = SelectSql('rank','idSquad',idSquad)
    totalkills = 0
    for k in select:
        totalkills = totalkills + int(k[3])

    return totalkills
def CountScore(idrank, multiplicadorKills, ScoreRanking):
    select = SelectSql('rank','idrank',idrank)
    countKills = 0
    for k in select:
        countScore = TotalCount(k[2])
        countKills = countKills + int(k[3])
    Score_individual = (countKills * multiplicadorKills) + ScoreRanking
    # UpdateQuerySql({
        # 'score_partida': Score_individual,
    # }, 'rank', 'idrank', idrank)

    return Score_individual, countScore
def CountScoreEquipePartida(colocacaoPartida,idsquad, idcampeonato,idrank,jogo_ativo):
    role  = rules(colocacaoPartida,idcampeonato)
    multiplicadorKill = role[1]
    scoreRank = role[0]
    scoreEquipe = (int(CountKillsSquad(idsquad)) * int(multiplicadorKill)) + int(scoreRank)

    print(f'colocacao : {colocacaoPartida}')
    print(f'idsquad : {idsquad}')
    print(f'idcampeonato : {idcampeonato}')
    print(f'idrank : {idrank}')
    print(f'jogo_ativo : {jogo_ativo}')


    selectAll = SelectSqlMulti('rank','idsquad',idsquad,'ativo',jogo_ativo)
    for i in selectAll:

        UpdateQuerySql({
            'score_equipe': scoreEquipe,
            'rank_partida': colocacaoPartida
        }, 'rank', 'idrank', i[0])
    UpdateQuerySql({jogo_ativo: scoreEquipe }, 'partidas_online', 'idsquad', idsquad)
    scores = CountScore(idrank, multiplicadorKill, scoreRank)
    UpdateQuerySql({
        'score': scores[1]
    }, 'bracket', 'squad', idsquad)
    UpdateQuerySql({
        'score_total': scores[1]
    }, 'rank', 'idSquad', idsquad)



    return scoreEquipe, scores[1]
def TotalCount(idPlayer):
    select = SelectSql('rank', 'idplayer', idPlayer)
    total = 0
    for n in select:
        print(n[7])
        total = total + int(n[7])
    return total


@app.route('/streaming/placar/channel1', methods=['GET', 'POST'])
def channel1():
    bracket = SelectSql('bracket', 'stream', 'on')
    return render_template('channel1.html', bracket=bracket)



def getRank(value):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM bracket WHERE stream={value} ORDER BY score DESC """)
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))






##### EMAIL FORGOT / TOKEN  #####


# @app.route('/token/<string:email>', methods=['GET', 'POST'])
# def token(email):
#     token = generateOTP()
#     print(token)
#     UpdateQuerySql({'OTP': token}, 'usuarios', 'EMAIL', email)
#     user = SelectSql('usuarios', 'LOGIN', email)
#     for item in user:
#         # id = item[0]
#         nome_completo = f'{item[3]} {item[4]}'
#     if __name__ == '__main__':
#         with app.app_context():
#             msg = Message(subject='Pedido de Nova Senha',
#                           sender=app.config.get('MAIL_USERNAME'),
#                           recipients=[email],
#                           html=render_template('email_reply.html', token=token, user=nome_completo))
#             mail.send(msg)
#             flash('Verifique o seu e-mail, um novo código foi enviado.', 'login')
#             return render_template('insert_code.html', email=email)
#
# @app.route('/send_email_password', methods=['GET', 'POST'])
# def index_mail():
#     email = request.form['email']
#     token = generateOTP()
#     print(token)
#     user = SelectSql('usuarios','LOGIN',email)
#     if user == False:
#         flash(f'Esse email não está cadastrado!!! Verifique se está correto o email {email}','erro')
#         return redirect(url_for('email_forgot'))
#     else:
#         UpdateQuerySql({'OTP': token}, 'usuarios', 'EMAIL',email)
#         for item in user:
#             nome_completo = f'{item[3]} {item[4]}'
#         if __name__ == '__main__':
#             with app.app_context():
#                 msg = Message(subject='Código para alteração de password Guia Figueira da Foz',
#                             sender=app.config.get('MAIL_USERNAME'),
#                               recipients=[email],
#                               html=render_template('email_reply.html',token=token, user=nome_completo))
#                 mail.send(msg)
#                 return render_template('insert_code.html', email=email)
#
#
# @app.route('/confima_code', methods=['GET', 'POST'])
# def confirma_code():
#     if request.method == "POST":
#         email = request.form['email']
#         code = request.form['code']
#         new_password = sha256_crypt.encrypt((str(request.form['new_password'])))
#         data = SelectSql('usuarios', 'LOGIN',email)
#         for item in data:
#             OTP = item[12]
#             if str(OTP) == str(code):
#                 UpdateQuerySql({'PASSWORD':new_password}, 'usuarios','EMAIL',email)
#                 flash('Senha Atualizada com Sucesso!', 'success')
#                 return redirect(url_for('LoginClientes'))
#             else:
#                 flash('Código não está correto, tente novamente', 'erro')
#                 return render_template('insert_code.html',email=email)
#
#
#
#         ####### REGISTER USUARIOS ##########
#
#


# @app.route('/register', methods=['POST'])
# def register():
#     error = ''
#     try:
#         if request.method == 'POST':
#             email = request.form['email']
#             nome = request.form['nome']
#             apelido = request.form['apelido']
#             check_user = check_user_Login(email)
#             print(check_user)
#             if check_user == False:
#                 myDict = {}
#                 password = sha256_crypt.encrypt((str(request.form['password'])))
#                 DATA = str(datetime.now().strftime("%b %d,%Y"))
#                 myDict.update({'DATA_INSCRICAO': DATA})
#                 myDict.update({
#                     'LOGIN': email,
#                     'PASSWORD' : password,
#                     'NOME' : nome,
#                     'APELIDO' : apelido,
#                     'NOTIFICACOES' : 0 ,
#                     'PONTOS' : 0
#                 })
#                 InsertSql(myDict,'usuarios')
#                 user = SelectSql('usuarios' , 'LOGIN',email)
#                 for item in user:
#                     id = item[0]
#                 session['logged_in'] = True
#                 session['email'] = email
#                 session['Nome'] = f'{nome} {apelido}'
#                 session['ID_User'] = id
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash('Usuário já cadastrado, escolha um email diferente', 'login')
#                 return redirect(url_for('LoginClientes'))
#
#         return render_template("area-Login.html", error=error)
#     except Exception as e:
#         flash(e)
#
#
#
#
#
# ############## CONFIGURACOES DE USUARIOS #################
#
# @app.route('/edit_profile_photo', methods=['GET', 'POST'])
# def edit_profile_photo():
#     if request.method == "POST":
#         myDict = {}
#         if request.files['file']:
#             f = request.files['file']
#             print(f)
#             if f and allowed_file(f.filename):
#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar'+filename))
#                 myDict.update({'FOTO':'avatar'+filename})
#         UpdateQuerySql(myDict, 'usuarios','EMAIL',session['email'])
#         return redirect(url_for('dashboard'))
#
#
# @app.route('/usuarios/', methods=['GET', 'POST'])
# def usuarios():
#     c, conn = connection()
#     c.execute("SELECT  * FROM usuarios")
#     data = c.fetchall()
#     c.close()
#     return render_template('lista-Usuarios.html', usuarios=data )
#
#
#
# @app.route('/edit_usuario', methods=['GET', 'POST'])
# def edit_usuario():
#     if request.method == "POST":
#         data = []
#         myDict = {}
#         for post in request.form:
#             data.append(post)
#         for form in data:
#             request_form = request.form[form]
#             print(request_form)
#             myDict.update({form: request_form})
#             if request_form == '':
#                 request_form = "blank"
#                 myDict.update({form: request_form})
#             else:
#                 myDict.update({form: request_form})
#         print(myDict)
#         UpdateQuerySql(myDict, 'usuarios', 'EMAIL', session['email'])
#     return redirect(url_for('dashboard'))
#
#
# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record Has Been Deleted Successfully")
#     c, conn = connection()
#     c.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_data,))
#     return redirect(url_for('usuarios'))
#
#
# if __name__ == "__main__":
#     app.run(debug=True,port=5002)




# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#
#
# @socketio.on('connect')
# def test_connect():
#     print('connect')
#     socketio.emit('my response', {'data': 'Connected'})


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

@socketio.on('refresh_channel')
def refresh_channel(json):
    setChannelAPI(json)

def setChannelAPI(data):
    # print(data)
    Lista_idSquads = data['Lista_idSquads']
    streamStatus = data['stream']
    idCampeonato = data['campeonato']
    selectStream = SelectSqlMulti('partidas_online', 'stream', 'on','idcampeonatos_ativos',int(idCampeonato))


    print(selectStream)



    # def on():
    #     print('on')
    #     socketio.emit('reload_statusChannel1', {'status_channel1': 'on'})
    #     for idsquad in Lista_idSquads:
    #         selectPartida = SelectSqlMulti('partidas_online', 'idsquad', idsquad, 'idcampeonatos_ativos',
    #                                        idCampeonato)
    #         for i in selectPartida:
    #             print(i)
    #             # UpdateQuerySql({'stream': 'on'}, 'partidas_online', 'idpartidas_online', i[0])
    #
    #             # UpdateQuerySql({'stream': 'off'}, 'partidas_online', 'idsquad', oldid)
    #             # UpdateQuerySql({'stream': 'off'}, 'bracket', 'squad', oldid)
    #             #         UpdateQuerySql({'stream': 'off'}, 'rank', 'idSquad', oldid)


    # def off():
    #     print('off')
    #     socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
    #     for idsquad in Lista_idSquads:
    #         selectPartida = SelectSqlMulti('partidas_online', 'idsquad', idsquad, 'idcampeonatos_ativos',
    #                                        idCampeonato)
    #         for i in selectPartida:
    #             print(i)
    #             # #     for idsquad in Lista_idSquads[:-1]:
    #             # UpdateQuerySql({'stream': 'off'}, 'partidas_online', 'idpartidas_online', i[0])
    #
    if selectStream == False:
        print('nao existe Stream ON')
        # print(streamStatus)
        if streamStatus == 'on':
            print('on')
            # socketio.emit('reload_statusChannel1', {'status_channel1': 'on'})
            for team in Lista_idSquads:
                # selecTEAM = SelectSqlMulti('partidas_online', 'idsquad', team, 'idcampeonatos_ativos', idCampeonato)
                # for item in selecTEAM:
                #     idPartida = item[0]
                UpdateQuerySqlMulti({'stream': 'on'}, 'partidas_online', 'idsquad', team,'idcampeonatos_ativos',idCampeonato)
                    # UpdateQuerySql({'stream': 'on'}, 'bracket', 'idpartidas_online', idPartida)
                    # UpdateQuerySql({'stream': 'on'}, 'rank', 'idpartidas_online', idPartida)

        else:
            print('off')
            for team in Lista_idSquads:
                # socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
                UpdateQuerySqlMulti({'stream': 'off'}, 'partidas_online', 'idsquad', team, 'idcampeonatos_ativos',
                                    idCampeonato)
                # selecTEAM = SelectSqlMulti('partidas_online', 'idsquad', team, 'idcampeonatos_ativos', idCampeonato)
                # for item in selecTEAM:
                #     idPartida = item[0]
                #     UpdateQuerySql({'stream': 'off'},'partidas_online', 'idpartidas_online', idPartida)




    else:
        print('ja exitem partidas online')
        for old in selectStream:
            if streamStatus == 'on':
                UpdateQuerySqlMulti({'stream': 'off'}, 'partidas_online', 'idpartidas_online', old[0], 'idcampeonatos_ativos',
                                        idCampeonato)
                for team in Lista_idSquads:
                        # socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
                        UpdateQuerySqlMulti({'stream': 'on'}, 'partidas_online', 'idsquad', team,
                                            'idcampeonatos_ativos',
                                            idCampeonato)



        if streamStatus == 'off':

            # for team in Lista_idSquads:
            # socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
            for team in Lista_idSquads:
                # socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
                UpdateQuerySqlMulti({'stream': 'off'}, 'partidas_online', 'idsquad', team, 'idcampeonatos_ativos',
                                    idCampeonato)
                # selecTEAM = SelectSqlMulti('partida

    socketio.emit('reload_statusChannel1', {'status_channel1': streamStatus})






    #             off()
    #             # print(selectStream)
    #             UpdateQuerySql({'stream': 'off'}, 'partidas_online', 'idpartidas_online', old[0])
    #             socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
    #














            # oldid = old[3]
            #
            # print(oldid)
            # print(Lista_idSquads)
            # if oldid in Lista_idSquads:
            #     print('Esta na lista')
            #
            # #     if streamStatus == 'on':
            # #         print(oldid[27])
            # #
            # #     if streamStatus == 'off':
            # #         print(oldid[27])
            #
            # else:
            #     print('nao esta na lista')
        #         UpdateQuerySql({'stream':'off'},'partidas_online','idsquad',oldid)
        #         UpdateQuerySql({'stream': 'off'}, 'bracket', 'squad', oldid)
        #         UpdateQuerySql({'stream': 'off'}, 'rank', 'idSquad', oldid)



        # if streamStatus == 'off':
        #     print('off')
        #     print('off')
        #     socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
        #     for idsquad in Lista_idSquads[:-1]:
        #         UpdateQuerySql({'stream':'off'},'partidas_online','idsquad',idsquad)
        #         UpdateQuerySql({'stream': 'off'}, 'bracket', 'squad', idsquad)
        #         UpdateQuerySql({'stream': 'off'}, 'rank', 'squad', idsquad)
    # else:
    #     for all in selectStream:
    #         partidasToOff = all[0]
    #         UpdateQuerySql({'stream': 'off'}, 'partidas_online', 'idpartidas_online', partidasToOff)
    #     if streamStatus == 'on':
    #         socketio.emit('reload_statusChannel1', {'status_channel1': 'on'})
    #         for idsquad in Lista_idSquads[:-1]:
    #             UpdateQuerySql({'stream':'on'},'partidas_online','idsquad',idsquad)
    #             UpdateQuerySql({'stream': 'on'}, 'bracket', 'squad', idsquad)
    #             UpdateQuerySql({'stream': 'on'}, 'rank', 'squad', idsquad)
    #     if streamStatus == 'off':
    #         socketio.emit('reload_statusChannel1', {'status_channel1': 'off'})
    #         for idsquad in Lista_idSquads[:-1]:
    #             UpdateQuerySql({'stream':'off'},'partidas_online','idsquad',idsquad)
    #             UpdateQuerySql({'stream': 'off'}, 'bracket', 'squad', idsquad)
    #             UpdateQuerySql({'stream': 'off'}, 'rank', 'squad', idsquad)


@socketio.on('refresh_kills')
def refresh_kills(json):
    setKillsAPI(json)
def setKillsAPI(data):
    UpdateQuerySql({'kills':data['kills']},'rank','idrank', data['idrank'])
    slipt = str(data['jogo_ativo']).split('/')
    jogo_ativo = slipt[0]
    return_data = CountScoreEquipePartida(data['colocacao_partida'],data['idsquad'],data['idcampeonato'],data['idrank'],jogo_ativo)
    data_json = [
        data['idsquad'],
        return_data[0],
         return_data[1]
    ]
    socketio.emit('score_stream',data_json,broadcast=True)

@socketio.on('refresh_rank')
def refresh_kills(json):
    setRankAPI(json)
def setRankAPI(data):
    print(data)

    return_data= CountScoreEquipePartida(int(data['rank_partida']),data['idsquad'],data['idcampeonato'],data['idrank'],data['jogo'])
    data_json = [
        data['idsquad'],
        return_data[0],
        return_data[1]
    ]
    socketio.emit('score_stream', data_json)

@socketio.on('refresh_game')
def refresh_kills(json):
    setGameAPI(json)
def setGameAPI(data):

    stage = data['jogo']
    print(stage)
    if stage == 'R1J1':
        next = 'R1J2'
    if stage == 'R1J2':
        next = 'R1J3'
    if stage == 'R1J3':
        next = 'R1J1'
    if stage == 'R2J1':
        next = 'R2J2'
    if stage == 'R2J2':
        next = 'R2J1'
    UpdateQuerySql({'jogo_ativo': next}, 'partidas_online', 'idsquad', data['idsquad'])
    UpdateQuerySql({'jogo_ativo': next}, 'bracket', 'squad', data['idsquad'])
    UpdateQuerySql({'ativo': 'no'}, 'rank', 'idSquad', data['idsquad'])
    nextPoint = SelectSqlMulti('rank', 'idSquad', data['idsquad'], 'jogo', next)
    for all in nextPoint:
        UpdateQuerySql({'ativo': next}, 'rank', 'idrank',all[0])
    socketio.emit('change round', 'next')

@socketio.on('dashboard items')
def dash_items():
    print('atualizar Dashboard...')
    data = []
    data.append(SelectSqlAll('modalidades'))
    data.append(SelectSqlAll('regras'))
    data.append(SelectSqlAll('campeonatos_ativos'))
    data.append(SelectSqlAll('squads'))
    socketio.emit('dashboard response', data)

    # data.append(campeonatos)
    #
    # lista_partidas =[]
    #
    # for item_campeonato in campeonatos:
    #     grupos = []
    #     data_partidas = [item_campeonato[0]]
    #     partidas = SelectSql('partidas_online','idcampeonatos_ativos',item_campeonato[0])
    #     for itme in partidas:
    #         grupo = itme[22]
    #         if grupo not in grupos:
    #             grupos.append(grupo)
    #             data_partidas.append(grupo)
    #     for x in grupos:
    #         partidasGrupo = SelectSqlMulti('partidas_online','idcampeonatos_ativos',item_campeonato[0],'grupo',x)
    #         data_partidas.append(partidasGrupo)
    #
    #     lista_partidas.append(data_partidas)
    # data.append(lista_partidas)







    # patidas_todas = SelectSqlAll('partidas_online')




    #
    # campeonatos = []
    # listaFinal = []
    #
    # for item in patidas_todas:
    #     idCampeonato = item[2]
    #     if idCampeonato not in campeonatos:
    #         campeonatos.append(idCampeonato)
    # for x in campeonatos:
    #     myDict = {'idCampeonato': x}
    #     grupos = []
    #     for item in patidas_todas:
    #         if x == item[2]:
    #             if item[22] not in grupos:
    #                 grupos.append(item[22])
    #
    #     # print(grupos)
    #     for check in grupos:
    #         partidas_grupos = []
    #         for c in patidas_todas:
    #
    #             if c[22] == check and c[2] == x:
    #                 partidas_grupos.append({c})
    #         myDict.update({
    #         check:partidas_grupos,
    #         })
    #
    #     listaFinal.append(myDict)
    # print(listaFinal)
    # # data.append(listaFinal)


    # print(listaFinal)

        # print(x)
        # for jar in
        # grupos_campeonatos = {'idCampeonato': idCampeonato}


            # for t in grupos_campeonatos:
            #     if t == item[22]:
            #         partidas_grupos.append(
            #             item
            #         )
            #


            # print(grupos_campeonatos)



    #         if x == idCampeonato:
    #             if grupo not in partidas_grupos:
    #                 partidas_grupos.append({
    #                     item
    #                 })
    # print(partidas_grupos)




            #     myDict = ({
            #         'idCampeonato':idCampeonato,
            #         'grupo':grupo,
            #         'partidas_online': item
            #
            #     })
            # print(myDict)

        # if grupo not in grupos:
        #     grupos.append(grupo)
    # partidas_grupos = SelectSql('partidas_online')
    # socketio.emit('dashboard response', listaFinal)

@socketio.on('bracket setup')
def dash_items():
    data = []
    data.append(SelectSqlAll('squads'))
    # data.append(SelectSqlAll('regras'))

    socketio.emit('bracket setup response', data)

@socketio.on('submit bracket')
def bracket_mount(data):

    # print(data)
    idcampeonato = data[0]
    fasedeGrupos= data[1]
    regras = data[2]
    nomeCampeonato = data[3]
    listaSquad= data[4:]
    # limiter = len(listaSquad)
    random.shuffle(listaSquad)
    if fasedeGrupos == 1:
        fase = 'R2'
    if fasedeGrupos != 1:
        fase = 'R1'


    teste = list(chunker_list(listaSquad, int(fasedeGrupos)))
    listData = [{
            'listaSquad': listaSquad,
            'fasedeGrupos':fasedeGrupos,
            'idcampeonato':idcampeonato
        }]

    socketio.emit('salved', listData)
    grupoList = []
    for c in range(len(list(teste))):
        grupo = f'grupo {c + 1}'
        grupoList.append(grupo)
        for myDict in teste[c]:
            myDict.update({
                            'braket': int(fasedeGrupos),
                            'grupo': grupo,
                            'idcampeonatos_ativos': idcampeonato,
                            'nomeCampeonato': nomeCampeonato,
                            'score':0,
                            'regras':regras,
                            'status': fasedeGrupos,
                        })
            InsertSql(myDict, 'bracket')
    for g in grupoList:
        mySelect =  SelectSqlMulti('bracket','idcampeonatos_ativos',idcampeonato,'grupo',g)
        posicaoInicial = 0
        for m in mySelect:
            posicaoInicial = int(posicaoInicial) + 1
            UpdateQuerySql({'posicao':f'{fase}_{g}_{posicaoInicial}'},'bracket','idbracket',m[0])

    make_partidas(idcampeonato, regras,fasedeGrupos, nomeCampeonato)



#
#
# @app.route('/submitrank',methods=['GET','POST'])
# def rank_items(data):
#     # print(data)
#     grupo = data[0]
#     jogo_ativo = data[1]
#     idCampeonato = data[2]
#     listaSquads = []
#     faseGrupos = data[3]
#
#
#
#     squads =  SelectSqlMulti('partidas_online','idcampeonatos_ativos', idCampeonato, 'grupo', grupo)
#     for team in squads:
#         # print(team)
#         nomeCampeonato = team[23]
#         listaSquads.append(team[3])
#
#     # listaSquads = [str(data['squad1']),str(data['squad2'])]
#     # faseGrupos = data['fasegrupos']
#     # idCampeonato = data['idCampeonato']
#     # jogo_ativo = data['jogo_ativo']
#     #
#     try:
#         # print(listaSquads)
#         check = SelectSqlMulti('rank','idSquad',listaSquads[0],'ativo',jogo_ativo)
#         # print(check)
#
#         if check != False:
#             print('Rank da Partida ja Existe')
#
#         if check == False:
#             print('NAO EXITE')
#             make_ranking(listaSquads, faseGrupos, idCampeonato)
#     except:
#         print('Algo deu errado')
#     texto = ''
#     for k in listaSquads:
#         texto = texto + k + 'p'
#     newData = {
#         'nomeCampeonato':nomeCampeonato,
#         'grupo': grupo,
#         'idSquads': texto,
#         'fasegrupos': faseGrupos,
#         'idCampeonato':idCampeonato
#     }
#     return make_response(jsonify(newData), 200)
#     # socketio.emit('bracket rank response', newData)


def make_ranking(idsquad,fasedeGrupos,idcampeonato):
    # print(listaSquad)
    # for idsquad in listaSquad:
    #     # print(squad)
    #     # print(idsquad)
    nome = SelectSql('squads','idsquads',idsquad)
    # print(nome)
    for i in nome:
        tagName = i[1]
        print(tagName)
        #####################################################################INSERIR PELO ID SQUAD##### PRECISA REINICIAR OS PLAYER #####
        players = SelectSql('players', 'squad', tagName)
        print(players)


        # print(players)
    if int(fasedeGrupos) != 1:
        jogos = ['R1J1', 'R1J2', 'R1J3']
        for jogo in jogos:
            if jogo == 'R1J1':
                jogo_ativo = jogo
            else:
                jogo_ativo = 'no'
            for i in players:
                myDict = fillDictRAnk(
                        idpartida_online=i[0],
                        idplayer=i[0],
                        idcampeonato=idcampeonato,
                        idSquad=idsquad,
                        player=i[2],
                        squad=i[1],
                        status=fasedeGrupos,
                        jogo=jogo,
                        jogo_ativo=jogo_ativo
                    )
                    # print(myDict)
                InsertSql(myDict, 'rank')
    if int(fasedeGrupos) == 1:
        jogos = ['R2J1', 'R2J2']
        for jogo in jogos:
            if jogo == 'R2J1':
                jogo_ativo = jogo
            else:
                jogo_ativo = 'no'
            for i in players:
                myDict = fillDictRAnk(
                        idpartida_online=i[0],
                        idplayer=i[0],
                        idcampeonato=idcampeonato,
                        idSquad=idsquad,
                        player=i[2],
                        squad=i[1],
                        status=fasedeGrupos,
                        jogo=jogo,
                        jogo_ativo=jogo_ativo
                    )
                    # print(myDict)
                InsertSql(myDict, 'rank')




#
# def createRank(players,partidas,idSquad):
#     faseBracket = partidas[0][9]
#     campeonato = partidas[0][2]
#
#     if faseBracket == 'GRUPOS':
#         jogos = ['R1J1', 'R1J2', 'R1J3']
#         for jogo in jogos:
#             if jogo == 'R1J1':
#                 jogo_ativo = jogo
#             else:
#                 jogo_ativo = 'no'
#             for i in players:
#                 myDict = fillDictRAnk(
#                     idpartida_online=i[0],
#                     idplayer=i[0],
#                     idcampeonato= campeonato,
#                     idSquad=idSquad,
#                     player=i[2],
#                     squad=i[1],
#                     status=faseBracket,
#                     jogo=jogo,
#                     jogo_ativo= jogo_ativo
#                 )
#                 print(myDict)
#                 InsertSql(myDict, 'rank')
#     if faseBracket == 'OITAVAS':
#         jogos = ['R2J1', 'R2J2']
#         for jogo in jogos:
#             if jogo == 'R2J1':
#                 jogo_ativo = jogo
#             else:
#                 jogo_ativo = 'no'
#             for i in players:
#                 myDict = fillDictRAnk(
#                     idpartida_online=i[0],
#                     idplayer=i[0],
#                     idcampeonato=campeonato,
#                     idSquad=idSquad,
#                     player=i[2],
#                     squad=i[1],
#                     status=faseBracket,
#                     jogo=jogo,
#                     jogo_ativo=jogo_ativo
#                 )
#                 InsertSql(myDict, 'rank')
#                 UpdateQuerySql({'jogo_ativo'},'partidas_online', 'idsquad',idSquad)
#                 # InsertSql({'jogo_ativo'},'partidas_online',)
#



# @socketio.on('get partidas')
# def data_partidas(idCampeonato):
#     # print(idCampeonato)
#     partidas_online = SelectSql('partidas_online', 'idcampeonatos_ativos', int(idCampeonato))
#     data = []
#     for item in partidas_online:
#         # totalPosition = item[28].split('_')
#         # print(totalPosition)
#         # round = totalPosition[0]
#         # bracket = item[4]
#
#         data.append(item)
#
#
#     socketio.emit('braket mount', data,broadcast=False)


def make_partidas(idCampeonato, regras, braket,nomeCampeonato):
    openBracket = SelectSql('bracket', 'idcampeonatos_ativos', int(idCampeonato))
    for itens in openBracket:
        idbracket = itens[0]
        refGroup = itens[2]
        idSquad = itens[3]
        nameSquad = itens[5]
        status = itens[6]
        posicao = itens[12]
        roundGroupsDict = ({
                    'idbracket': idbracket,
                    'idcampeonatos_ativos': idCampeonato,
                    'nomeCampeonato': nomeCampeonato,
                    'idsquad': idSquad,
                    'nome': nameSquad,
                    'status': status,
                    'grupo': refGroup,
                    'regras': regras,
                    'braket': braket,
                    'posicao':posicao
                })
            #
        # print(status)
        if int(status) == 1:
            roundGroupsDict.update({
                         'jogo_ativo':'R2J1',
                         'R2J1':0,
                         'R2J2': 0
                    })
             # UpdateQuerySql({'jogo_ativo':'R2J1'},'bracket','squad',idSquad)

        if int(status) != 1:
            roundGroupsDict.update({
                         'jogo_ativo':'R1J1',
                            'R1J1': 0,
                'R1J2': 0,
                'R1J3': 0
                    })
            #         UpdateQuerySql({'jogo_ativo': 'R1J1'}, 'bracket', 'squad', idSquad)
            #
        # print(roundGroupsDict)
        InsertSql(roundGroupsDict, 'partidas_online')

if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app, port=5002, debug=True)
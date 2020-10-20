import pymysql
import warnings
import random
import math

def connection():
    conn = pymysql.connect(host="us-cdbr-east-02.cleardb.com",
                           user='bd6c26b0e448e5',
                           passwd='ff99600e',
                           db = 'heroku_fc3f18d75e6928c')
    c = conn.cursor()

    return c,conn

# arcadeadminarena

def InsertSql(myDict,table):
    try:
        print('INSERINDO ....')
        c, conn = connection()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in myDict.keys())
            values = ', '.join("'" + str(x) + "'" for x in myDict.values())
            c.execute('SET @@auto_increment_increment=1;')
            conn.commit()
            sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
            c.execute(sql)
            conn.commit()
        print(f'INSERIDO :na TABELA {table} |||  { myDict} {{status :: OK}} ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def SelectSql(table, coluna,value):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna}= '{value}'""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def SelectSqlShort(table, coluna,value,ordenagem):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna}= '{value}' ORDER BY {ordenagem} DESC """)
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))

def SelectSqlMulti(table, coluna1,value1,coluna2,value2):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna1}= '{value1}' AND {coluna2} = '{value2}' """)
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))

def SelectSqlMultiORDER(table, coluna1,value1,coluna2,value2,ordenagem):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna1}= '{value1}' AND {coluna2} = '{value2}' ORDER BY {ordenagem} DESC """)
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def SelectSqlMulti3(table, coluna1,value1,coluna2,value2,coluna3,value3):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table} WHERE {coluna1}= '{value1}' AND {coluna2} = '{value2}' AND {coluna3} = '{value3}' """)
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
def SelectSqlAll(table):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM {table}""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
def UpdateQuerySql(mydict,table,item,modifica):
    print(' ATUALIZANDO DADOS .... ')
    try:
        c, conn = connection()
        for k in mydict:
            coluna = (k)
            value = (mydict[k])
            sql = (f"""UPDATE `{table}` SET `{coluna}` = '{value}' WHERE (`{item}` = '{modifica}');""")
            c.execute(sql)
            conn.commit()
        print(f'--->>> ATUALIZAÇÃO da TABELA :{table}  == > DATA {mydict}{{status :: OK}} .... ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))

def UpdateQuerySqlMulti(mydict,table,coluna1,value1,coluna2,value2):
    print(' ATUALIZANDO DADOS .... ')
    try:
        c, conn = connection()
        for k in mydict:
            coluna = (k)
            value = (mydict[k])
            sql = (f"""UPDATE `{table}` SET `{coluna}` = '{value}' WHERE (`{coluna1}` = '{value1}' AND `{coluna2}` = '{value2}');""")
            c.execute(sql)
            conn.commit()
            print(f'--->>> ATUALIZAÇÃO da TABELA :{table}  == > DATA {mydict}{{status :: OK}} .... ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))

def UpdateQuerySqlMulti3(mydict,table,coluna1,value1,coluna2,value2,coluna3,value3):
    print(' ATUALIZANDO DADOS .... ')
    try:
        c, conn = connection()
        for k in mydict:
            coluna = (k)
            value = (mydict[k])
            sql = (f"""UPDATE `{table}` SET `{coluna}` = '{value}' WHERE (`{coluna1}` = '{value1}' AND `{coluna2}` = '{value2}' AND `{coluna3}` = '{value3}');""")
            c.execute(sql)
            conn.commit()
            print(f'--->>> ATUALIZAÇÃO da TABELA :{table}  == > DATA {mydict}{{status :: OK}} .... ')
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def check_user_Login(login):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM usuarios WHERE LOGIN={login}""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def check_user_ID(id):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM usuarios WHERE id_usuario={id}""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def generateOTP():
    # Declare a string variable
    # which stores all string
    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    return OTP



# def criar_table_ask ():
#     try:
#         c, conn = connection()
#         print()
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore')
#             c.execute(f"DROP TABLE IF EXISTS ask ")
#             c.execute(f""" CREATE TABLE ask (
#                         `idask` INT NOT NULL AUTO_INCREMENT ,
#                         `iduser` INT ,
# open_domingo VARCHAR(600) DEFAULT '' not null,
# open_Segunda VARCHAR(600) DEFAULT '' not null,
# open_Terça VARCHAR(600) DEFAULT '' not null,
# open_Quarta VARCHAR(600) DEFAULT '' not null,
# open_Quinta VARCHAR(600) DEFAULT '' not null,
# open_Sexta VARCHAR(600) DEFAULT '' not null,
# open_Sabado VARCHAR(600) DEFAULT '' not null,
# close_domingo VARCHAR(600) DEFAULT '' not null,
# close_Segunda VARCHAR(600) DEFAULT '' not null,
# close_Terça VARCHAR(600) DEFAULT '' not null,
# close_Quarta VARCHAR(600) DEFAULT '' not null,
# close_Quinta VARCHAR(600) DEFAULT '' not null,
# close_Sexta VARCHAR(600) DEFAULT '' not null,
# close_Sabado VARCHAR(600) DEFAULT '' not null,
# dinheiro VARCHAR(600) DEFAULT '' not null,
# multibanco VARCHAR(600) DEFAULT '' not null,
# cheque VARCHAR(600) DEFAULT '' not null,
# paypal VARCHAR(600) DEFAULT '' not null,
# boleto VARCHAR(600) DEFAULT '' not null,
# criptomoedas VARCHAR(600) DEFAULT '' not null,
# outros VARCHAR(600) DEFAULT '' not null,
# delivery VARCHAR(600) DEFAULT '' not null,
# desconto VARCHAR(600) DEFAULT '' not null,
#
#                          PRIMARY KEY(`idask`))
#                         ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin""")
#
#             conn.commit()
#         print('TABELA-ASK CRIADA COM SUCESSOO')
#
#     except Exception as e:
#         print(f' ERROR:       {str(e)}')
#         return (str(e))
# def criar_table_fotos ():
#     try:
#         c, conn = connection()
#         print()
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore')
#             c.execute(f"DROP TABLE IF EXISTS FOTOS ")
#             c.execute(f""" CREATE TABLE FOTOS (
#                         `idfoto` INT NOT NULL AUTO_INCREMENT ,
#                         `iduser` INT ,
#                         `foto` VARCHAR(450)  NULL , PRIMARY KEY(`idfoto`))
#                         ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin""")
#
#             conn.commit()
#         print('TABELA-FOTOS CRIADA COM SUCESSOO')

    # except Exception as e:
    #     print(f' ERROR:       {str(e)}')
    #     return (str(e))
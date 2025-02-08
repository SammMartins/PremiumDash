import pandas as pd
import cx_Oracle as cx
from configparser import ConfigParser

with open('/home/ti_premium/dbpath.txt', 'r') as file:
    dbpath = file.read().strip().strip("'")
config = ConfigParser()
files = config.read(dbpath)
if not files:
    raise ValueError(f"Não foi possível ler o arquivo: {dbpath}")

path = '/home/ti_premium/PyDashboards/PremiumDashboards/4Dashboards/'

try:
    username = config.get('oracle_db', 'username')
    password = config.get('oracle_db', 'password')
    host = config.get('oracle_db', 'host')
    port = config.get('oracle_db', 'port')
    sid = config.get('oracle_db', 'sid')
except Exception as e:
    raise ValueError("Erro ao obter as informações de conexão do arquivo de configuração") from e


def df1(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorSupervisor.sql', 'r') as arquivo:
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%b-%Y')
    dataFim = dataFim.strftime('%d-%b-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)
    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df2(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorRCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%m-%Y')
    dataFim = dataFim.strftime('%d-%m-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df3(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorCliente.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%m-%Y')
    dataFim = dataFim.strftime('%d-%m-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def df4(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'vendasPorFornecedor.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    dataIni = dataIni.strftime('%d-%m-%Y')
    dataFim = dataFim.strftime('%d-%m-%Y')

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)

    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def diasUteis():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dias_uteis.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def diasDecorridos():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dias_decorridos.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash322RCA(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash322_RCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def top10CliRCA(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'top_clientes_RCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash322RCA_semDev(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash322_RCA_semDev.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flashDN322RCA(rca, fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dn_RCA322.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca, fornec=fornec)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flashDN1464RCA(rca, fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dn_RCA1464.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca, fornec=fornec)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash1464RCA(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash1464_RCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash1464SUP(sup):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash1464_SUP.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(sup=sup)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flashDN1464SUP(sup, fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dn_SUP1464.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(sup=sup, fornec=fornec)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flashDN322SUP(sup, fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'dn_SUP322.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(sup=sup, fornec=fornec)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def flash322SUP(sup):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'flash322_SUP.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(sup=sup)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def top100Cli(sup, impulso, takehome, acai, supOffOn):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'top_clientes.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(supOffOn=supOffOn, sup=sup, impulso=impulso, takehome=takehome, acai=acai)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def pedErro():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'pedErro.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def metaCalc(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'consulta_meta.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def metaSupCalc(sup):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'consulta_metaSup.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(sup=sup)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def verbas(senha):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'verbas.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(senha=senha)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def trocaRCA(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'trocaRCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def inad(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'inadimplencia.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def devolucao(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'devolucoes.sql', 'r') as arquivo:
        consulta = arquivo.read()


    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)
    try:
        cursor.execute(consulta)


        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def qtdVendaProd(dataIni, dataFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'qtdVendaProd.sql', 'r') as arquivo:
        consulta = arquivo.read()

    consulta = consulta.format(dtIni=dataIni, dtFim=dataFim)
    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def top100Cli_comparativo(sup, impulso, takehome, acai, supOffOn):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'top_clientes_comparativo.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(supOffOn=supOffOn, sup=sup, impulso=impulso, takehome=takehome, acai=acai)
    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def campanhaDanone():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'campanhaDanone.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def campanhaYoPRO():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'campanhaYoPRO.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def pedCont():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'pedCont.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def estoque266():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'estoque266.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def pedidoVsEstoque():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'pedidoVsEstoque.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def prodSemVenda(fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'prodSemVenda.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(fornec=fornec)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def cliente_semVenda(sup, rca, supOnOff, rcaOnOff, fornec):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'cliente_semVenda.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(fornec=fornec, sup=sup, rca=rca, supOnOff=supOnOff, rcaOnOff=rcaOnOff)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def ceps():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'ceps.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def campanhaGulao():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'campanhaGulao2.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def inadimplenciaSup():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'inadimplenciaSup.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def cortesEquipe(fornec, dtIni, dtFim):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'cortesEquipe.sql', 'r') as arquivo: 
        consulta = arquivo.read()
    
    consulta = consulta.format(fornec=fornec , dtIni=dtIni, dtFim=dtFim)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def cortesFornec(dtIni, dtFim, supOnOff, supCod):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'cortesFornec.sql', 'r') as arquivo: 
        consulta = arquivo.read()
    
    consulta = consulta.format(supCod=supCod , dtIni=dtIni, dtFim=dtFim, supOnOff=supOnOff)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def nomesRCA():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'nomesRCA.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def nomesFornec():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'nomesFornec.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def nomesSup():
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'nomesSup.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df

def mix_ideal_dn(rca):
    if None in [username, password, host, port, sid]:
        raise ValueError("Uma ou mais variáveis necessárias não estão estão definidas")

    dsn_tns = cx.makedsn(host, port, sid)
    try:
        con = cx.connect(user=username, password=password, dsn=dsn_tns)
    except cx.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Por favor cheque as credenciais.')
        else:
            print('Erro Banco de Dados: {}'.format(e))
    except cx.OperationalError as e:
        print('Erro na operação: {}'.format(e))

    cursor = con.cursor()

    with open(path + 'mix_ideal_dn.sql', 'r') as arquivo: 
        consulta = arquivo.read()

    consulta = consulta.format(rca=rca)

    try:
        cursor.execute(consulta)

        resultados = cursor.fetchall()

        df = pd.DataFrame.from_dict(resultados)
    finally:
        cursor.close()
        con.close()
    return df
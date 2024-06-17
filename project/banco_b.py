from banco import Banco
from flask import Flask, request, jsonify, session
import requests
import os
import socket

nome_banco = os.getenv('NOME_BANCO', 'banco_B')
app = Flask(nome_banco)
banco = Banco(nome_banco)
app.secret_key = 'secret_key'  # Chave secreta para assinatura da sessão
endereco_ip = socket.gethostbyname(socket.gethostname())


@app.route('/criar-conta-fisica', methods=['POST'])
def criar_contaFisica():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    senha = data.get('senha')
    cpf = data.get('cpf')
    try:
        conta = banco.criar_contaPF(numero, saldo, senha, cpf)
        if conta == False:
            return jsonify({'mensagem': 'Cliente já existe no cadastro do banco'})
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cpf': conta.cpf, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({"mensagem": "Erro ao criar conta"}), 400

@app.route('/criar-conta-PJ', methods=['POST'])
def criar_contaPJ():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    cnpj = data.get('cnpj')
    senha = data.get('senha')
    try:
        conta = banco.criar_contaPJ(numero, saldo, senha, cnpj)
        if conta == False:
            return jsonify({'mensagem': 'Cliente já existe no cadastro do banco'})
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cnpj': conta.cnpj, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({"mensagem": "Erro ao criar conta"}), 400

@app.route('/criar-conta-conjunta', methods=['POST'])
def criar_contaConjunta():
    data = request.json
    numero = data.get('numero')
    saldo = float(data.get('saldo'))
    cpf1 = data.get('cpf1')
    cpf2 = data.get('cpf2')
    senha = data.get('senha')
    try:
        conta = banco.criar_contaConjunta(numero, saldo, senha, cpf1, cpf2)
        if conta == False:
            return jsonify({'mensagem': 'Um dos clientes já possui conta'})
        return jsonify({'numero': conta.numero, 'saldo': conta.saldo, 'cpf1': conta.cpf1, 'cpf2': conta.cpf2, 'mensagem': 'Conta criada com sucesso'}), 200
    except:
        return jsonify({'mensagem': 'Erro ao criar conta'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cpf = data.get('cpf')
    senha = data.get('senha')
    if banco.verificar_credenciais(cpf, senha) == True:
        session['logged_in'] = True
        session['cpf'] = cpf
        return jsonify({"mensagem": "Login realizado com sucesso"}), 200
    return jsonify({"mensagem": "Cpf ou senha inválidos"}), 401

@app.route('/exibir-conta', methods=['GET'])
def exibir_conta():
    cpf = session.get('cpf')  # Obtém o CPF do usuário logado da sessão
    conta = banco.get_conta(cpf)  # Obtém os detalhes da conta do banco
    if conta:
        return jsonify(conta), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/add', methods=['POST'])
def add_saldo():
    data = request.json
    cpf = data.get('cpf')
    valor = float(data.get('valor'))
    conta = banco.get_conta(cpf)  # Obtém os detalhes da conta do banco
    if conta:
        conta = banco.add(cpf, valor)
        return jsonify({"mensagem": "Valor adicionado na conta"}), 200    
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/retirada', methods=['POST'])
def retirada():
    data = request.json
    cpf = data.get('cpf')
    valor = float(data.get('valor'))
    conta = banco.get_conta(cpf)  # Obtém os detalhes da conta do banco
    if conta:
        conta = banco.retirada(cpf, valor)
        return jsonify({"mensagem": "Valor retirado da conta"}), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

@app.route('/transferencia', methods=['POST'])
def transferencia():
    if session.get('logged_in'):
        data = request.json
        cpf_origem = session.get('cpf')
        cpf_destino = data.get('cpf_destino')
        valor = float(data.get('valor'))
        nome_banco_destino = data.get('nome_banco_destino')

        if nome_banco_destino == nome_banco:
            # Transferência dentro do mesmo banco
            try:
                conta_origem = banco.get_conta(cpf_origem)
                conta_destino = banco.get_conta(cpf_destino)
                if conta_origem and conta_destino:
                    banco.retirada(cpf_origem, valor)
                    banco.add(cpf_destino,valor)
                    return jsonify({"mensagem": f"Transferência de R${valor:.2f} realizada com sucesso"}), 200
                else:
                    return jsonify({"mensagem": "Conta de origem ou conta de destino não encontrada"}), 404
            except Exception as e:
                return jsonify({"mensagem": f"Erro ao realizar transferência: {str(e)}"}), 500
        else:
            # Transferência para outro banco
            if nome_banco_destino in bancos:
                try:
                    banco.retirada(cpf_origem, valor)
                    url_banco_destino = bancos[nome_banco_destino]
                    payload = {
                        "cpf": cpf_destino,
                        "valor": valor  
                    }
                    response = requests.post(f"{url_banco_destino}/add", json=payload)
                    if response.status_code == 200:
                        response_data = response.json()
                        if response_data.get('mensagem') == "Valor adicionado na conta":
                            return jsonify({"mensagem": f"Transferência de R${valor:.2f} para {nome_banco_destino} realizada com sucesso"}), 200
                        else:
                            return jsonify({"mensagem": f"Falha ao transferir para {nome_banco_destino}: {response_data.get('mensagem')}"}), 500
                    else:
                        return jsonify({"mensagem": f"Falha ao transferir para {nome_banco_destino}: {response.json().get('mensagem')}"}), response.status_code
                except Exception as e:
                    return jsonify({"mensagem": f"Erro ao transferir para {nome_banco_destino}: {str(e)}"}), 500
            else:
                return jsonify({"mensagem": f"Banco destino {nome_banco_destino} não reconhecido"}), 404


@app.route('/exibir-contas-cpf', methods=['GET'])
def exibir_contas_cpf():
    if session.get('logged_in'):
        cpf = session.get('cpf')  
        contas_encontradas = []

        conta_local = banco.get_conta(cpf)
        if conta_local:
            contas_encontradas.append({'saldo': conta_local['saldo'], 'banco': nome_banco})

        for nome_banco_externo, url_banco in bancos.items():
            try:
                response = requests.get(f"{url_banco}/exibir-conta/{cpf}")
                if response.status_code == 200:
                    conta_info = response.json()
                    if 'saldo' in conta_info:  
                        contas_encontradas.append({'saldo': conta_info['saldo'], 'banco': nome_banco_externo})
            except Exception as e:
                print(f"Erro ao recuperar contas do banco {nome_banco_externo}: {str(e)}")

        return jsonify(contas_encontradas), 200

def criar_conta_inicial():
    numero = '123'
    saldo = 1000.0
    senha = '123'
    cpf = '123'
    conta = banco.criar_contaPF(numero, saldo, senha, cpf)

if __name__ == '__main__':
    criar_conta_inicial()
    port = int(os.getenv('portApi', 4321))
    f"http://{endereco_ip}:{port}"
    app.run(debug=True, host=endereco_ip, port=port)

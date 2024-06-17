from contaFisica import ContaFisica
from contaPJ import ContaPJ
from contaConjunta import ContaConjunta


class Banco:
    def __init__(self, nome):
        self.nome= nome
        self.contas={}
    
    def criar_contaPF(self,numero,saldo,senha,cpf):
        if cpf in self.contas:
            print("Cliente já existe nesse banco")
            return False
        else:
            conta=ContaFisica(numero,saldo,senha,cpf)
            self.contas[conta.cpf] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha, 'cpf': conta.cpf}
            return conta

    
    def criar_contaPJ(self,numero,saldo,senha,cnpj):
        if cnpj in self.contas:
            print("Cliente já existe nesse banco")
            return False
        else:
            conta=ContaPJ(numero,saldo,senha,cnpj)
            self.contas[conta.cnpj] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha,'cpf': conta.cnpj}
            return conta
        
    def criar_contaConjunta(self,numero,saldo,senha,cpf1,cpf2):
        if cpf1 in self.contas or cpf2 in self.contas:
            print("Cliente já tem uma conta nesse banco")
        else:
            conta=ContaConjunta(numero,saldo,senha,cpf1,cpf2)
            self.contas[conta.cpf1] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha,'cpf1': conta.cpf1}
            self.contas[conta.cpf2] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha,'cpf2': conta.cpf2}
            return conta

    def get_conta(self,cpf_ou_cnpj):
        if self.contas.get(cpf_ou_cnpj) :
            return self.contas.get(cpf_ou_cnpj)
        return False
        
    def verificar_credenciais(self, cpf_ou_cnpj, senha):
        conta = self.contas.get(cpf_ou_cnpj)
        if conta and conta['senha'] == senha:
            return True
        return False
    
    def retirada(self,cpf_ou_cnpj,valor):
        conta = self.contas.get(cpf_ou_cnpj)
        if conta['saldo'] >= valor:
            conta['saldo'] -= valor
            return True
        else:
            return False
    
    def add(self,cpf_ou_cnpj,valor):
        conta = self.contas.get(cpf_ou_cnpj)
        if conta:
            conta['saldo'] += valor
            return True
        return False



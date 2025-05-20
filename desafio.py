from typing import List, Dict

menu_conta = """
u
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

usuarios: List[Dict] = []
contas: List[Dict] = []

# Função Deposito (positional only)
def deposito(saldo, valor, /, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

# Função Saque (keyword only)
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    return saldo, extrato, numero_saques

# Função Extrato (positional and keyword)
def extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato, end='')
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função Criar Usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado): ")

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

# Função Criar Conta Corrente
def criar_conta_corrente(usuarios, contas):
    cpf = input("Informe o CPF do usuário para criar a conta: ")

    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    if not usuario:
        print("Usuário não encontrado. Crie um usuário primeiro.")
        return

    numero_conta = len(contas) + 1
    conta = {
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "limite": 500,
        "numero_saques": 0,
        "limite_saques": 3
    }
    contas.append(conta)
    print(f"Conta {numero_conta} criada com sucesso para {usuario['nome']}!")

# Função que gerencia as operações de uma conta
def operacao_conta(conta):
    while True:
        opcao = input(menu_conta)

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("Valor inválido! Informe um número.")
                continue
            conta['saldo'], conta['extrato'] = deposito(conta['saldo'], valor, conta['extrato'])

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Valor inválido! Informe um número.")
                continue
            conta['saldo'], conta['extrato'], conta['numero_saques'] = saque(
                saldo=conta['saldo'],
                valor=valor,
                extrato=conta['extrato'],
                limite=conta['limite'],
                numero_saques=conta['numero_saques'],
                limite_saques=conta['limite_saques']
            )

        elif opcao == "e":
            extrato(conta['saldo'], extrato=conta['extrato'])

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Loop principal do sistema
def main():
    while True:
        print("\nMenu principal:")
        print("[u] Criar Usuário")
        print("[c] Criar Conta Corrente")
        print("[a] Acessar Conta")
        print("[q] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta_corrente(usuarios, contas)

        elif opcao == "a":
            if not contas:
                print("Nenhuma conta cadastrada. Crie uma conta primeiro.")
                continue
            try:
                numero = int(input("Informe o número da conta: "))
            except ValueError:
                print("Número inválido.")
                continue

            conta = next((c for c in contas if c['numero_conta'] == numero), None)
            if not conta:
                print("Conta não encontrada.")
                continue

            print(f"Bem-vindo, {conta['usuario']['nome']}!")
            operacao_conta(conta)

        elif opcao == "q":
            print("Saindo do sistema. Obrigado!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
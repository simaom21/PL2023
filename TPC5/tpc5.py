import re

def troco(money):

    t = money
    moedas = {
        1: 0,
        2: 0,
        5: 0,
        10: 0,
        20: 0,
        50: 0,
        100: 0,
        200: 0
    }

    # testar todas as moedas a cada iteração e repetir se ainda houver troco para dar
    while money > 0:
        for moeda in [200, 100, 50, 20, 10, 5, 2, 1]:
            if money >= moeda:
                moedas[moeda] += 1
                money -= moeda
                break

    print(f"{t / 100}€ de troco: {moedas[200]} de 2e, {moedas[100]} de 1e, {moedas[50]} de 50c, {moedas[20]} de 20c, {moedas[10]} de 10c, {moedas[5]} de 5c, {moedas[2]} de 2c, {moedas[1]} de 1c")

def levantar(str, state):
    if state["phone_up"]:
        print("Input inválido: Telefone já levantado")
        return
    state["phone_up"] = True

def pousar(str, state):
    if not state["phone_up"]:
        print("Input inválido: Telefone já pousado")
        return
    troco(state["money"])
    state["phone_up"] = False
    state["money"] = 0

def moedas(str, state):
    if not state["phone_up"]:
        print("Telefone não levantado")
        return
    coins = re.findall(r"\d+[ce]", str)

    value = 0
    for coin in coins:
        r = int(coin[:-1])
        mult = 100 if coin[len(coin) - 1] == 'e' else 1

        if mult * r not in [1,2,5,10,20,50,100,200]:
            print("Moedas inválidas")
            return

        value += mult * r

    state["money"] += value

def chamada(state, custo):
    if not state["phone_up"]:
        print("Telefone não levantado")
        return

    if state["money"] >= custo:
        state["money"] -= custo
    else:
        print(f"Sem saldo. Precisa de {custo / 100}€")

def telefonar(str, state):
    phone = str[2:]

    if not re.match(r"(00\d{9})|(\d{9})", phone):
        print("Número de telemóvel inválido")
        return

    if phone.startswith("601") or phone.startswith("641"):
        print("Número bloqueado")
    elif phone.startswith("00"):
        chamada(state, 150)
    elif phone.startswith("2"):
        chamada(state, 25)
    elif phone.startswith("808"):
        chamada(state, 10)

def abortar(str, state):
    if not state["phone_up"]:
        print("Telefone não levantado")
        return
    troco(state["money"])
    state["money"] = 0

def sair(str, state):
    exit(0)

def main():
    states = {
        "LEVANTAR": levantar,
        "POUSAR": pousar,
        "MOEDA": moedas,
        "T": telefonar,
        "ABORTAR": abortar,
        "SAIR": sair
    }

    state = {
        "phone_up": False,
        "money": 0
    }

    while True:
        line = input()

        for k,v in states.items():
            if line.startswith(k):
                v(line, state)


if __name__ != "main":
    main()
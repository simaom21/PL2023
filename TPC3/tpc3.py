import re
import math
import json
import os


def distribuicao_anos(file):
    dist = dict()
    fp = open(file)
    lines = fp.readlines()
    line_ant = ""

    for line in lines:
        if line == line_ant:
            continue
        er = re.compile(r"\d+::(?P<ano>\d+)-")
        res = er.match(line)

        if res:
            if res.group("ano") not in dist:
                dist[res.group("ano")] = 0
            dist[res.group("ano")] += 1
        line_ant = line

    dist = dict(sorted(dist.items()))

    print("-" * 28)
    print("   ano    | Nr de Registos ")
    print("-" * 28)
    for ano in dist:
        print(f"   {ano}   | {dist[ano]}" +
              " " * (12-len(str(dist[ano]))))
    print("-" * 28)


def distribuicao_nomes(file):
    dist_nome = dict() 
    dist_apelido = dict()
    fp = open(file)
    lines = fp.readlines()
    line_ant = ""

    for line in lines:
        if line == line_ant:
            continue
        er = re.compile(r".*?::(?P<ano>\d{4})-\d{2}-\d{2}::(?P<nome>\w+)[\w|\s]+?(?P<apelido>\w+)::.*?::.*?::.*?::")
        res = er.match(line)
        if res:
            ano = int(res.group("ano"))
            nome = res.group("nome")
            apelido = res.group("apelido")
            r = 0
            sec = math.ceil(ano/100)
            if sec not in dist_nome:
                dist_nome[sec] = dict()

            if sec not in dist_apelido:
                dist_apelido[sec] = dict()

            if nome not in dist_nome[sec]:
                (dist_nome[sec])[nome] = 1
            else:
                (dist_nome[sec])[nome] += 1
            if apelido not in dist_apelido[sec]:
                (dist_apelido[sec])[apelido] = 1
            else:
                (dist_apelido[sec])[apelido] += 1
        line_ant = line
    
    for key in dist_nome:
        lista = list(dist_nome[key].items())
        lista.sort(key=lambda x: x[1], reverse=True)
        dist_nome[key] = lista[:5]

    for key in dist_apelido:
        lista = list(dist_apelido[key].items())
        lista.sort(key=lambda x: x[1], reverse=True)
        dist_apelido[key] = lista[:5]

    dist_nome = dict(sorted(dist_nome.items()))
    dist_apelido = dict(sorted(dist_apelido.items()))

    print("-" * 42)
    print(" Século |  |      Nome      | Nr registos ")
    print("-" * 42)

    for sec in dist_nome:
        i = 1
        for nome in dist_nome[sec]:
            if i == 1:
                print("   " + str(sec)+"   |"+str(i)+"º|  " +
                      nome[0] + " "*(14-len(nome[0])) + "|   "+str(nome[1]) + " "*(10-len(str(nome[1]))))

            else:
                print("        |"+str(i)+"º|  " +
                      nome[0] + " "*(14-len(nome[0]))+"|   " + str(nome[1]) + " "*(10-len(str(nome[1]))))
            i += 1
        print("-" * 42)

    print("\n\n" + "-" * 42)
    print(" Século |  |     Apelido    | Nr registos ")
    print("-" * 42)

    for sec in dist_apelido:
        i = 1
        for apelido in dist_apelido[sec]:
            if i == 1:
                print("   " + str(sec)+"   |"+str(i)+"º|  " +
                      apelido[0] + " "*(14-len(apelido[0])) + "|   "+str(apelido[1]) + " "*(10-len(str(apelido[1]))))

            else:
                print("        |"+str(i)+"º|  " +
                      apelido[0] + " "*(14-len(apelido[0]))+"|   " + str(apelido[1]) + " "*(10-len(str(apelido[1]))))
            i += 1
        print("-" * 42)


def distribuicao_relacao(file):
    dist = dict()
    fp = open(file)
    lines = fp.readlines()
    line_ant = ""

    for line in lines:
        if line_ant == line:
            continue
        er = re.compile(r"(:{2}|\.)\s*[\w\s]+?,\s*(?P<relacao>[\w\s]+?)\.\s*Proc\.\d+")
        res = er.finditer(line)
        if res:
            for elem in res:
                relacao = elem.group("relacao")
                if relacao not in dist:
                    dist[relacao] = 1
                else:
                    dist[relacao] += 1
        line_ant = line

    dist = dict(sorted(dist.items()))

    print("-" * 41)
    print("          Relação           | Nr pessoas ")
    print("-" * 41)

    for relacao in dist:
        print(f" {relacao}"+" "*(27-len(str(relacao))) +
              f"| {dist[relacao]}" + " " * (11-len(str(dist[relacao]))))
    print("-" * 41)


def fich_json(file_name):
    fp = open(file_name, "r")
    f = open("dict.json", "w")
    i = 0
    lines = fp.readlines()
    lista = []
    er = re.compile(r"(?P<pasta>\d+?)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>\w[\w|\s]+?)::(?P<pai>\w[\w|\s]+?)::(?P<mae>\w[\w|\s]+?)(?P<Observações>::.*?::)")
    line_ant = ""

    for line in lines:
        if line == line_ant:
            continue
        elif i == 20:
            break
        res = er.match(line)
        if res:
            dados = dict()
            dados['pasta'] = res.group("pasta")
            dados['data'] = res.group("data")
            dados['nome'] = res.group("nome")
            dados['pai'] = res.group("pai")
            dados['mae'] = res.group("mae")

            er_observacoes = re.compile(r"(:{2}|\.)?\s*(?P<relacao>[\w\s]+?,\s*[\w\s]+?\.)\s*(?P<processo>Proc\.\d+)?")

            dados["Observacoes"] = dict()
            dados["Observacoes"]["relacoes"] = []
            dados["Observacoes"]["outros"] = []

            res1 = er_observacoes.finditer(res.group("Observações"))

            if res1:
                for elem in res1:
                    if elem.group("processo"):
                        (dados["Observacoes"])["relacoes"].append(
                            elem.group("relacao")+elem.group("processo"))
                    else:
                        (dados["Observacoes"])["outros"].append(
                            elem.group("relacao"))
        lista.append(dados)
        i += 1
        line_ant = line
    json.dump(lista, f, indent=' ')



def main():	
	while True:
		print("-------------Selecione o exercício pretendido-------------")
		print("1 - Frequência de processos por ano")
		print("2 - Frequência de nomes")
		print("3 - Frequêcia dos tipos de relações")
		print("4 - Converter os 20 primeiros registos em um ficheiro json")
		string = input()
		os.system('clear')
		match string:
			case "1":
				distribuicao_anos("processos.txt")
			case "2":
				distribuicao_nomes("processos.txt")
			case "3":
				distribuicao_relacao("processos.txt")
			case "4":
				fich_json("processos.txt")
			case "q":
				break


if __name__ == "__main__":
	main()
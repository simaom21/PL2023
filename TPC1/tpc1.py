from matplotlib import pyplot as plt
import textwrap

class heart:
	
	def __init__(self):
		with open("myheart.csv") as fp:
			file = fp.readlines()
			file.pop(0)
			self.heart = []
			for i in file:
				x = i.split(",")
				tuple_ = (int(x[0]),x[1],int(x[2]),int(x[3]),int(x[4]), True if x[5] == '1\n' else False)
				self.heart.append(tuple_)

	def distSexo(self):
		m = 0
		f = 0
		for i in self.heart:
			if i[5] == True:
				if i[1] == "M":
					m += 1
				else:
					f += 1
		return [(m,f)]

	def distIdade(self):
		r = {}
		for i in self.heart:
			if i[5] == True:
				idade = i[0]-i[0]%5
				try:
					value = r[idade]
					r[idade] = value+1
				except:
					r[idade] = 1
		return sorted(r.items(), key=lambda x:x[0])

	def distColestrol(self):
		r = {}
		for i in self.heart:
			if i[5] == True:
				colesterol = i[3]-i[3]%10
				try:
					value = r[colesterol]
					r[colesterol] = value+1
				except:
					r[colesterol] = 1
		return sorted(r.items(), key=lambda x:x[0])

def printTable(title, rows):

	max_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]

	title_line = '+'.join('-' * (int(len(title)/2)+1) for i in range(len(rows[0])))
	title = textwrap.fill(title, 80)
	title = f"\n{title_line}\n|{title:^{sum(max_widths) + 4}}|\n{title_line}\n"

	sep = '+'.join('-' * (max_widths[i] + 2) for i in range(len(rows[0])))

	table = ''
	for row in rows:
		table += '\n' + '|'.join(textwrap.wrap(' | '.join(f"{r:<{max_widths[i]}}" for i, r in enumerate(row)), width=80))

	print(f"{title}{table}\n{sep}")

def main():
    h = heart()
    distSexo = h.distSexo()
    distIdade = h.distIdade()
    distColestrol = h.distColestrol()
    printTable("Distribuicao por sexo", distSexo)
    y1 = ["Masculino", "Feminino"]
    y2 = list(h.distSexo()[0])
    plt.bar(y1, y2, color="red")
    plt.xlabel("Género")
    plt.ylabel("Número de doentes")
    plt.title("Distribuição da doença por Género")
    plt.show()

    printTable("Distribuicao por idade", distIdade)
    y1 = dict(distIdade).keys()
    y2 = dict(distIdade).values()
    plt.bar(y1, y2, color="red")
    plt.xlabel("Faixa Etária (em anos)")
    plt.ylabel("Número de doentes")
    plt.title("Distribuição da doença por Idade")
    plt.show()

    printTable("Distribuicao por colesterol", distColestrol)
    y1 = dict(distColestrol).keys()
    y2 = dict(distColestrol).values()
    plt.bar(y1, y2, color="red")
    plt.xlabel("Valores de Colestrol")
    plt.ylabel("Número de doentes")
    plt.title("Distribuição da doença por níveis de Colestrol")
    plt.show()

main()
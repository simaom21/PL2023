import sys

def reader():
     
    a_somar = True
    numero = ""
    resultado = 0
    pos = 0
    in_number = False

    for line in sys.stdin:
        pos = 0
        if line.lower().strip() == 'quit':
            break

        for char in line:
            
            if char.isdigit():
                numero += char
                in_number = True
            else :
                if a_somar and in_number:
                    resultado += int(numero)
                    numero = ""
                
                if char == '=':
                    print("Resultado = " + str(resultado))

                elif char.lower() == 'o':
                    if line.lower().startswith("off", pos):
                        a_somar = False
                        numero = ''

                    elif line.lower().startswith("on", pos):
                        a_somar = True
                        numero = ''
                in_number = False
            pos += 1
        


def main():
    reader()

if __name__ == "__main__":
    main()
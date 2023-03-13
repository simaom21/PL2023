import re
import json
from statistics import mean


def conversor(f_name):

    with open(f_name + ".csv") as file:
        lines = file.readlines()
    
    header_re = re.compile(r"([^,{]+)(?:\{(\d+)(?:,(\d+))?\}(?:::(\w+))?)?[,]?")
    header_fields = header_re.findall(lines[0].strip())


    header = []
    lists = dict()
    aggregates = dict()
    for i in range(0, len(header_fields)):
        field = header_fields[i][0]
        quantity1 = header_fields[i][1]
        quantity2 = header_fields[i][2]
        aggregate = header_fields[i][3]

        header.append(field)

        if aggregate != '':
            lists[field] = (quantity1, quantity2)
            aggregates[field] = aggregate
        elif quantity1 != '':
            lists[field] = (quantity1, quantity2)


    body_re = ""
    for field in header:
        if field in lists:
            if lists[field][1] != '':
                quantity = f"{{{int(lists[field][0])},{int(lists[field][1])}}}"
            else:
                quantity = f"{{{int(lists[field][0])}}}"

            body_re += rf"(?P<{field}>([^,]+[,]?){quantity})[,]?"
        else:
            body_re += rf"(?P<{field}>[^,]+)[,]?"

    body_re = re.compile(body_re)


    data = list()
    for line in lines[1:]:
        matches = body_re.finditer(line.strip())
        data += [match.groupdict() for match in matches]
    
    

    for elem in data:
        for field in header:
            if field in lists:
                elem[field] = [int(num) for num in re.findall(r"\d+", elem[field])]
            
            if field in aggregates:
                if aggregates[field] == "sum":
                    elem[field] = sum(elem[field])
                elif aggregates[field] == "media":
                    elem[field] = mean(elem[field])


    with open(f_name + ".json", "w") as json_file:
        json.dump(data, json_file, indent=len(header), ensure_ascii=False)    



def main():

    while True:
        print("Indique o nome do ficheiro que pretende converter (sem extensão):")
        file = input()

        match file:
            case "q":
                break
            case _:
                try:
                    conversor(file)
                except:
                    print("Ficheiro inexistente.")
    
     


if __name__ == '__main__':
    main()
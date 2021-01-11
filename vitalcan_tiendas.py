import argparse
import json
import re
import requests

parser = argparse.ArgumentParser(
    description = "Obtener datos sobre tiendas oficiales de Vitalcan. Se puede 'renovar' el archivo json si no hay ninguno o si se sospecha que pudo ser actualizado"
    )
parser.add_argument(
    "-r", "--renew", default = False, 
    help = "Baja el archivo json y renueva el que se encuentra en el mismo lugar para trabajar", action = "store_true")
parser.add_argument(
    "-t", "--title", type = str, default = ".*", help = "Expresión regular que identifique el nombre de la tienda (si tiene)"
    )
parser.add_argument(
    "-c", "--city", type = str, default = ".*", help = "Expresión regular que identifique la localidad a buscar"
    )
parser.add_argument(
    "-pc", "--postal-code", type = str, default = ".*", help = "Expresión regular que identifique el código postal"
    )
parser.add_argument(
    "-p", "--phone",   type = str, default = ".*", help = "Expresión regular que identifique al número de teléfono"
    )
parser.add_argument(
    "-a", "--address", type = str, default = ".*", help = "Expresión regular que identifique la calle y la altura ('CALLE NÚMERO')"
    )

try:
    args = parser.parse_args()
    
    search_url = "https://www.vitalcan.com/buscador-tiendas-ajax.php"

    file = "vitalcan_tiendas.json"
    encode = "utf-8"
    
    title = "title"
    city = "localidad"
    postal_code = "cp"
    phone = "telefono"
    address = "direccion"

    if args.renew:
        response = requests.post(
            url = search_url
        )
        response.raise_for_status()
        fh = open(file = file, mode = "w+", encoding = encode)
        fh.write(response.content.decode(encoding = encode))
        fh.close()
        print("Ahora podes realizar la búsqueda...")
        exit()
    
    try:
        data = json.load(open(file = file, encoding = encode))
    except Exception as e:
        print(e)
        print("Probar ejecutando con la opción --renew")
        exit()
    
    def filter_by_match(entry):
        return (
            re.match(args.title, entry[title], re.IGNORECASE) and re.match(args.city, entry[city], re.IGNORECASE) and \
            re.match(args.postal_code, entry[postal_code], re.IGNORECASE) and re.match(args.phone, entry[phone], re.IGNORECASE) and \
            re.match(args.address, entry[address], re.IGNORECASE)
        )
    print(json.dumps(list(filter(filter_by_match, data)), indent = 4))
except Exception as e:
    print(e)
        
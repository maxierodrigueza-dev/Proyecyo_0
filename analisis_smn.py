import datetime
import sys
from pathlib import Path
import json




#================= APARTADO DE FUNCIONES ====================

def leer_observaciones(ruta: Path) -> dict:   
    # Proba leer el archivo con utf-8 o proba leer el archivo con latin-1 
    try: #
        with open(ruta, encoding="utf-8") as f:
            lineas_leidas = f.readlines()

    except UnicodeDecodeError:
        with open(ruta, encoding="latin-1") as f:
            lineas_leidas = f.readlines()   

        
            # iniciar variables 
            mi_dicc = {}
            lineas_invalidas = 0 

            for x in lineas_leidas:
                algo = x.strip(" / \n")
                campos = algo.split(";")

                if len(campos) != 10:
                    lineas_invalidas += 1 
                    continue

                # Limpiar los espacios en blancos de ciudad
                ciuad_estación = campos[0].strip()

                # Parsear y pasar a int o a float
                hora = campos[2]
                condición_del_cielo = campos[3]
                visibilidad = campos[4]
                try: 
                    temperatura_C = float(campos[5])
                    humedad = int(campos[7])
                    presión_hPa = float(campos[9])
                except ValueError:
                    lineas_invalidas += 1 
                    continue

                sensación_térmica_C = campos[6]  # — puede venir como el texto No se calcula en vez de un número
               
                viento = campos[8]  # dirección y velocidad juntos (por ejemplo Sur  5, o Calma cuando no hay viento)
               

                #Para la fecha
                objeto_datetime = parsear_fecha_hora(campos[1], campos[2])

                # Apartado del Sensacion_termina_C
                if "No se calcula" not in sensación_térmica_C:
                    sensación_térmica_C = float(sensación_térmica_C)
                else:
                    sensación_térmica_C = None 

                #viento
                direccion, velocidad = separar_viento(viento)


                # Append a todo el dicc
                mi_dicc[ciuad_estación] = {
                    "Fecha": objeto_datetime,
                    "Hora": hora,
                    "Condicion del cielo": condición_del_cielo,
                    "Visibilidad": visibilidad,
                    "temperatura(°C)": temperatura_C,
                    "Sensación térmica (°C)": sensación_térmica_C,
                    "Humedad (%)": humedad,
                    "Dirección del viento": direccion,
                    "Velocidad del viento": velocidad,
                    "Presión (hPa)": presión_hPa,
                }
            
            return mi_dicc, lineas_invalidas
    except FileNotFoundError:
        print("Error: No se encontró el archivo especificado.")
        sys.exit(1)
    
#cantidad total de ciudades leídas
def cantidad_ciudades_leidas(ciudades:dict) -> int:
    """Devuelve la cantidad total de ciudades leídas."""
    return len(ciudades)


# Ciudades con toda la info
def cantidad_ciudades_completas(observaciones: dict) -> int:
    """Devuelve la cantidad de ciudades sin ningún dato faltante."""

    numero= 0
    for valores in observaciones.values():
        if None not in valores.values():
            numero += 1
    return numero


#Funcion generica
def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    """Devuelve las n (por parámetro) ciudades ordenadas según 'campo', de mayor a menor
    (o al revés si descendente=False), en una lista. Reutilizable tanto para temperatura
    como para viento."""
    lista_valores = []
    

    for ciudad,info in observaciones.items():
        c = ciudad
        valor = info[campo]

        if valor == None:
            continue

        lista_valores.append((valor, c))

    lista_valores.sort(reverse=descendente)
    resultado = lista_valores[:n]


    if not resultado: # si la lista esta vacía
        return resultado # termina acá y devuelve []
    
    valor_de_corte = resultado[-1][0]
    for i in lista_valores[n:]:
        if i[0] == valor_de_corte:
            resultado.append(i)
        else:
            break
    return resultado


# Apartado de viento
def separar_viento(campo_viento: str) -> tuple:
    """Convierte un campo de viento como 'Norte  3' en (dirección, velocidad).
    Contempla el caso 'Calma' (sin velocidad numérica)."""
    viento_separado = campo_viento.split()

    if "Calma" in viento_separado:
            direccion = "Calma"
            velocidad = 0.0
    else:
            direccion = " ".join(viento_separado[:-1])
            velocidad = float(viento_separado[-1])
    return direccion, velocidad


#Reporte de información faltante
def reporte_faltantes(observaciones: dict) -> dict:
    """El objetivo es que esta función arme y devuelva un diccionario nuevo a modo de "reporte".
    Las claves de este diccionario van a ser los nombres de los campos que tienen faltantes
    (por ejemplo, "Sensación térmica (°C)")
    y el valor va a ser una lista con los nombres de las ciudades afectadas."""

    afectadas = {}
    for ciudad,informacion in observaciones.items():
        c = ciudad
        for campo in informacion:
            if informacion[campo] == None:
                if campo not in afectadas:
                    afectadas[campo] = [c]
                else:
                    afectadas[campo].append(c)
    return afectadas

# Parsear la fecha
def parsear_fecha_hora(fecha: str, hora: str) -> datetime.datetime:
    """Convierte 'dd-mes-aaaa' y 'hh:mm' del SMN en un datetime."""
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, 
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, 
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    partes_fecha = fecha.split("-")
    dia = int(partes_fecha[0])
    mes = meses[partes_fecha[1]]
    anio = int(partes_fecha[2])
    
    partes_hora = hora.split(":")
    horas = int(partes_hora[0])
    minutos = int(partes_hora[1])
    
    return datetime.datetime(anio, mes, dia, horas, minutos)

#Horas
def horarios_reportados(observaciones: dict) -> list:
    mi_lista = []
    for info in observaciones.values():
        hora_actual = info["Hora"]
        if hora_actual not in mi_lista:
            mi_lista.append(hora_actual)
    mi_lista.sort()
    return mi_lista

#================================== RESUMEN ==================================

def mostrar_resumen(observaciones: dict, n=5) -> None:
 """Imprime por pantalla el resumen con todas las características calculadas. Usar n=5"""

 print("--- Resumen Meteorológico ---")

 # Ciudades leidas
 total = cantidad_ciudades_leidas(observaciones)
 print(f"Cantidad total de ciudades leídas: {total}")

 #Cantidad de cuidades con toda la info
 total_completas = cantidad_ciudades_completas(observaciones)
 print(f"Ciudades con toda la información: {total_completas}")

 # Temperaturas máximas y mínimas usando top_n_ciudades
 top_calidas = top_n_ciudades(observaciones, "temperatura(°C)", n, descendente=True)
 top_minimas = top_n_ciudades(observaciones,"temperatura(°C)", n, descendente=False)
 print("\nTop 5 ciudades más cálidas:")
 for valor, ciudad in top_calidas:
     print(f"- {ciudad}: {valor}°C")

 print("\nTop 5 ciudades más frias:")
 for valor, ciudad in top_minimas:
     print(f"- {ciudad}: {valor}°C")

 #Dirección del viento y velocidad ¿
 top_viento_max = top_n_ciudades(observaciones, "Velocidad del viento", n, descendente=True)
 top_viento_min = top_n_ciudades(observaciones, "Velocidad del viento", n, descendente=False)
 print("\nTop 5 ciudades más ventosas:")
 for valor, ciudad in top_viento_max:
     print(f"- {ciudad}: {valor}")

 print("\nTop 5 ciudades menos ventosas:")
 for valor, ciudad in top_viento_min:
     print(f"- {ciudad}: {valor}")

 #Horas
 hora = horarios_reportados(observaciones)
 print(f"\nHorarios reportados:\n{', '.join(hora)}") # alterno comillas simples dentro de {} para que no tire error 


 # Reporte de faltantes
 print("\nInformación faltante:")
 faltantes = reporte_faltantes(observaciones)
 if not faltantes: # Si no hay columnas faltantes imprimi esto
     print("No hay columnas con datos faltantes")
 else:
     for campo, ciudades in faltantes.items(): #Si hay columnas faltantes hace esto
        print(f"Ciudades sin toda la información: {len(ciudades)}\n{campo}: {ciudades}")


#================================== TERMINAL ==================================


if __name__ == '__main__':
    # Verificar que le hayas pasado argumento correctamente a la terminal
    if len(sys.argv) > 2: # Si le pasaste mas de 2 argumentos a la terminal= error
        print("Error: Ingresó demasiados parámetros antes de cerrar el programa.")
        sys.exit(1)

    elif len(sys.argv) == 1: # Si le pasas 1 le das una ayuda al usuario diciendo q carpetas tiene en datos
        print("Error: Falta ingresar la ruta del archivo.")
        datos_txt =list(Path("datos").glob("*.txt"))
        datos_json = list(Path("obs_json").glob("*.json"))
        print(f"Archivos disponibles: {len(datos_txt)} .txt y {len(datos_json)} .json")
        sys.exit(1)

    else: # Si le pasas 2 archivos el poscision 1 va a ser el path
        ruta_archivo = Path(sys.argv[1])

        # Verificar si es .txt o .json
        if ruta_archivo.suffix == ".txt":

            #Creacion de las dos variables
            diccionario_final, lineas_invalidas = leer_observaciones(ruta_archivo)

            # Imprime el aviso si hubo errores
            if lineas_invalidas > 0:
                print(f"Aviso: Se ignoraron {lineas_invalidas} líneas por formato inválido.\n")
            
            print('Parseando Fecha a Json...')
            for valores in diccionario_final.values(): 
                # Sobreescribo el resultado de "Fecha" para que el Json lo acepte
                valores["Fecha"] = valores["Fecha"].isoformat(timespec='minutes')


            salida = Path("obs_json")
            print('archivo del SMN, convirtiendo a json...')

            if salida.exists():
                print("Ya existe el directorio")
            else:
                salida.mkdir(parents=True, exist_ok=True) # creo archivo
                print('el directorio obs_json no existe, creándolo...')
            
            ruta = salida / f"{ruta_archivo.stem}.json"

            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(diccionario_final, archivo, ensure_ascii=False, indent=2)

           
            print(cantidad_ciudades_leidas(diccionario_final))
            print(cantidad_ciudades_completas(diccionario_final))

        elif ruta_archivo.suffix == ".json":
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos_json = json.load(archivo)

            print(cantidad_ciudades_leidas(datos_json))
            print(cantidad_ciudades_completas(datos_json))                

        else:
            print("Error: la extensión no es ni .txt ni .json.")





#================= APARTADO DE JSON ====================

#0:56hs 9/10
import os
import copy
import time
import random
from pyfiglet import Figlet
from colorama import Back, Style
font = Figlet(font='rounded')

PATH_ARCHIVO = "winners.csv"

# Tiempo de espera entre jugadores
# (En segundos):
ESPERA = 3

# 0 -> NO hay barco
# 1 -> SI hay barco
# 2 -> Tiro fallido
# 3 -> Tiro efectivo

TABLERO_BASE = [
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0]
    ]

NUMEROS_A_LETRAS = ['A', 'B', 'C', 'D', 'E']

LETRAS_A_NUMEROS = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
}

NUMERO_A_EMOJI = ['🌊', '🚢', '❌', '🔥']

SEPARADOR = "──────────────────────────────────────"

def azul(texto: str):
    return Back.CYAN + texto + Style.RESET_ALL

# Función para limpiar consola dependiendo del sistema operativo
def limpiar_consola ():
    os.system('cls' if os.name == 'nt' else 'clear')
    imprmir_titulo("Battleship")

# Función para imprimir al centro de la terminal
def print_center (texto:str):
    size = os.get_terminal_size().columns
    print(texto.center(size))

# Función para obtener un string offset
# para poder centrar textos
def get_offset(text: str):
    terminal_width = os.get_terminal_size().columns
    offset  = int((terminal_width-len(text))/2)
    offset_string = ""
    for i in range(offset):
        offset_string+= " "
    return offset_string

def input_center (pregunta: str):
    offset_string = get_offset(pregunta)
    respuesta = input(offset_string+pregunta)
    return respuesta

def imprmir_titulo (text: str):
    size = os.get_terminal_size().columns
    title = font.renderText(text)
    lines = title.split("\n")

    for line in lines:
        print(line.center(size))

# Función para mostrar titulo y autores del juego
def intro ():
    size = os.get_terminal_size().columns
    text = "By: Eduardo, Felipe & Aldo"

    print(SEPARADOR.center(size))
    print(text.center(size))
    print(SEPARADOR.center(size))
    print("\n")

# Función para gráficar el tablero en la terminal
def graficar_tablero (tablero: list):
    header = azul("┌───┬────┬────┬────┬────┬────┐")
    offset_string = get_offset(header) + "     "

    print(offset_string+header)
    print(offset_string+azul("│   │ A  │ B  │ C  │ D  │ E  │"))
    for n in range(len(tablero)):
        fila = tablero[n]
        print(offset_string+azul("├───┼────┼────┼────┼────┼────┤"))
        fila_str = azul(f"│ {n + 1} │ ")
        for n in range(len(fila)):
            casilla = fila[n]
            if n != len(fila) - 1:
                fila_str += azul(NUMERO_A_EMOJI[casilla] + " │ ")
            else:
                fila_str += azul(NUMERO_A_EMOJI[casilla] + " │")

        print(offset_string+fila_str)
    print(offset_string+azul("└───┴────┴────┴────┴────┴────┘"))

def posicion_aleatoria():
    x = random.randrange(5)
    y = random.randrange(5)
    return [x,y]

def coord_a_pos (coord: str):
    coord = coord.upper()
    mensaje_error = "Coordenada Inválida - "
    error = ""
    if len(coord) != 2:
        error = "Longitud de la coordenada inválida"
    
    letra, numero = [value for value in coord]
    numero = int(numero) - 1
    if not(letra in LETRAS_A_NUMEROS):
        error = "Letra no válida"
    
    if numero > 4:
        error = "5 es la máxima coordenada"

    if error:
        print_center(mensaje_error+error)
        return []
    
    posicion = [numero, LETRAS_A_NUMEROS[letra]]
    
    return posicion

def solicitar_tablero(jugador: int):
    pregunta = f"Escribe tu el nombre del Jugador {jugador}: "
    offset_string = get_offset(pregunta)
    nombre = input(offset_string+pregunta)

    tablero = copy.deepcopy(TABLERO_BASE)

    confirmar = False

    while not(confirmar):
        print_center(f"{nombre} elige tus barcos")
        aleatorio = input_center("Barcos aleatorios?: (s/n)")

        for n in range(5):
            posicion = []
            while not(posicion):
                if aleatorio == "s":
                    posicion = posicion_aleatoria()
                    posicion_previa = tablero[posicion[0]][posicion[1]]
                    while posicion_previa != 0:
                        posicion = posicion_aleatoria()
                        posicion_previa = tablero[posicion[0]][posicion[1]]
                else:
                    pregunta_coord = f"Jugador {jugador} - Barco {n + 1}: "
                    coordenada = input_center(pregunta_coord)
                    posicion = coord_a_pos(coordenada)
                    posicion_previa = tablero[posicion[0]][posicion[1]]
                    if posicion_previa == 1 and aleatorio != "s":
                        posicion = []
                        mensaje_error = "Coordenada inválida - Ya fue elegida antes"
                        print_center(mensaje_error)
            x,y = posicion
            tablero[x][y] = 1

        print_center(f"Barcos de: {nombre}")
        graficar_tablero(tablero)

        pregunta_confirmar = "Confirmar selección: (s/n): "
        confirmacion = input_center(pregunta_confirmar)
        if confirmacion != "s":
            tablero = copy.deepcopy(TABLERO_BASE)
        else:
            confirmar = True

    return [tablero, nombre]

def siguiente_jugador (segundos: int):
    limpiar_consola()
    for n in range(segundos):
        imprmir_titulo(str(n + 1))
        time.sleep(1)
        limpiar_consola()

def guardar_ganador (nombre: str):
    f = open(PATH_ARCHIVO)
    archivo = f.read()
    data: list = archivo.split("\n")

    nueva_data = []
    no_encontrado = True

    for usuario in data:
        # Por si hay una línea vacía
        if usuario == "":
            continue
        nombre_usuario, vic_str = usuario.split(",")
        victorias = int(vic_str)
        if nombre_usuario == nombre:
            nueva_data.append(f"{nombre_usuario},{str(victorias + 1)}\n")
            no_encontrado = False
        else:
            nueva_data.append(f"{nombre_usuario},{str(victorias)}\n")

    if no_encontrado:
        nueva_data.append(f"{nombre},{str(1)}\n")
    
    f.close()
    f2 = open(PATH_ARCHIVO, '+r')
    f2.writelines(nueva_data)
    f2.close()
        

def empezar_juego ():
    tablero1, nombre1 = solicitar_tablero(1)
    siguiente_jugador(ESPERA)
    tablero2, nombre2 = solicitar_tablero(2)
    siguiente_jugador(ESPERA)

    nombres = [nombre1, nombre2]

    # Tableros de los jugadores
    tableros = [tablero1, tablero2]
    # Vista del tablero enemigo
    copia1 = copy.deepcopy(TABLERO_BASE)
    copia2 = copy.deepcopy(TABLERO_BASE)
    tableros_oculto = [copia1, copia2]
    barcos = [5,5]
    turno_jugador = 0
    turno_jugador_enemigo = 1 if turno_jugador == 0 else 0

    while barcos[0] > 0 and barcos[1] > 0:
        print_center(f"Turno de: {nombres[turno_jugador]}")
        graficar_tablero(tableros_oculto[turno_jugador])
        coordenada = input_center(f"Coordenada de ataque: ")
        posicion = coord_a_pos(coordenada)
        x,y = posicion
        
        casilla = tableros[turno_jugador_enemigo][x][y]

        mensaje = ""
        if casilla == 0:
            mensaje = "Tiro fallido!!"
            tableros_oculto[turno_jugador][x][y] = 2
        elif casilla == 1:
            mensaje = "Tiro acertado"
            tableros[turno_jugador_enemigo][x][y] = 3
            tableros_oculto[turno_jugador][x][y] = 3
            barcos[turno_jugador_enemigo] = barcos[turno_jugador_enemigo] - 1
        elif casilla == 2 or casilla == 3:
            mensaje = "Ya disparaste en esa coordenada, intenta de nuevo"

        limpiar_consola()
        print_center(mensaje)
        graficar_tablero(tableros_oculto[turno_jugador])

        if casilla == 0:
            time.sleep(ESPERA)
            turno_jugador = 1 if turno_jugador == 0 else 0
            siguiente_jugador(ESPERA)

    ganador = -1
    if barcos[0] == 0:
        ganador = 1
    elif barcos[1] == 0:
        ganador = 0

    guardar_ganador(nombres[ganador])
    print_center(f"Ganó el {nombres[ganador]}")

def ver_ganadores():
    f = open(PATH_ARCHIVO)
    archivo = f.read()
    usuarios = archivo.split("\n")
    data = []

    for usuario in usuarios:
        # Por si hay líneas vacías:
        if usuario == "":
            continue
        data_usuario = usuario.split(",")
        data.append(data_usuario)


    data.insert(0, ["Nombre:", "#"])

    max_name_len = 0
    for player in data:
        name = player[0]
        if len(name) > max_name_len:
            max_name_len = len(name)

    header_name = "┌──"
    header_wins = "┬───┐"
    extra_string = ""


    for n in range(max_name_len):
        extra_string += "─"

    full_header = header_name + extra_string + header_wins

    offset_string = get_offset(full_header)
    
    print(offset_string+full_header)

    for player in data:
        name, wins = player
        extra = 0
        extra_space = ""
        if len(name) != max_name_len:
            extra = max_name_len - len(name)
        
        for n in range(extra):
            extra_space += " "


        column_str = offset_string + "│ " + name + extra_space + " │ " + str(wins) + " │"
        separator1 = "├──"
        separator2 = "┼───┤"

        for n in range(max_name_len):
            separator1 += "─"
        
        print(column_str)

        if data.index(player) == len(data) - 1:
            bottom1 = "└──"
            bottom2 = "┴───┘"
            bottom_string = offset_string + bottom1 + extra_string + bottom2
            print(bottom_string)
        else:
            separator_str = offset_string + separator1 + separator2
            print(separator_str)



def menu():
    terminal_width = os.get_terminal_size().columns
    opcion = 0
    # Loop para mantener el menu activo hasta salir con (3)
    # O se ingresa una opción no válida
    while opcion != 3 and not(opcion >= 1 and opcion <= 3):
        print_center(SEPARADOR)
        print("1- Juego Nuevo".center(terminal_width))
        print("2- Desplegar puntajes".center(terminal_width))
        print("3- Salir".center(terminal_width))
        print_center(SEPARADOR)
        opcion = int(input_center("Introduce la opción: "))
        print_center(SEPARADOR)

        # Ejecutar la función correspondiente
        if opcion == 1:
            empezar_juego()
        elif opcion == 2:
            ver_ganadores()
        elif opcion == 3:
            print("Función 3")

def main():
    limpiar_consola()
    intro()
    menu()

main()
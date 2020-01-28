import random
import math
import sqlite3

def main():
    main_continue = True
    try:
        print("Que quieres hacer?")
        print("\t1) Agregar jugador")
        print("\t2) Listar jugadores")
        print("\t3) Eliminar jugador")
        print("\t4) Sortear cuadros")
        print("\t5) Salir")
        opcion = int(input("Opcion: "))
        if (opcion == 1):
            nombre = input("Nombre: ")
            cuadros = int(input("Cuadros: "))
            try:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                
                query = """INSERT INTO players (name, squares)
                            VALUES (?, ?);"""
                data_tuple = (nombre, cuadros)
                cursor.execute(query, data_tuple)
                conn.commit()
                cursor.close()
            except sqlite3.Error as error:
                print("Error en la DB: ", error)
            finally:
                if (conn):
                    conn.close()
        elif (opcion == 2):
            print("Lista de jugadores: ")
            try:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                
                query = """SELECT * FROM players WHERE squares > 0;"""
                cursor.execute(query)
                records = cursor.fetchall()
                print("Hay ", len(records), " registrados:")
                for row in records:
                    print("\tID: ", row[0], ", ", row[1], " con ", row[2], " cuadros.")
                print("\n")
                cursor.close()
            except sqlite3.Error as error:
                print("Error en la DB: ", error)
            finally:
                if (conn):
                    conn.close()
        elif (opcion == 3):
            jugador = int(input("Jugador a eliminar: "))
            try:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                query = """SELECT * FROM players WHERE id = ?;"""
                cursor.execute (query, (jugador,))
                records = cursor.fetchall()
                opcion = input("Está seguro que quiere eliminar a " + records[0][1] + "? [y/N] ")
                if (opcion.upper() == "Y"):
                    query = """DELETE FROM players WHERE id = ?;"""
                    cursor.execute(query, (jugador,))
                    conn.commit()
                print("\n")
                cursor.close()
            except sqlite3.Error as error:
                print("Error en la DB: ", error)
            except IndexError as error:
                print("El jugador que seleccionó no existe, intente nuevamente.\n")
            finally:
                if (conn):
                    conn.close()
        elif (opcion == 4):
            cuadros = []
            for i in range(10):
                new = []
                for j in range(10):
                    new.append(0)
                cuadros.append(new)
            try:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                
                query = """SELECT * FROM players;"""
                cursor.execute(query)
                records = cursor.fetchall()
                lugares_encontrados = 0
                for row in records:
                    for squares in range(row[2]):
                        found = False
                        while not found:
                            rando = random.randrange(100)
                            x = math.floor(rando / 10)
                            y = rando % 10
                            igual = False
                            for i in range(10):
                                if (cuadros[x][i] == row[0]):
                                    igual = True
                                    break
                            if (not igual):
                                for i in range(10):
                                    if (cuadros[i][y] == row[0]):
                                        igual = True
                                        break
                            if (igual):
                                continue
                            else:
                                if (cuadros[x][y] > 0):
                                    continue
                                else:
                                    found = True
                                    lugares_encontrados += 1
                                    print("Encontré el lugar:", lugares_encontrados, "en", x, ",", y)
                                    cuadros[x][y] = row[0]
                for i in range(10):
                    linea = ""
                    for j in range(10):
                        str_id = ""
                        if (cuadros[i][j] < 10):
                            str_id = "0" + str(cuadros[i][j])
                        else:
                            str_id = str(cuadros[i][j])
                        linea += str_id + "\t"
                    print(linea)
                cursor.close()
            except sqlite3.Error as error:
                print("Error en la DB: ", error)
            finally:
                if (conn):
                    conn.close()
        elif (opcion == 5):
            print("Adios!")
            main_continue = False
        else:
            print("Opción incorrecta, intente nuevamente.\n")
    except ValueError:
        print("Lo que ingresó es incorrecto, intente nuevamente.\n")

    if (main_continue):
        main()

if __name__ == "__main__":
    main()
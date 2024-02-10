import conexion

conexion = conexion.conexion()

def borrar_modelo():
    print("Borrando modelo...")
    
    try:
        conexion.execute("DROP DATABASE practica1_semi2")
        print("Modelo borrado")
    except Exception as e:
        print("No existe la base de datos practica1_semi2")  

def crear_modelo():
    print("Creando modelo...")
    
    try:
        conexion.execute("CREATE DATABASE practica1_semi2")
        conexion.execute("USE practica1_semi2")
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE modelo (id INT, nombre VARCHAR(50), PRIMARY KEY (id))")
        cursor.close()
        
        print("Modelo creado")
    except Exception as e:
        print("Error al crear el modelo")

def extraer_informacion():
    path = input("Ingrese el path del archivo: ")
    
    print("Extrayendo información...")
    
    cursor = conexion.cursor()
    query = '''CREATE TABLE tempTsunami (
        year text, 
        month text,
        day text,
        minute text,
        second text,
        TEV text,
        TCC text,
        EM text,
        Deposits text,
        Latitude text,
        Longitude text,
        MWH text,
        NR text,
        TM text,
        TI text,
        TD text,
        TMIS text,
        TMD text,
        TINJ text,
        TDMil text,
        TDD text,
        THD text,
        THDA text,
        COUNTRY text,
        Location text)'''
    cursor.execute("USE practica1_semi2")
    cursor.execute(query)
    cursor.close()
    
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.split(",")
            query = "INSERT INTO tempTsunami VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor = conexion.cursor()
            cursor.execute(query,data[:25])
            cursor.commit()
            cursor.close()
    
    print("Información extraída")

def menu():
    print("Seleccione una opción:")
    print("1. Borrar modelo")
    print("2. Crear modelo")
    print("3. Extraer información")
    print("4. Cargar informacion")
    print("5. Realizar consultas")
    print("6. Salir")
    
    opcion = input("Opción: ")
    
    if opcion == "1":
        borrar_modelo()
    elif opcion == "2":
        crear_modelo()
    elif opcion == "3":
        extraer_informacion()
    elif opcion == "4":
        print("1")
        #cargar_informacion()
    elif opcion == "5":
        print("1")
        #realizar_consultas()
    elif opcion == "6":
        print("Saliendo...")
        return
    else:
        print("Opción no válida")
    
    menu()

if __name__ == "__main__":
    if conexion is not None:
        menu() 

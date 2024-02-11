import conexion

conexion = conexion.conexion()

def borrar_modelo():
    print("Borrando modelo...")
    
    try:
        cursor = conexion.cursor()
        cursor.execute("DROP TABLE tsunami")
        cursor.execute("DROP TABLE dates")
        cursor.execute("DROP TABLE places")
        cursor.execute("DROP TABLE tempTsunami")
        cursor.commit()
        cursor.close()
        print("Modelo borrado")
    except Exception as e:
        print("Error al borrar el modelo")  

def crear_modelo():
    print("Creando modelo...")
    
    try:
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE dates (id INT IDENTITY(1,1), year INT, month INT, day INT, hour int, minute INT, second float, PRIMARY KEY (id))")
        cursor.execute("CREATE TABLE places (id INT IDENTITY(1,1), country VARCHAR(50), location VARCHAR(50), PRIMARY KEY (id))")
        cursor.execute('''CREATE TABLE tsunami (TEV INT, TCC INT, EM FLOAT, Deposits INT, Latitude FLOAT, Longitude FLOAT, MWH FLOAT, NR INT, TM FLOAT, TI FLOAT, TD INT, TMIS INT, TMD INT, TINJ INT, TDMil FLOAT, TDD FLOAT, THD INT, THDA INT, id_date INT, id_place INT, FOREIGN KEY (id_date) REFERENCES dates(id), FOREIGN KEY (id_place) REFERENCES places(id))''')
        query = '''CREATE TABLE tempTsunami (
            year varchar(4), 
            month varchar(4),
            day varchar(4),
            hour varchar(4),
            minute varchar(4),
            second varchar(4),
            TEV varchar(50),
            TCC varchar(50),
            EM varchar(50),
            Deposits varchar(50),
            Latitude varchar(50),
            Longitude varchar(50),
            MWH varchar(50),
            NR varchar(50),
            TM varchar(50),
            TI varchar(50),
            TD varchar(50),
            TMIS varchar(50), 
            TMD varchar(50),
            TINJ varchar(50),
            TDMil varchar(50),
            TDD varchar(50),
            THD varchar(50),
            THDA varchar(50),
            COUNTRY varchar(50),
            Location varchar(70))'''
        cursor.execute(query)
        cursor.commit()
        cursor.close()
        
        print("Modelo creado")
    except Exception as e:
        print("Error al crear el modelo",e)

def extraer_informacion():
    path = input("Ingrese el path del archivo: ")
    
    print("Extrayendo información...")
    
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            try:
                data = line.split(",")
                query = "INSERT INTO tempTsunami VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                cursor = conexion.cursor()
                cursor.execute(query,data)
                cursor.commit()
                cursor.close()
            except Exception as e:
                continue
    
    print("Información extraída")

def cargar_informacion():
    print("Cargando información...")
    
    try:
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO dates(year,month,day,hour,minute,second) SELECT DISTINCT cast(t.year as int), cast(t.month as int), cast(t.day as int), cast(t.hour as int), cast(t.minute as int), cast(t.second as float) 
                       FROM tempTsunami as t
                       WHERE (t.year IS NOT NULL AND t.year != '') AND 
                       (t.month IS NOT NULL AND t.month != '') AND
                       (t.day IS NOT NULL AND t.day != '') AND
                       (t.hour IS NOT NULL AND t.hour != '') AND
                       (t.minute IS NOT NULL AND t.minute != '') AND
                       (t.second IS NOT NULL AND t.second != '')''')
        
        cursor.execute('''INSERT INTO places(country,location) SELECT DISTINCT t.country, t.location
                        FROM tempTsunami as t
                        WHERE (t.country IS NOT NULL AND t.country != '') AND
                        (t.location IS NOT NULL AND t.location != '')''')
        
        cursor.execute('''INSERT INTO tsunami(TEV, TCC, EM, Deposits, Latitude, Longitude, MWH, NR, TM, TI, TD, TMIS, TMD, TINJ, TDMil, TDD, THD, THDA, id_date, id_place)
                        SELECT cast(t.TEV as int), cast(t.TCC as int), cast(t.EM as float), cast(t.Deposits as int), cast(t.Latitude as float), cast(t.Longitude as float), cast(t.MWH as float), cast(t.NR as int), cast(t.TM as float), cast(t.TI as float), cast(t.TD as int), cast(t.TMIS as int), cast(t.TMD as int), cast(t.TINJ as int), cast(t.TDMil as float), cast(t.TDD as int), cast(t.THD as int), cast(t.THDA as int), d.id, p.id
                        FROM tempTsunami as t
                        JOIN dates as d ON cast(t.year as int) = d.year AND cast(t.month as int) = d.month AND cast(t.day as int) = d.day AND cast(t.hour as int) = d.hour AND cast(t.minute as int) = d.minute AND cast(t.second as float) = d.second
                        JOIN places as p ON t.country = p.country AND t.location = p.location''')
        cursor.commit()
        cursor.close()
        
        print("Información cargada")
    except Exception as e:
        print("Error al cargar la información",e)

def consulta1():
    buffer = "Consulta 1\n"
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT count(*) FROM tsunami")
        rows = cursor.fetchall()
        buffer += f"No. tsunamis: {rows[0][0]} \n"
        cursor.execute("SELECT count(*) FROM dates")
        rows = cursor.fetchall()
        buffer += f"No. dates: {rows[0][0]}\n"
        cursor.execute("SELECT count(*) FROM places")
        rows = cursor.fetchall()
        buffer += f"No. places: {rows[0][0]}\n"
        cursor.close()
        return buffer
    except Exception as e:
        return "Error al realizar la consulta  \n"

def consultaDual(query, i):
    buffer = f"Consulta {i}\n"
    try:
        cursor = conexion.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            buffer += f"{row[0]}: {row[1]}\n"
        cursor.close()
        return buffer
    except Exception as e:
        return "Error al realizar la consulta {i} \n"

def consulta3():
    buffer = ""
    try:
        cursor = conexion.cursor()
        cursor.execute('''SELECT DISTINCT country FROM places''')
        rows = cursor.fetchall()
        for row in rows:
            buffer += "Pais"
            cursor.execute(f'''SELECT year FROM dates
                            JOIN tsunami ON dates.id = tsunami.id_date
                            JOIN places ON places.id = tsunami.id_place
                            WHERE country = '{row[0]}' ORDER BY year''')
            years = cursor.fetchall()
            bufferYears = row[0]
            for i in range(len(years)):
                buffer+= f",Año {i+1}"
                bufferYears += f",{years[i][0]}"
            buffer += f"\n{bufferYears}\n"
            
        cursor.close()
        f = open("consulta3.csv", "w")
        f.write(buffer)
        f.close()
    except Exception as e:
        print("Error al realizar la consulta 3 \n")

def realizar_consultas():
    print("Realizando consultas...")
    buffer = consulta1() + "\n"
    buffer += consultaDual('''SELECT country, count(*) as no_tsunamis FROM places 
                       JOIN tsunami ON places.id = tsunami.id_place 
                       GROUP BY country''',2) + "\n"
    buffer += consultaDual('''SELECT country, sum(TDMil) as total_damage FROM places 
                       JOIN tsunami ON places.id = tsunami.id_place 
                       GROUP BY country''',4) + "\n"
    buffer += consultaDual('''SELECT TOP 5 country, sum(TD) as total_Deaths FROM places 
                       JOIN tsunami ON places.id = tsunami.id_place 
                       GROUP BY country ORDER BY total_Deaths DESC''',5) + "\n"
    buffer += consultaDual('''SELECT TOP 5 year, sum(TD) as total_Deaths FROM tsunami
                       JOIN dates ON dates.id = tsunami.id_date 
                       GROUP BY year ORDER BY total_Deaths DESC''',6) + "\n"
    buffer += consultaDual('''SELECT TOP 5 year, count(*) as total_Tsunami FROM tsunami
                       JOIN dates ON dates.id = tsunami.id_date 
                       GROUP BY year ORDER BY total_Tsunami DESC''',7) + "\n"
    buffer += consultaDual('''SELECT TOP 5 country, sum(THD) as total_THD FROM tsunami
                       JOIN places ON places.id = tsunami.id_place 
                       GROUP BY country ORDER BY total_THD DESC''',8) + "\n"
    buffer += consultaDual('''SELECT TOP 5 country, sum(THDA) as total_THDA FROM tsunami
                       JOIN places ON places.id = tsunami.id_place 
                       GROUP BY country ORDER BY total_THDA DESC''',9) + "\n"
    buffer += consultaDual('''SELECT country, avg(MWH) as max_water FROM tsunami
                       JOIN places ON places.id = tsunami.id_place 
                       GROUP BY country''',10) + "\n"
    
    f = open("consultas.txt", "w")
    f.write(buffer)
    f.close()
    
    consulta3()

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
        cargar_informacion()
    elif opcion == "5":
        realizar_consultas()
    elif opcion == "6":
        print("Saliendo...")
        return
    else:
        print("Opción no válida")
    menu()

if __name__ == "__main__":
    if conexion is not None:
        menu() 

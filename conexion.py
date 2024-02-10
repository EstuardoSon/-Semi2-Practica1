import pyodbc

def conexion():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-3F7VQTP\SQLEXPRESS;UID=sa;PWD=Es2009000458;',autocommit=True)
        print('Conexion exitosa')
        return conexion
    except Exception as e:
        print(f'Error en la conexion: {e}')
        return None

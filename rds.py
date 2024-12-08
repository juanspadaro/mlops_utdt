import psycopg2

engine = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="rdsgrupo4",
    host="grupo-4-rds2.cf4i6e6cwv74.us-east-1.rds.amazonaws.com",
    port='5432'
)
cursor = engine.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios ( id SERIAL PRIMARY KEY, nombre VARCHAR(255) ); """)
cursor.execute("""SELECT * FROM usuarios;""")
rows = cursor.fetchall()
print('Primera query')
print(rows)
cursor.execute("""INSERT INTO usuarios (nombre) VALUES ('Fede');""")
cursor.execute("""SELECT * FROM usuarios;""")
rows = cursor.fetchall()
print('Segunda query')
print(rows)
engine.commit()

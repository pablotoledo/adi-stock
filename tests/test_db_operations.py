import psycopg2
import pandas as pd

# Configuración de la conexión
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="financials",
    user="your_username",
    password="your_password"
)

# Crear un DataFrame de una consulta SQL
query = "SELECT * FROM financialdata"
df = pd.read_sql_query(query, conn)

# Mostrar el DataFrame
df.head()

import oracledb
conn = oracledb.connect(user="your_username", password="your_password", dsn="localhost:1521/your_service_name")
print("Connected!")
conn.close()
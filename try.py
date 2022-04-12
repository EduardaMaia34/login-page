import sqlite3
banco = sqlite3.connect("contas.db")
cursor=banco.cursor()

#cursor.execute("CREATE TABLE contas (nome text, email text, password text)")

#cursor.execute("DELETE FROM contas WHERE email=?", ("eduardamfmcavalcanti@gmail.com",))
#cursor.execute("SELECT * FROM contas")
#print(cursor.fetchall())
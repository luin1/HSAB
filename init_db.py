import sqlite3
import time

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (content) VALUES (?)",('Pamiętaj, nigdy nie jesteś bezużyteczny! Zawsze możesz służyć, jako zły przykład.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Czasem na drodze spotykam prawdziwych szaleńców! Pędzą na złamanie karku i wbrew rozsądkowi......czasem naprawdę trudno ich wyprzedzić!',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Pamiętaj, nigdy nie jesteś bezużyteczny! Zawsze możesz służyć, jako zły przykład.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Cicho, cicho dzieci. To nie demony, nie diabły... Gorzej. To ludzie. ',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Zagłuszanie bólu na jakiś czas sprawia, że powraca ze zdwojoną siłą. ',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Lepiej zaliczać się do niektórych, niż do wszystkich.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Jestem tak dobry w spaniu, że mogę to robić z zamkniętymi oczami.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Małżeństwo to zakład o połowę majątku, że będziesz z kimś do końca życia.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Te upały przypominają człowiekowi, w jakiej części składa się z wody.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Boję się, że Reni Jusis kiedyś mnie znajdzie...',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Najwięcej blizn zostawiają bliźni.',))
time.sleep(3)
cur.execute("INSERT INTO posts (content) VALUES (?)",('Kto nie ma szczęścia w kartach, ten nie ma pieniędzy na miłość!',))

cur.execute("INSERT INTO login (username,password) VALUES (?,?)",('admin','zxc123'))

connection.commit()
connection.close()

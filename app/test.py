import psycopg2

conn = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="Qwedxzas16", port="5432")

cursor = conn.cursor()

cursor.execute("INSERT INTO public.books (id, name, description) VALUES(1, 'Мастер и Маргарита', 'Крутая книга')")

conn.commit()  # реальное выполнение команд sql1

cursor.close()
conn.close()
import psycopg2
conn = psycopg2.connect("postgresql://soup_admin:Bxg6dZlX03mv6RQNCBAHR0UmperDQAaW@dpg-d8vvad19rddc73ap7lf0-a.singapore-postgres.render.com/soup_db_2l2kgit add .")
cur = conn.cursor()
cur.execute("SELECT title FROM ptt_soup LIMIT 5;")
print(cur.fetchall())
import psycopg2

def getTablesCount():
    DB_HOST = '127.0.0.1'
    DB_NAME = 'db01'
    DB_USER = 'user1'
    DB_PASS = '1111'

    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST
                            )

    cur = conn.cursor()

    ##вывод
    cur.execute("SELECT * FROM pg_catalog.pg_tables;")
    a=cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    #parse data
    string = str(a)
    l = string.split(',')
    n = 0

    for i in range(len(l)):
        if 'bankroll' in l[i]:
            n += 1

    return n-3


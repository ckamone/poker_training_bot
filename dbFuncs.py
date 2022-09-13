import psycopg2


def create_table(id):
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

    ##создать
    cur.execute("CREATE TABLE bankroll_" + str(id) + " (id SERIAL PRIMARY KEY, money float);")

    ##внести
    cur.execute("INSERT INTO bankroll_" + str(id) + " (money) VALUES(%s)", (100000,))

    ##вывод
    #cur.execute("SELECT * FROM bankroll_" + str(id) + ";")
    #print(cur.fetchall())

    conn.commit()
    cur.close()
    conn.close()

def writeBankroll(id,money,action):
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
    cur.execute("SELECT * FROM bankroll_" + str(id) + ";")
    old=cur.fetchall()
    old=old[-1][1]

    if action=='+':
        ##внести
        cur.execute("INSERT INTO bankroll_"+str(id)+" (money) VALUES(%s)",(old+money,))
    elif action=='-':
        cur.execute("INSERT INTO bankroll_" + str(id) + " (money) VALUES(%s)", (old - money,))



    conn.commit()
    cur.close()
    conn.close()

def checkDb(id):
    try:
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
        cur.execute("SELECT * FROM bankroll_" + str(id) + ";")
        a=cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        a='0'
    return a

'''
#example
dbid=11
if checkDb(dbid)=='0':
    print('creating')
    create_table(dbid)
    print(checkDb(dbid))
else:
    print('exists',checkDb(1))

writeBankroll(11,10000,'+')
'''
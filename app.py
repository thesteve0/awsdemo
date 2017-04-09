__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, static_file, DEBUG
import os


@route('/')
def index():
    return static_file("index.html", root='./')
    #return "<h1> hello OpenShift Ninja without DB</h1>"


# since this is a read only talk to the replicas
@get('/db')
def dbexample():
    try:
        conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'),
                                host=os.environ.get('REPLICA_SERVICE_HOST'), password=os.environ.get('PG_PASSWORD'))
    except:
        print(os.environ.get('REPLICA_SERVICE_HOST'))

    cur = conn.cursor()
    # cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints limit 10""")
    cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints ORDER by parkid DESC LIMIT 10""")

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

    cur.close()
    conn.close()

    return result_string

#For Static files

@get("/static/css/<filename:re:.*\.css>")
def css(filename):
    return static_file(filename, root="static/css")

@get("/static/font/<filename:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filename):
    return static_file(filename, root="static/font")

@get("/static/img/<filename:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filename):
    return static_file(filename, root="static/img")

@get("/static/js/<filename:re:.*\.js>")
def js(filename):
    return static_file(filename, root="static/js")


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)

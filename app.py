__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, static_file, DEBUG
import os

def format_result(entries):
    result = []

    for entry in entries:
        data = {}

        data['id'] = entry['name']
        data['latitude'] = str(entry['coordinates'][0])
        data['longitude'] = str(entry['coordinates'][1])
        data['name'] = entry['toponymName']

        result.append(data)

    return result


@route('/')
def index():
    return static_file("index.html", root='./')



@get('/ws/zips')
def getzips():
    results = []
    try:
        conn = psycopg2.connect(database=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
                                host=os.environ.get('POSTGRES_HOST'), password=os.environ.get('POSTGRES_PASSWORD'))
    except:
        print("couldn't make connection" + os.environ.get('POSTGRES_HOST'))

    cur = conn.cursor()
    #TODO eventually remove the limit
    cur.execute("""select zipcode, count, ST_AsText(the_geom) from zipcodes LIMIT 100""")
    rows = cur.fetchall()

    for row in rows:
        result = {}
        result = {'zipcode': row[0], 'count': row[1]}
        coords = {}
        temp_coords = row[2]
        lon = temp_coords[temp_coords.find('(')+ 1:temp_coords.find(' ')]
        lat = temp_coords[temp_coords.find(' '):temp_coords.find(')')]
        coords = {'lon': lon, 'lat': lat}
        result['coords': coords]
        results.append(result)

    return results

@get('/ws/airports')
def getairports():
    try:
        conn = psycopg2.connect(database=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
                                host=os.environ.get('POSTGRES_HOST'), password=os.environ.get('POSTGRES_PASSWORD'))
    except:
        print(os.environ.get('POSTGRES_HOST'))

    cur = conn.cursor()

    return "howdy airports"



#This is for the parkpoints data set which may or may not be there
@get('/db')
def dbexample():
    try:
        conn = psycopg2.connect(database=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'),
                            host=os.environ.get('POSTGRES_HOST'), password=os.environ.get('POSTGRES_PASSWORD'))
    except:
        print(os.environ.get('POSTGRES_HOST'))

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

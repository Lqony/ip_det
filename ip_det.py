import sys
import urllib.request
import psycopg2

def int2ip(ip):
    str_ip=""
    for i in [3, 2, 1, 0]:
        str_ip +=(str((ip >> 8*i) % 256))
        if i > 0:
            str_ip += "."
    return str_ip


def get_info(ip):
    response = urllib.request.Request("http://v2.api.iphub.info/ip/{}".format(ip))
    response.add_header("X-Key", "")

    try:
        response = urllib.request.urlopen(response).read().decode()
    except:
        return None

    return response


#main
if len(sys.argv) < 5:
    print('Please specify db, user, pasword and host')
    exit(0)

dst_con = psycopg2.connect(dbname=sys.argv[1],
      user=sys.argv[2], host=sys,argv[4],
      password=sys.argv[3] port="5432")

dst_cur = dst_con.cursor()
dst_cur.execute("CREATE TABLE IF NOT EXISTS ip_table (info JSONB NOT NULL, found_date DATE NOT NULL DEFAULT CURRENT_DATE);")

info = None
try:
    for i in range(5, len(sys.argv)):
		ip = int2ip(sys.argv[i])
		info = get_info(ip)
		if info != None:
			dst_cur.execute("INSERT INTO ip_table (info) VALUES (\'{}\');".format(info))
			dst_con.commit()
			print('New ip found:', ip)
			print(info)
except BaseException as e:
    print(e)

dst_con.commit()
dst_cur.close()
dst_con.close()
exit(0)
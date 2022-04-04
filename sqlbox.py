import pymysql
import pymysql.cursors
import json
import pandas as pd
import time

class acomManager(object):
    def __init__(self):
        self.sqlpassword = None
        self.logindb = None
        self.acomdb = None
        self.acomtable = None
        self.dns_sort = None


    def _readCsv(self):

        csv_data = pd.read_csv("dns_sample.csv", sep = ",")

        csv_data.to_json("dns_sample.json", orient = "records")


    def _create_db(self):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password= self.sqlpassword)

        cursor = conn.cursor()

        sql = "create database if not exists {}".format(self.acomdb)

        cursor.execute(sql)

        conn.close()

    
    def import_db(self):

        self._create_db()
        
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password= self.sqlpassword,
                               database= self.acomdb,
                               cursorclass=pymysql.cursors.DictCursor,
                               charset='utf8')

        cursor = conn.cursor()

        try:
            create_tabel = """create table if not exists {0}(\
                   date varchar(100),\
                   time varchar(100),\
                   usec varchar(100),\
                   sourceip varchar(100),\
                   sourceport varchar(100),\
                   destinationip varchar(100),\
                   destinationport varchar(100),\
                   fqdn varchar(100)\
                   )engine=InnoDB DEFAULT CHARSET=utf8;""".format(self.acomtable)

            cursor.execute(create_tabel)
            conn.commit()

        except:
            conn.rollback()

        self._readCsv()

        with open('dns_sample.json', 'r') as ds:
            dns_sample = json.load(ds)

        for dns in dns_sample:

            unix_timestamp = dns['frame.time_epoch']
            usec = str(unix_timestamp).split('.')[1]
            while len(usec) < 8:
                usec = usec + '0'

            utt_format = '%Y-%m-%d %H:%M:%S'
            utt_value = time.localtime(unix_timestamp)
            datetime = time.strftime(utt_format, utt_value)
            d = datetime.split(' ')[0]
            t = datetime.split(' ')[1]

            dns['date'] = d
            dns['time'] = t
            dns['usec'] = usec


        for dns in dns_sample:
            
                dns_sql = """insert into {} (date, time, usec, sourceip, sourceport, destinationip, destinationport, fqdn)
                            values (%s, %s, %s, %s, %s, %s, %s, %s)""".format(self.acomtable)

                dns_data = (dns['date'], dns['time'], dns['usec'], dns['ip.src'], dns['udp.srcport'], dns['ip.dst'], dns['udp.dstport'], dns['dns.qry.name'])

                try:
                    cursor.execute(dns_sql, dns_data)
                    conn.commit()

                except:
                    conn.rollback()
        
        conn.close()


    def get_dns(self): 

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password= self.sqlpassword,
                               database= self.acomdb,
                               cursorclass=pymysql.cursors.DictCursor,
                               charset='utf8')

        cursor = conn.cursor()

        dns_sql = """select * from {} order by date desc""".format(self.acomtable)

        cursor.execute(dns_sql)

        dns_data = cursor.fetchall()

        dns_dict = []

        for dns in dns_data:

            node = {}

            node['date'] = dns['date']
            node['time'] = dns['time']
            node['usec'] = dns['usec']
            node['sourceip'] = dns['sourceip']
            node['sourceport'] = dns['sourceport']
            node['destinationip'] = dns['destinationip']
            node['destinationport'] = dns['destinationport']
            node['fqdn'] = dns['fqdn']

            dns_dict.append(node)

        return dns_dict


    def check_dns(self, sourceip, fromTime, toTime, fqdn):

        conn = pymysql.connect(host='localhost',
                               user='root',
                               password= self.sqlpassword,
                               database= self.acomdb,
                               cursorclass=pymysql.cursors.DictCursor,
                               charset='utf8')

        cursor = conn.cursor()

        dns_sql = """select * from {0} where sourceip = '{1}' and (date between '{2}' and '{3}') and fqdn = '{4}' order by date desc""".format(self.acomtable, sourceip, fromTime, toTime, fqdn)

        cursor.execute(dns_sql)

        dns_data = cursor.fetchall()

        dns_dict = []

        for dns in dns_data:

            node = {}

            node['date'] = dns['date']
            node['time'] = dns['time']
            node['usec'] = dns['usec']
            node['sourceip'] = dns['sourceip']
            node['sourceport'] = dns['sourceport']
            node['destinationip'] = dns['destinationip']
            node['destinationport'] = dns['destinationport']
            node['fqdn'] = dns['fqdn']

            dns_dict.append(node)

        return dns_dict


    def get(self, username):
        
        try:
            conn = pymysql.connect(host= 'localhost',
                                    user= 'root',
                                    password= self.sqlpassword,
                                    database= self.logindb,
                                    cursorclass= pymysql.cursors.DictCursor,
                                    charset= 'utf8')
        except:
            print('connect fail')

        cursor = conn.cursor()

        user = self.check(conn, cursor)
        if user:
            return None

        sql = "select password from register where username = '{0}'".format(username)

        cursor.execute(sql)

        password = cursor.fetchone()

        conn.close()

        return password


    def push(self, email, username, password):

        try:
            conn = pymysql.connect(host= 'localhost',
                                    user= 'root',
                                    password= self.sqlpassword,
                                    database= self.logindb,
                                    cursorclass= pymysql.cursors.DictCursor,
                                    charset= 'utf8')
        except:
            print('connect fail')

        user = self.check(conn, username)
        if user:
            return False

        cursor = conn.cursor()

        sql = "insert into register (email, username, password) values ('{0}', '{1}', '{2}')".format(email, username, password)

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()

        conn.close()

        return True


    def check(self, conn, username):

        cursor = conn.cursor()

        sql = "select * from register where username = '{0}'".format(username)

        try:
            cursor.execute(sql)
        except:
            conn.rollback()

        user = cursor.fetchall()

        return user




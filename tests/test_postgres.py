from compose.cli.command import get_project
import unittest
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def wait_for_postgres(dbname, user, password, host, port):
    for i in range(540):
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except psycopg2.OperationalError as e:
            print i, e.message
            time.sleep(1)


class DockerUnittestExample(unittest.TestCase):

    def setUp(self):
        self.dbname = "testdb"
        self.project = get_project('./', ['test-docker-compose2.yml'])
        self.project.up()
        wait_for_postgres(dbname='postgres', user="postgres", password="postgres", host="127.0.0.1", port="8432")

    def tearDown(self):
        pass
        self.project.kill()
        self.project.remove_stopped()

    def test_postgres(self):
        conn = psycopg2.connect(dbname='postgres', user="postgres", password="postgres", host="127.0.0.1", port="8432")
        print "Opened database successfully"

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        cur.execute('CREATE DATABASE ' + self.dbname)
        cur.execute('''CREATE TABLE COMPANY
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);''')
        print "Table created successfully"

        conn.commit()
        conn.close()
        self.project.stop('postgres')
        self.project.rm('postgres')
        self.project.up('postgres')
        wait_for_postgres(dbname='postgres', user="postgres", password="postgres", host="127.0.0.1", port="8432")
        time.sleep(60)
        cur = conn.cursor()
        cur.execute('select * from COMPANY')
        rows = cur.fetchall()
        self.assertEqual(rows,[])
        #Test something with postgres
        self.fail()


if __name__ == '__main__':
    unittest.main()
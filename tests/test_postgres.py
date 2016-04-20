from compose.cli.command import get_project
import unittest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DockerUnittestExample(unittest.TestCase):

    def setUp(self):
        self.dbname = "testdb"
        self.project = get_project('./', ['test-docker-compose.yml'])
        self.project.up()

    def tearDown(self):
        pass
        #self.project.kill()
        #self.project.remove_stopped()

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
        #Test something with postgres
        pass


if __name__ == '__main__':
    unittest.main()
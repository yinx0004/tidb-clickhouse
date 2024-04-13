from client.clickhouseclient import ClickHouseClient
from lib import sql
from lib.logger import setup_logger


class TableProcessor:
    def __init__(
            self,
            host=None,
            port=None,
            user=None,
            password=None,
            dbs=None,
            tables=None,
            ):
        self.logger = setup_logger(__name__)
        self.host = host
        self.port = port
        self.user = user
        self.passwd = password
        self.dbs = [] if dbs is None else [x for x in dbs.split(',') if x]
        self.tables = [] if tables is None else [x for x in tables.split(',') if x]
        self.client = ClickHouseClient({
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.passwd,
        })

    def table_list(self):
        self.logger.info('Listing tables...')
        tables = []
        try:
            for db in self.dbs:
                res = self.client.execute(sql.get_tables, {'db': db})
                tables = tables + res
            return tables
        except Exception as err:
            self.logger.error("Unexpected error: {}".format(str(err)))
            raise Exception("Can not list tables on host={} port={} user={} password={} dbs={}".format(
                self.host,
                self.port,
                self.user,
                self.passwd,
                self.dbs,
            ))

    def show_create_table(self, db, table):
        try:
            ddl = self.client.execute('show create table {}.{}'.format(db, table),{'db': db, 'table': table})
            return ddl
        except Exception as err:
            self.logger.error("Unexpected error: {}".format(str(err)))
            raise Exception("Can not show create table on host={} port={} user={} password={} db={} table={}".format(
                self.host,
                self.port,
                self.user,
                self.passwd,
                db,
                table,
            ))



import click
from lib.logger import setup_logger
from schema.chtableprocessor import TableProcessor
from schema.tidbtablebuilder import TableSQLBuilder
from utils.helpers import append2file


@click.group()
def cli():
    click.echo('Welcome to TiDB Tool for Clickhouse!')


@cli.command()
@click.option('--host', '-h', help='clickhouse server host', required=True)
@click.option('--port', '-P', help='clickhouse port', required=True)
@click.option('--user', '-u', help='clickhouse user', required=True)
@click.option('--passwd', '-p', help='clickhouse password', required=True)
@click.option('--dbs', '-d', help='a list of clickhouse databases name', required=True)
@click.option('--file', '-f', help='ddl output file name', default="clickhouse_ddl.sql")
def dump_clickhouse_table_schema(host, port, user, passwd, dbs, file):
    logger.info("start to connect to clickhouse server")
    tp = TableProcessor(host, port, user, passwd, dbs)
    tables = tp.table_list()
    for table in tables:
        db = table[0]
        table = table[1]
        res = tp.show_create_table(db, table)
        ddl = res[0][0] + ';\n\n'
        append2file(file, ddl)
    logger.info("Dump clickhouse table schema completed! Please find the ddl output in outputs/{}".format(file))


@cli.command()
@click.option('--host', '-h', help='clickhouse server host', required=True)
@click.option('--port', '-P', help='clickhouse port', required=True)
@click.option('--user', '-u', help='clickhouse user', required=True)
@click.option('--passwd', '-p', help='clickhouse password', required=True)
@click.option('--dbs', '-d', help='a list of clickhouse databases name', required=True)
@click.option('--file', '-f', help='ddl output file name', default="tidb_ddl.sql")
def build_tidb_table_schema(host, port, user, passwd, dbs, file):
    tidb_ddl = ''
    tb = TableSQLBuilder(host, port, user, passwd, dbs)

    for db in tb.dbs:
        database_ddl = tb.create_database_sql(db)
        tidb_ddl = tidb_ddl + database_ddl

    tables = tb.table_list()
    for table in tables:
        db_name = table[0]
        table_name = table[1]
        res = tb.get_columns_description(db_name, table_name)
        table_ddl = tb.create_table_sql(db_name, table_name, res)
        tidb_ddl = tidb_ddl + table_ddl
    append2file(file, tidb_ddl)


if __name__ == '__main__':
    logger = setup_logger(__name__)
    cli()

from schema.chtableprocessor import TableProcessor
from lib import sql
from utils.helpers import fetch_in_brackets
from lib.logger import setup_logger


class TableSQLBuilder(TableProcessor):
    """
    Build TiDB table(s)
    """

    @staticmethod
    def create_database_sql(db):
        """
        Produce create database statement for TiDB
        CREATE DATABASE
        for specified ClickHouse's db

        :param db: string - name of the DB
        :return: string - ready-to-use TiDB CREATE DATABASE statement
        """

        sql = "CREATE DATABASE IF NOT EXISTS `{}`;\n\n".format(db)
        return sql

    def get_columns_description(self, db, table):
        try:
            columns_description = []
            columns = self.client.execute(sql.get_columns, {'db': db, 'table': table})
            for column in columns:
                (name, type, default_kind, default_expression, is_in_partition_key, is_in_sorting_key, is_in_primary_key, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision) = column
                columns_description.append({
                    'name': name,
                    'type': type,
                    'default_kind': default_kind,
                    'default_expression': default_expression,
                    'is_in_partition_key': is_in_partition_key,
                    'is_in_sorting_key': is_in_sorting_key,
                    'is_in_primary_key': is_in_primary_key,
                    'character_octet_length': character_octet_length,
                    'numeric_precision': numeric_precision,
                    'numeric_precision_radix': numeric_precision_radix,
                    'numeric_scale': numeric_scale,
                    'datetime_precision': datetime_precision
                })
            return columns_description
        except Exception as err:
            self.logger.error("Unexpected error: {}".format(str(err)))
            raise Exception("Can not get column on host={} port={} user={} password={} db={} table={}".format(
                self.host,
                self.port,
                self.user,
                self.passwd,
                db,
                table,
            ))

    def fetch_primary_key_fields(self, columns_description):
        """
        Fetch list of primary keys columns names
        :param columns_description:
        :return: list | None
        """
        primary_key_fields = []
        for column_description in columns_description:
            if self.is_field_primary_key(column_description['is_in_primary_key']):
                primary_key_fields.append(column_description['name'])

        return None if not primary_key_fields else primary_key_fields

    def fetch_nullable_fields(self, columns_description):
        nullable_fields = []
        for column_description in columns_description:
            if self.is_field_nullable(column_description['type']):
                nullable_fields.append(column_description['name'])
        return None if not nullable_fields else nullable_fields

    @staticmethod
    def is_field_primary_key(field):
        """
        Check whether `key` field description value can be interpreted as True
        :param field:
        :return:
        """
        return bool(field)

    @staticmethod
    def is_field_nullable(type):
        if type.startswith('Nullable'):
            return True
        else:
            return False

    def create_table_sql(self, db, table, columns_description):
        tidb_columns = []
        engine = "ENGINE=InnoDB"
        nullable_fields = self.fetch_nullable_fields(columns_description)

        for column_description in columns_description:
            tag_null = None
            tag_default = ''

            name = column_description['name']
            clickhouse_type = column_description['type']

            if nullable_fields and name in nullable_fields:
                tidb_type = self.map_type_nullable(clickhouse_type)
            else:
                tidb_type = self.map_type(clickhouse_type)
                tag_null = "NOT NULL"

            # enum
            if tidb_type == 'ENUM':
                tidb_type = self.adjust_enum_type(tidb_type, clickhouse_type)

            if tidb_type == 'DECIMAL':
                tidb_type = self.adjust_decimal_type(tidb_type, clickhouse_type)

            if column_description['default_kind'] == 'DEFAULT':
                tag_default = '{} {}'.format(column_description['default_kind'], column_description['default_expression'])

            # string length
            if 'FixedString' in clickhouse_type and tidb_type != 'UNKNOWN':
                tag_length = column_description['character_octet_length']
            elif 'String' in clickhouse_type and tidb_type != 'UNKNOWN':
                tag_length = self.fetch_string_length(name, db, table)
            else:
                tag_length = None

            if tag_length is not None:
                tidb_type = self.adjust_string_type(tidb_type, tag_length)

            if tag_null is not None:
                column = '`{}` {} {} {}'.format(name, tidb_type, tag_null, tag_default)
            else:
                column = '`{}` {} {}'.format(name, tidb_type, tag_default)
            tidb_columns.append(column.strip())

        primary_key_fields = self.fetch_primary_key_fields(columns_description)
        if primary_key_fields:
            if len(primary_key_fields) > 1:
                primary_keys = 'PRIMARY KEY ({})'.format(', '.join(primary_key_fields))
            else:
                primary_keys = 'PRIMARY KEY ({})'.format(primary_key_fields[0])
            tidb_columns.append(primary_keys)

        sql = """CREATE TABLE IF NOT EXISTS {}.{} (
    {}
    ) {}
    ;
    \n""".format(
            db, table,
            ",\n    ".join(tidb_columns),
            engine,
        )
        return sql

    @staticmethod
    def map_type(clickhouse_type):
        # Numeric Types
        if clickhouse_type.startswith('UInt8'):
            tidb_type = 'TINYINT UNSIGNED'
        elif clickhouse_type.startswith('Int8'):
            tidb_type = 'TINYINT'
        elif clickhouse_type.startswith('UInt16'):
            tidb_type = 'SMALLINT UNSIGNED'
        elif clickhouse_type.startswith('Int16'):
            tidb_type = 'SMALLINT'
        elif clickhouse_type.startswith('UInt32'):
            tidb_type = 'INT UNSIGNED'
        elif clickhouse_type.startswith('Int32'):
            tidb_type = 'INT'
        elif clickhouse_type.startswith('UInt64'):
            tidb_type = 'BIGINT UNSIGNED'
        elif clickhouse_type.startswith('Int64'):
            tidb_type = 'BIGINT'
        elif clickhouse_type.startswith('Float32'):
            tidb_type = 'FLOAT'
        elif clickhouse_type.startswith('Float64'):
            tidb_type = 'DOUBLE'
        elif clickhouse_type.startswith('Decimal'):
            tidb_type = 'DECIMAL'
        # Date and Time Types
        elif clickhouse_type.startswith('DateTime'):
            tidb_type = 'DATETIME'
        elif clickhouse_type.startswith('Date'):
            tidb_type = 'DATE'
        # String Types
        elif clickhouse_type.startswith('FixedString'):
            tidb_type = 'CHAR'
        elif clickhouse_type.startswith('String'):
            tidb_type = 'VARCHAR'
        # SET Types
        elif clickhouse_type.startswith('Enum8'):
            tidb_type = 'ENUM'
        elif clickhouse_type.startswith('Enum16'):
            tidb_type = 'ENUM'
        #elif clickhouse_type.startswith('Array'):
        #    tidb_type = 'SET'
        elif clickhouse_type.startswith('Bool'):
            tidb_type = 'BOOLEAN'
        elif clickhouse_type.startswith("Object('json')"):
            tidb_type = 'JSON'
        else:
            tidb_type = 'UNKNOWN'

        return tidb_type

    def map_type_nullable(self, clickhouse_type):
        if clickhouse_type.startswith('Nullable'):
            type = fetch_in_brackets(clickhouse_type)
            if type:
                tidb_type = self.map_type(type)
            else:
                tidb_type = 'UNKNOWN'
            return tidb_type
        else:
            raise Exception('Not ClickHouse Nullable type {}'.format(clickhouse_type))

    def fetch_string_length(self, column, db, table):
        try:
            res = self.client.execute("SELECT max(lengthUTF8({})) as len from {}.{}".format(column, db, table))
            len = res[0][0]
            if len == 0 or len is None:
                len = 255
            return len
        except Exception as err:
            self.logger.error(err)
            raise Exception("Can't get string length for column {} in table {}".format(column, table))

    @staticmethod
    def adjust_string_type(type, string_length):
        if string_length > 255:
            tidb_type = 'TEXT'
        elif string_length > 65535:
            tidb_type = 'MEDIUMTEXT'
        elif string_length > 16777215:
            tidb_type = 'LONGTEXT'
        else:
            tidb_type = '{}({})'.format(type, string_length)
        return tidb_type

    def adjust_enum_type(self, type, clickhoust_type):
        if type == 'ENUM':
            enum = []
            res = fetch_in_brackets(clickhoust_type)
            items = res.split(',')
            for item in items:
                key = item.split('=')[0].strip()
                enum.append(key)
            enum = '({})'.format(','.join(enum))
            tidb_type = type + enum
            return tidb_type
        else:
            self.logger.error('Not enum type: {}'.format(type))
            raise Exception("Not enum type: {}".format(type))

    def adjust_decimal_type(self, type, clickhoust_type):
        if type == 'DECIMAL':
            res = fetch_in_brackets(clickhoust_type)
            decimal = '({})'.format(res)
            tidb_type = type + decimal
            return tidb_type
        else:
            self.logger.error('Not enum type: {}'.format(type))
            raise Exception("Not enum type: {}".format(type))
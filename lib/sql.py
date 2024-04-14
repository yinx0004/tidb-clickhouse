get_tables = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = %(db)s"
get_columns = "SELECT name, type, default_kind, default_expression, is_in_partition_key, is_in_sorting_key, is_in_primary_key, character_octet_length, numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision FROM system.columns WHERE database = %(db)s AND  table = %(table)s"
get_string_length = "SELECT max(lengthUTF8(%(column)s)) as len FROM %(table)s"
get_data_skipping_indices = "SELECT name, expr FROM system.data_skipping_indices WHERE database = %(db)s AND table = %(table)s"

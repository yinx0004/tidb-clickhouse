CREATE TABLE test.felix
(
    `id` Int32 DEFAULT 100
)
ENGINE = MergeTree
PRIMARY KEY id
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE test.my_first_table
(
    `user_id` UInt32,
    `message` String,
    `timestamp` DateTime,
    `metric` Float32
)
ENGINE = MergeTree
PRIMARY KEY (user_id, timestamp)
ORDER BY (user_id, timestamp)
SETTINGS index_granularity = 8192;

CREATE TABLE test.nullable
(
    `n` Nullable(UInt32)
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS index_granularity = 8192;

CREATE TABLE test.stock
(
    `s_i_id` Int32,
    `s_w_id` Int32,
    `s_quantity` Nullable(Int32),
    `s_dist_01` Nullable(String) DEFAULT NULL
)
ENGINE = MergeTree
PRIMARY KEY (s_w_id, s_i_id)
ORDER BY (s_w_id, s_i_id)
SETTINGS index_granularity = 8192;

CREATE TABLE test.users_a
(
    `uid` Int16,
    `name` String,
    `age` Int16,
    `name_len` UInt8 MATERIALIZED length(name),
    CONSTRAINT c1 ASSUME length(name) = name_len
)
ENGINE = MergeTree
ORDER BY (name_len, name)
SETTINGS index_granularity = 8192;

CREATE TABLE test.yy
(
    `name` FixedString(10)
)
ENGINE = MergeTree
PRIMARY KEY name
ORDER BY name
SETTINGS index_granularity = 8192;

CREATE TABLE test.zz
(
    `name` String
)
ENGINE = MergeTree
PRIMARY KEY name
ORDER BY name
SETTINGS index_granularity = 8192;

CREATE TABLE sherry.asynchronous_inserts
(
    `query` String,
    `database` String,
    `table` String,
    `format` String,
    `first_update` DateTime64(6),
    `total_bytes` UInt64,
    `entries.query_id` Array(String),
    `entries.bytes` Array(UInt64)
)
ENGINE = MergeTree
ORDER BY query
SETTINGS index_granularity = 8192;

CREATE TABLE sherry.certificates
(
    `version` Int32,
    `serial_number` Nullable(String),
    `signature_algo` Nullable(String),
    `issuer` Nullable(String),
    `not_before` Nullable(String),
    `not_after` Nullable(String),
    `subject` Nullable(String),
    `pkey_algo` Nullable(String),
    `path` String,
    `default` UInt8
)
ENGINE = MergeTree
PRIMARY KEY version
ORDER BY version
SETTINGS index_granularity = 8192;

CREATE TABLE sherry.dt
(
    `timestamp` DateTime('Asia/Istanbul'),
    `event_id` UInt8
)
ENGINE = TinyLog;

CREATE TABLE sherry.dt64
(
    `timestamp` DateTime64(3, 'Asia/Istanbul'),
    `event_id` UInt8
)
ENGINE = TinyLog;

CREATE TABLE sherry.float_vs_decimal
(
    `my_float` Float64,
    `my_decimal` Decimal(18, 3)
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS index_granularity = 8192;

CREATE TABLE sherry.json
(
    `o` Object('json')
)
ENGINE = Memory;

CREATE TABLE sherry.t_enum
(
    `x` Enum8('hello' = 1, 'world' = 2)
)
ENGINE = TinyLog;

CREATE TABLE sherry.test_bool
(
    `A` Int64,
    `B` Bool
)
ENGINE = Memory;

CREATE TABLE sherry.was
(
    `name` String
)
ENGINE = MergeTree
PRIMARY KEY name
ORDER BY name
SETTINGS index_granularity = 8192;


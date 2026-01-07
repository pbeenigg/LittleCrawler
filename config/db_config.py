import os

# mysql config
MYSQL_DB_PWD = os.getenv("MYSQL_DB_PWD", "123456")
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER", "root")
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST", "localhost")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT", 3306)
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME", "little_crawler")

mysql_db_config = {
    "user": MYSQL_DB_USER,
    "password": MYSQL_DB_PWD,
    "host": MYSQL_DB_HOST,
    "port": MYSQL_DB_PORT,
    "db_name": MYSQL_DB_NAME,
}


# redis config
REDIS_DB_HOST = "127.0.0.1"  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password
REDIS_DB_PORT = os.getenv("REDIS_DB_PORT", 6379)  # your redis port
REDIS_DB_NUM = os.getenv("REDIS_DB_NUM", 0)  # your redis db num

# cache type
CACHE_TYPE_REDIS = "redis"
CACHE_TYPE_MEMORY = "memory"

# sqlite config
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "sqlite_tables.db")

sqlite_db_config = {
    "db_path": SQLITE_DB_PATH
}

# mongodb config
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PWD = os.getenv("MONGODB_PWD", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "media_crawler")

mongodb_config = {
    "host": MONGODB_HOST,
    "port": int(MONGODB_PORT),
    "user": MONGODB_USER,
    "password": MONGODB_PWD,
    "db_name": MONGODB_DB_NAME,
}

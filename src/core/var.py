from asyncio.tasks import Task
from contextvars import ContextVar
from typing import List

import aiomysql

request_keyword_var: ContextVar[str] = ContextVar("request_keyword", default="")
crawler_type_var: ContextVar[str] = ContextVar("crawler_type", default="")
comment_tasks_var: ContextVar[List[Task]] = ContextVar("comment_tasks", default=[])
db_conn_pool_var: ContextVar[aiomysql.Pool] = ContextVar("db_conn_pool_var")
source_keyword_var: ContextVar[str] = ContextVar("source_keyword", default="")

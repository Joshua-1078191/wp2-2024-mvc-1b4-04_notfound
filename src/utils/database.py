import sqlite3
from collections import namedtuple
from sqlite3 import Cursor, Connection

QueryParams = namedtuple('QueryParams', ['query', 'params'])


def connect_database(database_path: str) -> (Connection, Cursor):
    # Connect to database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row  # fetches data as a dictionary instead of list : [] -> {}

    return conn, cursor

def generate_query_params(**kwargs) -> QueryParams | None:
    query_arguments = []
    params = []

    if not kwargs:
        return None

    for arg in kwargs:
        if kwargs[arg] is not None:
            query_arguments.append(f"`{arg}`=?")
            params.append(kwargs[arg])

    query = str.join(", ", query_arguments)

    return QueryParams(query=query, params=params)
"""Database utility functions for SQLite connection management."""

import sqlite3
from contextlib import contextmanager
from decimal import Decimal

sqlite3.register_adapter(Decimal, str)


@contextmanager
def connect_to_db(path: str):
    """
    Context manager for connecting to a SQLite database.

    This function establishes a connection to a SQLite database at the
    given file path, configures the connection to return rows as
    `sqlite3.Row` objects (allowing dict-like access), and ensures that
    the transaction is properly committed or rolled back.

    Usage:
        with connect_to_db("example.db") as conn:
            cursor = conn.execute("SELECT * FROM my_table")

    Args:
        path (str): The file path to the SQLite database.

    Yields:
        sqlite3.Connection: An active SQLite connection object.

    Raises:
        Exception: Re-raises any exception encountered during database
            operations after rolling back the transaction.

    Behavior:
        - Commits the transaction if no exception occurs.
        - Rolls back the transaction if an exception is raised.
        - Always closes the connection upon exiting the context.
    """
    conn = sqlite3.connect(path)
    try:
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

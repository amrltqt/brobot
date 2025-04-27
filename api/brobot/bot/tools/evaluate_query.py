from io import StringIO
from textwrap import dedent

from rich.console import Console
from rich.table import Table

import duckdb
from agents import function_tool

connection = duckdb.connect(database=":memory:")

connection.execute(
    dedent(
        """
            CREATE TABLE students (
                id INTEGER,
                name VARCHAR,
                note INTEGER
            );
        """
    )
)

connection.execute(
    dedent(
        """            
            INSERT INTO students VALUES 
                (1, 'Alice', 7),
                (2, 'John', 6),
                (3, 'Charlie', 8);
        """
    )
)


@function_tool(name_override="evaluate_query")
async def evaluate_query(query: str) -> str:
    """
    Execute the query against the duckdb engine that expose the table of the exercise.

    Args:
        query (str): SQL query of the user

    Returns:
        str: the table representation of the result
    """
    result = connection.execute(query)
    columns = [col[0] for col in result.description]
    rows = result.fetchall()

    buffer = StringIO()
    buffered_console = Console(file=buffer, force_terminal=True)

    table = Table(title="Result table")

    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*[str(item) for item in row])

    buffered_console.print(table, highlight=False)

    return buffer.getvalue()

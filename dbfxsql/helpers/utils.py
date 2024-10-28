import types
from dbfxsql.constants import sample_commands
from prettytable import PrettyTable
from watchfiles import Change


def show_table(rows: list[dict]) -> None:
    """Displays a list of rows in a table format."""

    table = PrettyTable()

    table.field_names = rows[0].keys() if rows else []

    for row in rows:
        table.add_row([row[field] for field in table.field_names])

    print(table, end="\n\n")


def embed_examples(func: types.FunctionType) -> types.FunctionType:
    """Decorator to add docstrings to a function."""
    examples: str = """
    \n
    \b
    Examples:
    ---------
    """

    for command in sample_commands.DBF.keys():
        if func.__name__ in command:
            examples += "- " + sample_commands.DBF[command]

    for command in sample_commands.SQL.keys():
        if func.__name__ in command:
            examples += "\n    "
            examples += "- " + sample_commands.SQL[command]

    func.__doc__ += examples

    return func


def only_modified(change: Change, path: str) -> bool:
    allowed_extensions: tuple[str] = (".dbf", ".sql")

    return change == Change.modified and path.endswith(allowed_extensions)


def notify(operations: list, tables: list) -> None:
    for (insert, update, delete), table in zip(operations, tables):
        print(f"\nMake changes in: {table.source}")

        for row in insert:
            print(f"Insert row: {row["fields"]}")

        for row in update:
            print(f"Update row: {row["fields"]} with row_number {row["index"]}")

        for row in delete:
            print(f"Delete row with row_number {row["index"]}")
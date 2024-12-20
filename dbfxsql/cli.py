from .constants import config
from .models.order_commands import OrderCommands
from .modules import dbf_controller, sql_controller, sync_controller
from .helpers import utils

import click
import asyncio
from yaspin import yaspin


@click.group(cls=OrderCommands)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def cli():
    """This script helps with the initialization of the tool."""


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their types.",
    required=True,
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def create(rdbms: str, source: str, table: str | None, fields: tuple) -> None:
    """Create a DBF file/SQL file and table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    if "DBF" == engine.upper():
        dbf_controller.create_table(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.create_table(engine, source, table, fields)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their values.",
    required=True,
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def insert(rdbms: str, source: str, table: str | None, fields: tuple) -> None:
    """Insert a row into a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    if "DBF" == engine.upper():
        dbf_controller.insert_row(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.insert_row(engine, source, table, fields)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def read(
    rdbms: str,
    source: str,
    table: str | None,
    condition: tuple | None,
) -> None:
    """Read rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    rows: list = []

    if "DBF" == engine.upper():
        rows = dbf_controller.read_rows(engine, source, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        rows = sql_controller.read_rows(engine, source, table, condition)

    else:
        raise NotImplementedError

    utils.show_table(rows)


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their values.",
    required=True,
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
    required=True,
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def update(
    rdbms: str,
    source: str,
    table: str | None,
    fields: tuple,
    condition: tuple,
) -> None:
    """Update rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    if "DBF" == engine.upper():
        dbf_controller.update_rows(engine, source, fields, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.update_rows(engine, source, table, fields, condition)

    else:
        raise NotImplementedError()


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
    required=True,
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def delete(rdbms: str, source: str, table: str | None, condition: tuple) -> None:
    """Delete rows from an DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    if "DBF" == engine.upper():
        dbf_controller.delete_rows(engine, source, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.delete_rows(engine, source, table, condition)

    else:
        raise NotImplementedError()


@cli.command()
@click.option(
    "-r",
    "--rdbms",
    default="SQLite",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    default="",
)
@click.confirmation_option(
    prompt="Are you sure you want to drop?", help="Confirm the operation."
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def drop(rdbms: str, source: str, table: str | None) -> None:
    """Drop a DBF file/SQL file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}'.")

    if "DBF" == engine.upper():
        dbf_controller.drop_table(engine, source)

    elif not table and "SQLite" == rdbms:
        sql_controller.drop_database(engine, source)

    elif "SQLite" == rdbms:
        sql_controller.drop_table(engine, source, table)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-p",
    "--priority",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def migrate(priority: str) -> None:
    """
    Migrate data between DBF and SQL files.

    Expects a priority folder where the files will be migrated to the other
    and a list of extensions.
    """

    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            setup: dict = sync_controller.init()
            relations: list = setup["relations"]
            filenames: list = sync_controller.collect_files(setup, priority)

            spinner.text = "Migrating..."
            sync_controller.migrate(filenames, relations)

            spinner.ok("DONE")

        except KeyboardInterrupt:
            spinner.ok("END")


@cli.command()
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def sync():
    """Synchronize data between DBF and SQL files."""
    priority: str = "DBF"

    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            setup: dict = sync_controller.init()
            relations: list = setup["relations"]
            filenames: list = sync_controller.collect_files(setup, priority)

            spinner.text = "Migrating..."
            sync_controller.migrate(filenames, relations)

            spinner.text = "Listening..."
            asyncio.run(sync_controller.synchronize(setup, priority))

        except KeyboardInterrupt:
            spinner.ok("END")

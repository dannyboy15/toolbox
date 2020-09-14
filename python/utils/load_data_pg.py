from parsons import Table, Postgres

import click
import glob
import os
import re


def get_type(path):
    return (
        "file" if os.path.isfile(path) else
        "dir" if os.path.isdir(path) else ""
    )


def get_tablename(path):
    tablename = path_to_parts(path)[1]

    if not _is_valid_tablename(tablename):
        tablename = _format_tablename(tablename)

    return tablename


def path_to_parts(filename):
    dir, basename = os.path.split(filename)
    name, ext = os.path.splitext(basename)

    return dir, name, ext


def _is_valid_tablename(tablename):
    # https://www.postgresql.org/docs/9.1/sql-syntax-lexical.html
    # SQL identifiers and key words must begin with a letter (a-z, but also
    # letters with diacritical marks and non-Latin letters) or an underscore
    # (_). Subsequent characters in an identifier or key word can be letters,
    # underscores, digits (0-9), or dollar signs ($). Note that dollar signs
    # are not allowed in identifiers according to the letter of the SQL
    # standard, so their use might render applications less portable. The SQL
    # standard will not define a key word that contains digits or starts or
    # ends with an underscore, so identifiers of this form are safe against
    # possible conflict with future extensions of the standard.

    # https://stackoverflow.com/questions/8213127/maximum-characters-in-labels-table-names-columns-etc#comment77075321_8218026  # noqa

    # e.g. valid: _name_of_id_10, my_col, col$
    # e.g. invalid: 1_col, !name, name!, col name
    rgx = r"^[a-z_][a-z0-9_$]{,63}$"
    return re.fullmatch(rgx, tablename) is not None


def _format_tablename(tablename):
    # rgx_char_1 = r"[^a-z_]"

    # prefix with underscore if first char is digit
    # ignore invalid chars for now, that will be handled later
    if tablename[0].isdigit() or tablename[0] == "$":
        tablename = f"_{tablename}"

    # in regex \w is a-zA-Z0-9_]
    # test: a_1$!@#%^&*()+adsCAPITALf1_
    rgx_bad_chars = r"[^\w$]"
    tablename = re.sub(rgx_bad_chars, "_", tablename).lower()

    return tablename[:63]


@click.command()
@click.argument("path")
@click.option("--schema", default="public")
# @click.option("--tablename")
# ENH accept different files types
# ENH add dry-run option
# @click.option("--file-type", default="csv")
def main(path, schema):
    typ = get_type(path)

    print("Looking for files to import into postgres...")
    if typ == 'dir':
        path_ = os.path.join(path, "*.csv")
        files = glob.glob(path_)

    elif typ == 'file':
        files = [path]

    else:
        print("Invalid file or path")

    print(f"Found the following files: {files}")

    for file in files:
        print(f"Importing {file}...")
        tbl = Table.from_csv(file)
        tablename = f"{schema}.{get_tablename(file)}"

        tbl.to_postgres(tablename)

        sql = Postgres().create_statement(tbl, tablename)

        sql_ddl_file = f"sql/{get_tablename(file)}_ddl.sql"
        with open(sql_ddl_file, "w") as f:
            f.write(sql)

        print(
            f"File {file} imported into {tablename} and "
            f"DDL sql saved to {sql_ddl_file}.")


if __name__ == '__main__':
    main()

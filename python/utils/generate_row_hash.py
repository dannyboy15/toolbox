from parsons import Redshift

import click


DEFAULTS = {

}


def get_columns(table_name=None, lst=None):
    if not table_name and not lst:
        raise RuntimeError(
            "Must provide either table_name or a list of columns.")

    if table_name:
        rs = Redshift()

        return rs.get_columns(*(table_name.split(".")))
    else:
        return {c: {'data_type': "character varying"} for c in lst}


@click.command()
@click.argument("table")
def main(table):
    # TODO fix handling of passing a list
    # TODO fix to run local, no call to rs
    cols = get_columns(table)

    sql = (
        "md5(\n  " +
        "\n  || ".join([
            f"coalesce({col}::varchar, '')"
            for col in cols
        ]) +
        "\n)"
    )

    print(sql)
    return sql


if __name__ == "__main__":
    main()

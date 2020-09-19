# local imports assuming toolboox/python/ is in your python path
from python.utils.utils import github_url_to_raw_text_url
from python.utils.templates import read_file
from python.civis_utils.environment import setup_env_for_parsons
from civis_jobs.utils import (
    upload_dict_as_civis_script_outputs, upload_file_as_civis_script_outputs,
    timeit)

from parsons import Redshift

import logging
import os
import requests


# Set up logging
logger = logging.getLogger()

# # Log to standard output
# sys_hdlr = logging.StreamHandler()
# sys_hdlr.setFormatter(logging.Formatter(
#     '%(name)s pid:%(process)d %(levelname)s %(message)s'))
# sys_hdlr.setLevel("INFO")
# logger.addHandler(sys_hdlr)
#
# # Set Level to INFO for all logging
# logger.setLevel("INFO")


def save_file_from_url(url, auth=None, dir="/temp/files"):
    res = requests.get(url, auth=auth)

    res.raise_for_status()

    # create the folder if it doesn't exist
    os.makedirs(dir, exist_ok=True)
    filename = url.split("/")[-1]
    full_path = f"{dir}/{filename}"

    with open(full_path, "w") as fp:
        fp.write(res.text)

    return full_path


def parse_str_as_variables(var_str):
    if not var_str:
        return {}

    key_val_list = var_str.split()

    vars = {}
    for key_val in key_val_list:
        try:
            key, val = key_val.split("=")

            # remove any quotes, whether single or double
            if val[0] == '"':
                val = val.strip('"')
            elif val[0] == "'":
                val = val.strip("'")

            vars[key] = val
        except Exception:
            raise ValueError("Invalid variable format.")

    return vars


def run_query(sql):
    logging.info(f"Connecting to {os.environ['REDSHIFT_NAME']}")
    rs = Redshift()

    @timeit
    def run(rs, sql):
        return rs.query(sql)

    logging.info("Running query")
    logging.info(sql)
    return run(rs, sql)


def main():
    setup_env_for_parsons()

    url = os.environ["URL"]
    auth_user = os.getenv("AUTH_USERNAME")
    auth_pass = os.getenv("AUTH_PASSWORD")
    var_string = os.getenv("VARIABLES")

    url = github_url_to_raw_text_url(url)

    variables = parse_str_as_variables(var_string)

    auth = (auth_user, auth_pass) if auth_user else None
    path = save_file_from_url(url, auth=auth)

    sql = read_file(path)

    sql = sql.format(**variables)

    ptable, time_stats = run_query(sql)
    logging.info("Query succeeded")

    # TODO: Add results.csv data points (e.g. num_columns, num_rows)
    upload_dict_as_civis_script_outputs(time_stats["runtime"], "SQL Runtime")

    if ptable:
        logging.info("Exporting result as a csv")
        filename = ptable.to_csv("resutls.csv")
        upload_file_as_civis_script_outputs(filename)


if __name__ == '__main__':
    main()

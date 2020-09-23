import civis
import logging
import os
import json


def upload_file_as_civis_script_outputs(filename, civis_job_id=None,
                                        civis_run_id=None):
    """Upload a file as output to a Civis Script.

    Currently only supports container scripts. _Note: The scripts must be
    running when this function is called._

    `Args:`
        civis_job_id: int
            The job id for a Civis container script.
        civis_run_id: int
            The run id for a Civis container script run.
    """
    job_id = civis_job_id or os.getenv("CIVIS_JOB_ID")
    run_id = civis_run_id or os.getenv("CIVIS_RUN_ID")

    if not (job_id and run_id):
        print("Invalid job_id/run_id. Did not upload the file.")

    with open(filename, "r") as f:
        file_id = civis.io.file_to_civis(f, filename)

    client = civis.APIClient()
    client.scripts.post_containers_runs_outputs(
        job_id, run_id, 'File', file_id)


def upload_logs_as_civis_script_outputs(lgr):
    """Upload the logs files as outputs to a Civis Script.

    If the script is running locally, then the function does nothing.

    `Args:`
        lgr: logging.Logger
            The logger object with file handlers.
    """
    for handle in lgr.handlers:
        if isinstance(handle, logging.FileHandler):
            log_file = handle.baseFilename

            upload_file_as_civis_script_outputs(log_file)


def upload_dict_as_civis_script_outputs(data, output_name="", job_id=None,
                                        run_id=None):
    """Upload the dict as outputs to a Civis Script.

    If the script is running locally, then the function does nothing.

    `Args:`
        data: dict or any
            The values to upload as ouptuts.
        output_name:
            If data is not a dict, this will be the name associated with the
            output data.
        civis_job_id: int
            The job id for a Civis container script.
        civis_run_id: int
            The run id for a Civis container script run.
    """
    job_id = job_id or os.getenv("CIVIS_JOB_ID")
    run_id = run_id or os.getenv("CIVIS_RUN_ID")

    # Check again to see if there were in the environment
    if not job_id and not run_id:
        return

    if isinstance(data, dict):
        json_outputs = [
            {"value_str": json.dumps(val), "name": key}
            for key, val in data.items()
        ]

    else:
        json_outputs = [
            {"value_str": json.dumps(data), "name": output_name}
        ]

    client = civis.APIClient()
    for output in json_outputs:
        # save output to civis
        json_value_object = client.json_values.post(**output)

        # post it as a run output
        client.scripts.post_containers_runs_outputs(
            job_id, run_id, 'JSONValue', json_value_object["id"])


def wait_for_script(script_type,
                    job_id,
                    run_id,
                    client=None,
                    polling_interval=10,
                    return_future=False):
    """
    Wait for a Civis script to finish.

    If the script fails, this function will raise an error. Alternateively,
    you can pass `return_future=True` and return the future.

    `Args:`
        script_type: str
            The type of Civis script it is. One of 'custom', 'python', 'r',
            'sql', 'container'.
        job_id: int
            The id of the script.
        run_id: int
            The id of the run.
        client: civis.APIClient
            (Optional) A civis client to use to run and wait for the script.
        polling_interval: int
            (Optional) The interval to wait before checking agian if the script
            has completed.
        return_future: bool
            (Optional) If `True` returns a future insead of the result of the
            of the script. Defaults to `False`.

    `Returns:`
        The result of the script.
    """
    script_types = {
        "custom": client.scripts.get_custom_runs,
        "python": client.scripts.get_python3_runs,
        "r": client.scripts.get_r_runs,
        "sql": client.scripts.get_sql_runs,
        "container": client.scripts.get_containers_runs,
        "workflow": client.workflows.get_executions,
        "imports": client.imports.get_files_runs,
    }

    client = client or civis.APIClient()

    script = client.search.list(query=job_id, type=script_type)

    name = script["results"][0]["name"]

    logging.info(
        f"Waiting for {name} (job: {job_id}, run: {run_id}) to finish...")

    # uses a future object to ensure this script fails if the child fails
    poller = script_types[script_type]
    poller_args = job_id, run_id

    job_future = civis.futures.CivisFuture(poller, poller_args,
                                           polling_interval)

    if return_future:
        return job_future

    return job_future.result()

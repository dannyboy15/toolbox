import civis
import logging


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

from .utils import wait_for_script

from parsons import Slack

import os
import civis


def get_last_run_id(job_id):
    client = civis.APIClient()
    script = client.jobs.get(job_id)

    if not script["last_run"]:
        raise RuntimeError("The script hasn't been run yet.")

    return script["last_run"]["id"]


def get_job_status(job_id, run_id=None):
    client = civis.APIClient()

    if run_id:
        script = client.jobs.get_runs(job_id, run_id)

        return script["state"]
    else:
        script = client.jobs.get(job_id)

        return script["last_run"]["state"]


def get_job_name(id):
    client = civis.APIClient()

    return client.jobs.get(id)['name']


def main():

    DEFAULT_MESSAGE = (
        "The script *{name}* finished running with a status of {status}. "
        "(script_id: {script_id}, run_id: {run_id})")

    script_type = os.environ["SCRIPT_TYPE"]
    job_id = int(os.environ["JOB_ID"])
    run_id = int(os.getenv("RUN_ID", get_last_run_id(job_id)))

    channel = os.environ["SLACK_CHANNEL"]
    message = os.getenv("SLACK_MESSAGE", DEFAULT_MESSAGE)

    slack = Slack(api_key=os.environ["SLACK_API_PASSWORD"])

    print(f"Waiting for {job_id}, {run_id} to finish....")
    try:
        wait_for_script(script_type, job_id, run_id)
    except Exception:
        pass

    status = get_job_status(job_id, run_id)
    name = get_job_name(job_id)
    print(f"Script finished with status of {status}")

    message = message.format(name=name,
                             status=status,
                             script_id=job_id,
                             run_id=run_id)
    slack.message_channel(channel, message)


if __name__ == '__main__':
    main()

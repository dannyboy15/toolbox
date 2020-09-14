import os


def set_env_var(name, value, overwrite=False):
    """
    Set an environment variable to a value.

    `Args:`
        name: str
            Name of the env var
        value: str
            New value for the env var
        overwrite: bool
            Whether to set the env var even if it already exists
    """
    # Do nothing if we don"t have a value
    if not value:
        return

    # Do nothing if env var already exists
    if os.environ.get(name) and not overwrite:
        return

    os.environ[name] = value


def setup_env_for_parsons(redshift_parameter="REDSHIFT",
                          aws_parameter="AWS",
                          creds=[]):
    """
    Sets up environment variables commonly used in parsons scripts.

    Call this at the beginning of your script.

    `Args:`
        redshift_parameter: str
            Name of the Civis script parameter holding Redshift credentials.
            This parameter should be of type "database (2 dropdown)" in Civis.
        aws_parameter: str
            Name of the Civis script parameter holding AWS credentials.
        creds: list
            Arbitrary arguments for which to remove the '_PASSWORD' suffix.
    """

    env = os.environ

    # Redshift setup

    set_env_var("REDSHIFT_PORT", "5432")
    set_env_var("REDSHIFT_DB", "dev")
    set_env_var("REDSHIFT_ID", env.get(f"{redshift_parameter}_ID"))
    set_env_var("REDSHIFT_NAME", env.get(f"{redshift_parameter}_NAME"))
    set_env_var("REDSHIFT_HOST", env.get(f"{redshift_parameter}_HOST"))
    set_env_var("REDSHIFT_USERNAME",
                env.get(f"{redshift_parameter}_CREDENTIAL_USERNAME"))
    set_env_var("REDSHIFT_PASSWORD",
                env.get(f"{redshift_parameter}_CREDENTIAL_PASSWORD"))

    # AWS setup

    set_env_var("S3_TEMP_BUCKET", "tmp-bucket")
    set_env_var("AWS_ACCESS_KEY_ID", env.get(f"{aws_parameter}_USERNAME"))
    set_env_var("AWS_SECRET_ACCESS_KEY", env.get(f"{aws_parameter}_PASSWORD"))

    for cred in creds:
        set_env_var(cred.replace("_PASSWORD", ""), env.get(cred))

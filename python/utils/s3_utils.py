from parsons import S3, Table


def is_file_empty_or_invalid(bucket, key_dict):
    """Check a file to make sure it has data and is csv-formatted correctly.

    `Args:`
        bucket: str
            The bucket where the keys were obtained.
        key_dict: dict
            The dict with stats for a key.

    `Returns:`
        `bool` or `str`: If valid returns `False`, otherwise "invalid"
        or "empty"
    """
    # TODO: May want to break this up into 2 functions to we can
    # get separate lists.

    filename = S3().get_file(bucket, key_dict["Key"])

    # Check that it's valid
    try:
        ptable = Table.from_csv(filename)
    except ValueError as e:
        if "Could not create Table" in str(e):
            return "invalid"

    # Check that it's not empty
    if ptable.num_rows == 0:
        return "empty"

    return False

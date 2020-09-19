import hashlib
import inspect
import os
import secrets
import string


def md5_hash(string):
    """Return the md5 hash of a string.

    `Args:`
        string: str
            The string to hash
    `Returns:`
        str
            The hashed string.
    """
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def get_my_dirpath():
    """Return the /full/path/to/calling/script"""
    # based on https://stackoverflow.com/a/55469882
    # get the caller's stack frame and extract its file path
    frame_info = inspect.stack()[1]
    filepath = frame_info.filename
    # drop the reference to the stack frame to avoid reference cycles
    del frame_info

    # make the path absolute (optional)
    filepath = os.path.dirname(os.path.abspath(filepath))
    return filepath


def generate_password(length=12, req_lower=True, req_upper=True,
                      req_digit=True, req_char=True, valid_chars="!$%~#&+"):
    """Generate a basic password.

        `Args:`
            length: int
                The length of the password.
            req_lower: bool
                If ``True``, ensures the password contains a lowercase letter.
                Defaults to ``True``.
            req_upper: bool
                If ``True``, ensures the password contains an uppercase letter.
                Defaults to ``True``.
            req_digit: bool
                If ``True``, ensures the password contains a digit. Defaults
                to ``True``.
            req_char:
                If ``True``, ensures the password contains a non-word
                character. Defaults to ``True``.
            valid_chars: string
                A list of valid characters to include in the password.
        `Returns:`
            str
                The generated password.
    """
    alphabet = string.ascii_letters + string.digits + valid_chars

    tests = []

    if req_lower:
        tests.append(lambda pwd: any(c.islower() for c in pwd))

    if req_upper:
        tests.append(lambda pwd: any(c.isupper() for c in pwd))

    if req_digit:
        tests.append(lambda pwd: sum(c.isdigit() for c in pwd) >= 3)

    if req_char:
        tests.append(lambda pwd: any(c in valid_chars for c in pwd))

    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (all(test(password) for test in tests)):
            break
    return password


def seconds_to_text(secs, as_time_str=False):
    """Format seconds into their time parts.

    `Args:`
        secs: int
            The seconds to format.
        as_time_str: bool
            If true, returns the seconds represented as human readable (e.g.
            1 minute 20 seconds). Otherwise used time format. Defaults to
            False.
    `Returns:`
        str
            The formatted seconds.
    """
    # Adapted from
    # https://gist.github.com/Highstaker/280a09591df4a5fb1363b0bbaf858f0d
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60

    days_text = "day{}".format("s" if days != 1 else "")
    hours_text = "hour{}".format("s" if hours != 1 else "")
    minutes_text = "minute{}".format("s" if minutes != 1 else "")
    seconds_text = "second{}".format("s" if seconds != 1 else "")

    if as_time_str:
        result = ":".join(filter(lambda x: bool(x), [
            "{0} {1}".format(int(days), days_text) if days else "",
            "{0:02d}".format(int(hours)) if hours else "",
            "{0:02d}".format(int(minutes)) if minutes else "00",
            "{0:02.4f}".format(seconds) if seconds else "00"
        ]))
    else:
        result = ", ".join(filter(lambda x: bool(x), [
            "{0} {1}".format(int(days), days_text) if days else "",
            "{0} {1}".format(int(hours), hours_text) if hours else "",
            "{0} {1}".format(int(minutes), minutes_text) if minutes else "",
            "{0:.4f} {1}".format(seconds, seconds_text) if seconds else ""
        ]))
    return result


def github_url_to_raw_text_url(url):
    """Return the raw text url for the GitHub resource.

    `Args:`
        url: str
            The url for the GitHub resource.
    `Return:`
        str
            The raw text url for the GitHub resource.
    """
    if "gist." in url:
        url = f"{url}/raw"

    elif "github.com" in url:
        # raw content is hosted on a different host url
        url = url.replace("github.com", "raw.githubusercontent.com")

        # raw content url doesn't contain 'blob'
        url = url.replace("blob/", "")

    return url

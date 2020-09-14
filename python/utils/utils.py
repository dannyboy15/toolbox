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

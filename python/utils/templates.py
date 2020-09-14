from jinja2 import Template
from jinja2.utils import concat


TMPL_ENVS = {
    "sql": {
        "block_start_string": "-- {%",
        "block_end_string": "%}",
    },
    "sql-mlc": {
        "block_start_string": "/* {%",
        "block_end_string": "%} */",
    },
}


def read_file(path):
    with open(path, "r") as fp:
        return fp.read()


def template_blocks_to_dict(path, vars=None, use_env=None, custom_env=None):
    """
    Return a dictionary of blocks from a template (based on jinja2).
    Example:
        `queries.sql`::
            /* {% block query_1 %} */
            select * from schema.table
            /* {% endblock query_1 %} */
            /* {% block query_2 %} */
            select * from schema.table
            join schema.other_table using({{id}})
            /* {% endblock query_2 %} */
        .. code-block:: python
            >>> template_blocks_to_dict(
                "queries.sql", {"id": "join_id"}, "sql-mlc")
            {'query_1': 'select * from schema.table', 'query_2': 'select * from
             schema.table\\njoin schema.other_table using(join_id)'}

    `Args:`
        path: str
            The path to the file that contains the template blocks.
        vars: dict
            Dictionary of variables to pass to the template. Any variables not
            supplied will have not text output in the resulting dictionary.
            Note: Within the jinja2 template, varables use two sets of
            brackets, e.g. {{ var_name }}
        use_env: str
            Use a custom predefined set of start and end block strings.
            `sql`: `-- {%` and `%}`
            `sql-mlc`: `/* {%` and `%} */`
        custom_env: dict
            The custom environment to use. If this is provided, `use_env` is
            ignored. For more information on possible initialization parameters
            see jinja2 `documentation
            <https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment>`_
    `Returns:`
        dict
            Dictionary of blocks names and their contents.
    """  # noqa
    env = custom_env or TMPL_ENVS.get(use_env) or {}

    sql = read_file(path)
    template = Template(sql, **env)
    context = template.new_context(vars)

    # TODO: add support for returning functions that could be rendered

    data = {name: concat(block_func(context)).strip()
            for name, block_func in template.blocks.items()}

    return data


def render_template(path, vars=None, is_tmpl_str=False, use_env=None,
                    custom_env=None):
    """Render template (based on jinja2).
    `Args:`
        path: str
            The path to a templated file or a templated string to render.
        vars: dict
            Dictionary of variables to pass to the template. Any variables not
            supplied will have not text output in the resulting dictionary.
            Note: Within the jinja2 template, varables use two sets of
            brackets, e.g. ``{{ var_name }}``.
        is_tmpl_str: bool
            If `True`, ``path`` is interpretted as a template string instead
            of path to a templated file. Defaults to `False`.
        use_env: str
            Use a custom predefined set of start and end block strings.
            `sql`: `-- {%` and `%}`
            `sql-mlc`: `/* {%` and `%} */`
        custom_env: dict
            The custom environment to use. If this is provided, `use_env` is
            ignored. For more information on possible initialization parameters
            see jinja2 `documentation
            <https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment>`_
    `Returns:`
        str
            The render template.
    """
    env = custom_env or TMPL_ENVS.get(use_env) or {}
    vars = vars or {}

    sql = path if is_tmpl_str else read_file(path)

    template = Template(sql, **env)
    data = template.render(vars)

    return data

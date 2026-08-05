from pallets_sphinx_themes import ProjectLink, get_version

project = "Flask-BabelPlus"
copyright = "2016-2026, Peter Justin, Serge S. Koval, Armin Ronacher"
author = "Peter Justin, Serge S. Koval, Armin Ronacher"
release, version = get_version("Flask-BabelPlus")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "sphinxcontrib.log_cabinet",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_preserve_defaults = True
extlinks = {
    "issue": ("https://github.com/sh4nks/flask-BabelPlus/issues/%s", "#%s"),
    "pr": ("https://github.com/sh4nks/flask-BabelPlus/pull/%s", "#%s"),
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
}

issues_github_path = "sh4nks/flask-BabelPlus"


html_theme = "flask"
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.python.org/pypi/Flask-BabelPlus/"),
        ProjectLink("Source Code", "https://github.com/sh4nks/Flask-BabelPlus"),
        ProjectLink(
            "Issue Tracker", "https://github.com/sh4nks/Flask-BabelPlus/issues/"
        ),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
html_favicon = "_static/flask-babel.png"
html_logo = "_static/flask-babel.png"
html_title = f"Flask-BabelPlus Documentation ({version})"
html_show_sourcelink = False

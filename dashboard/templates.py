"""Admin page HTML templates."""

BASE_TEMPLATE = """
<head>
    <title>MyStuff Admin Dashboard</title>
</head>
<body>
    {body}
</body>
"""

SIGN_IN_PAGE = BASE_TEMPLATE.format(body="""
Hello, world!
""")

HOME_PAGE = BASE_TEMPLATE.format(body="""

""")

USER_PAGE = BASE_TEMPLATE.format(body="""

""")

STUFF_PAGE = BASE_TEMPLATE.format(body="""

""")

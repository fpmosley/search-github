from setuptools import setup

setup(
    name="github_query",
    version="0.1",
    py_modules=["github_query"],
    include_package_data=True,
    install_requires=[
        "click",
        "requests"
    ],
    entry_points="""
        [console_scripts]
        github_query=github_query:cli
    """,
)

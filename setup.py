from setuptools import setup

setup(
    name="ezrepo",
    version="1.0.0",
    description="GitHub repository creation tool",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["ezrepo"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "ezrepo=ezrepo:main",
        ],
    },
) 
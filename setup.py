from setuptools import setup, find_packages

setup(
    name="ezrepo",
    version="1.0.0",
    description="GitHub repository creation tool",
    author="Ahmed Wagdy",
    author_email="ahmedwagdymohy@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=["ezrepo"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "ezrepo=ezrepo:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 
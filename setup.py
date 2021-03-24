import setuptools

# include additional packages as well - requests , tabulate , json

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easySQLiteV2", # Replace with your own username
    version="0.11",
    author="Harsh Native",
    author_email="Harshnative@gmail.com",
    description="This module to used to manage sqlite database with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshnative/easySQLite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
   'tabulate',
   'cryptography',
   'onetimepad',
    ],

    python_requires='>=3.6',
)
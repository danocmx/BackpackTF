import setuptools


with open("README.md", "r") as fh:
    README = fh.read()

setuptools.setup(
    name="BackpackTF",
    version="1.0.0",
    author="danocmx",
    description="Backpack.tf api wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/danocmx/BackpackTF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

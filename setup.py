import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="r2d7py",
    version="0.0.1",
    author="Michael Dubno",
    author_email="michael@dubno.com",
    description="R2D7 shade controller over Ethernet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dubnom/r2d7py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

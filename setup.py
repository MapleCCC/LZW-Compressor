import setuptools

from LZW import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LZW-Compressor",
    author="MapleCCC",
    author_email="littlelittlemaple@gmail.com",
    description="A compression and decompression program for LZW archive format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapleCCC/LZW-Compressor",
    version=__version__,
    packages=setuptools.find_packages(),
    license="WTFPL 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=open("requirements.txt", "r").read().splitlines(),
    entry_points={"console_scripts": ["lzw=LZW.__main__:main",]},
)

from setuptools import setup, find_packages

setup(
    name="axiomtradeapi",
    version="0.1.0",
    description="A Python client for the AxiomTrade API.",
    author="ChipaDevTeam",
    author_email="",
    url="https://github.com/ChipaDevTeam/AxiomTradeAPI-py",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

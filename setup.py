from setuptools import setup, find_packages

setup(
    name="ENERES-100-HW-Libraries",
    version="0.1.0",
    description="Custom Unum Fork for ENERES 100",
    author="Serrindipity",
    author_email="jon_quitoriano@berkeley.edu",
    url="https://github.com/Serrindipity/ENERES-100-HW-Libraries",
    packages=find_packages(),
    install_requires=[
        "eneres_100_unum@https://github.com/Serrindipity/ENERES-100-Unum.git"
    ]
)
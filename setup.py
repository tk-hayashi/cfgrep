from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cfgrep",
    version="1.0.1",
    description="cfgrep is Cisco Config Context-aware Check grep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="toshayas",
    author_email='toshayas@cisco.com',
    url='https://github.com/tk-hayashi/cfgrep',
    packages=find_packages(),
    install_requires=["wheel",
                      "ciscoconfparse",
                      "netaddr",
                      "docopt"],
    entry_points={
        "console_scripts": [
            "cfgrep = bin.main:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)

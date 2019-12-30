from setuptools import setup, find_packages

setup(
    name="cfgrep",
    version="1.0.0",
    description="fgrep(c4grep, ccccgrep) is Cisco Config Context-aware Check grep",
    author="toshayas",
    author_email='toshayas@cisco.com',
    url='https://github.com/tk-hayashi/cfgrep',
    packages=find_packages(),
    install_requires=["ciscoconfparse",
                      "netaddr",
                      "docopt"],
    entry_points={
        "console_scripts": [
            "cfgrep = bin.main:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)

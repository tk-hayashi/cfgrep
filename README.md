# cfgrep

cfgrep(c4grep, ccccgrep) is Cisco-like Config Context-aware Check grep

[![Downloads](https://pepy.tech/badge/cfgrep)](https://pepy.tech/project/cfgrep)
[![Downloads](https://pepy.tech/badge/cfgrep/month)](https://pepy.tech/project/cfgrep/month)
[![Downloads](https://pepy.tech/badge/cfgrep/week)](https://pepy.tech/project/cfgrep/week)
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/tk-hayashi/cfgrep)

## Installing

pip from PyPI
```
pip install cfgrep
```

, or pip from github
```
pip install wheel git+https://github.com/tk-hayashi/cfgrep
```

, or running setup.py

```
git clone https://github.com/tk-hayashi/cfgrep
cd cfgrep
python setup.py install
```


## Usage
Regular expressions can be used as PATTERN similar to grep.

```bash

 > cfgrep -h
Overview:
    cfgrep(c4grep, ccccgrep) is Cisco Config Context-aware Check grep

Usage:
    cfgrep <PATTERN> <FILE> [-i | --interface] [-b | --bgp] [-d | --description]
    cfgrep -h | --help

Options:
    -i, --interface    interface mode
    -b, --bgp          bgp mode
    -d, --description  to specify PATTERN by description
    -h, --help         display help
```

### options
See [examples-xr.md](https://github.com/tk-hayashi/cfgrep/blob/master/examples-xr.md) and [examples-ios.md](https://github.com/tk-hayashi/cfgrep/blob/master/examples-ios.md)  for details of options

|  option  |  description  |
| ---- | ---- |
|  -i  |  Interface mode. To display a config related to ipv4 and ipv6 address of the interfaces. |
|  -b  |  BGP mode. To display a config related to route-policy(route-map) and bgp-group of the neighbors. |
|  -d  |  Description mode. To use a parent indent of description as PATTERN. |

## Authors

* **Toshiki Hayashi** - *Initial work*

## License

This project is licensed under the Apache License - see the [LICENSE](https://github.com/tk-hayashi/cfgrep/blob/master/LICENSE) file for details

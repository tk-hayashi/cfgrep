# cfgrep

cfgrep(c4grep, ccccgrep) is Cisco Config Context-aware Check grep

## Installing
```
pip install cfgrep
```

or

```
pip install wheel git+https://github.com/tk-hayashi/cfgrep
```

## Usage
Regular expressions can be used in PATTERN like grep.

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
|  -d  |  Description mode. To use a indent parent of description as PATTERN. |

## Authors

* **Toshiki Hayashi** - *Initial work*

## License

This project is licensed under the Apache License - see the [LICENSE](https://github.com/tk-hayashi/cfgrep/blob/master/LICENSE) file for details

"""Overview:
    cfgrep(c4grep, ccccgrep) is Cisco Config Context-aware Check grep

Usage:
    cfgrep <PATTERN> <FILE> [-i | --interface] [-b | --bgp] [-d | --description]
    cfgrep -h | --help

Options:
    -i, --interface    interface mode
    -b, --bgp          bgp mode
    -d, --description  to specify PATTERN by description
    -h, --help         display help
"""

from cfgrep.cfgrep import Cfgrep
from docopt import docopt


def main():
    args = docopt(__doc__)

    cfgrep = Cfgrep(file_name=args['<FILE>'])
    cfgrep.config_parse(pattern=args['<PATTERN>'],
                        mode_interface=args['--interface'],
                        mode_bgp_neighbor=args['--bgp'],
                        mode_description=args['--description']
                        )
    return


if __name__ == '__main__':
    main()

import re
from collections import defaultdict
from ciscoconfparse import CiscoConfParse
from netaddr import IPAddress, IPNetwork


class Cfgrep:
    def __init__(self, file_name):
        self.parse = CiscoConfParse(file_name)
        self.os = 'xr'
        self.__check_os()

    def __check_os(self):
        xr = self.parse.find_lines('!!\s+IOS\sXR\sConfiguration')
        if len(xr):
            self.os = 'xr'
            return self.os

        ios = self.parse.find_lines('^version\s\d')
        if len(ios):
            self.os = 'ios'
            return self.os

    @staticmethod
    def __print_str_list(str_list):
        for str_print in str_list:
            print(str_print)
        return

    @staticmethod
    def __print_notice(string):
        print('!')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('! {}'.format(string))
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    @staticmethod
    def __append_ip_address(address, prefix_length, line_num,
                            ip_list, ip_list_num):
        __network = IPNetwork(address + '/' + str(prefix_length))
        ip_list.append(__network)
        ip_list_num.append(line_num)
        return ip_list, ip_list_num

    def __search_interface_ip_address(self, line,
                                      ip_v4_list, ip_v4_line_num_list,
                                      ip_v6_list, ip_v6_line_num_list):
        __address_match = re.match(r'^\s+ip(v4)?\saddress\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)', line.text)
        if __address_match:
            __host_address = __address_match.group(2)
            prefix_length = IPAddress(__address_match.group(3)).netmask_bits()
            self.__append_ip_address(__host_address, prefix_length, line.linenum,
                                     ip_v4_list, ip_v4_line_num_list)

        __address_match = re.match(r'^\s+ipv6\saddress\s([\w:]*::[\w:]*)/(\d+)', line.text)
        if __address_match:
            __host_address = __address_match.group(1)
            prefix_length = __address_match.group(2)
            self.__append_ip_address(__host_address, prefix_length, line.linenum,
                                     ip_v6_list, ip_v6_line_num_list)

        return ip_v4_list, ip_v4_line_num_list, ip_v6_list, ip_v6_line_num_list

    @staticmethod
    def __append_bgp(regexp, line, bgp_list):
        __bgp_match = re.match(regexp, line.text)
        if __bgp_match:
            bgp_list.append(__bgp_match.group(1))
        return bgp_list

    def __search_bgp(self, line, bgp_policy_list, bgp_group_list):
        if self.os == 'xr':
            regexp = re.compile(r'^\s+route-policy\s(\S+)\s(in|out)')
            self.__append_bgp(regexp, line, bgp_policy_list)
            regexp = re.compile(r'^\s+default-originate\sroute-policy\s(\S+)$')
            self.__append_bgp(regexp, line, bgp_policy_list)
            regexp = re.compile(r'^\s+use\sneighbor-group\s(\S+)')
            self.__append_bgp(regexp, line, bgp_group_list)
        else:
            regexp = re.compile(r'^\s+neighbor\s\S+\sroute-map\s(\S+)\s(in|out)')
            self.__append_bgp(regexp, line, bgp_policy_list)
            regexp = re.compile(r'^\s+neighbor\s\S+\sdefault-originate\sroute-map\s(\S+)$')
            self.__append_bgp(regexp, line, bgp_policy_list)
            regexp = re.compile(r'^\s+neighbor\s\S+\speer-group\s(\S+)$')
            self.__append_bgp(regexp, line, bgp_group_list)

        return bgp_policy_list, bgp_group_list

    def __print_ios_neighbor(self, string, result_str=None):
        __count = True
        find_list = self.parse.find_objects(r'^\s+neighbor\s{}\s'.format(string))
        for find in find_list:
            if '  neighbor' in find.text and __count:
                if result_str:
                    result_str.append(find.parent.text)
                else:
                    print(result_str.append(find.parent.text))
                __count = False

            if result_str:
                result_str.append(find.text)
            else:
                print(find.text)

    def __print_interface_ip_address(self, ip_list, ip_list_num,
                                     regexp_parse, regexp,
                                     string):
        if not len(ip_list):
            return

        __target_addresses = []
        __addresses_line = self.parse.find_objects(regexp_parse)
        for network in ip_list:
            for address_line in __addresses_line:
                address_match = re.findall(regexp, address_line.text)
                for address in address_match:
                    if IPAddress(address) in network and address_line.linenum not in ip_list_num:
                        __target_addresses.append(address_line.text)

        if len(__target_addresses):
            self.__print_notice(string)
            for target_address in set(__target_addresses):
                self.config_parse(target_address)

    def config_parse(self, pattern,
                     mode_interface=False,
                     mode_bgp_neighbor=False,
                     mode_description=False):
        option_dict = defaultdict(list)
        old_line_num = -1
        result_str = []

        def __recursive_parent(__line):
            parent = __line.parent
            if parent.linenum != __line.linenum:
                __recursive_parent(parent)
                result_str.append(parent.text)
            else:
                result_str.append('!')
            return

        def __recursive_child(__line):
            if mode_bgp_neighbor and self.os == 'ios':
                self.__search_bgp(__line, option_dict['bgp_policy'], option_dict['bgp_group'])

            for __child in __line.children:
                result_str.append(__child.text)

                if mode_interface:
                    self.__search_interface_ip_address(__child,
                                                       option_dict['ip_v4'], option_dict['ip_v4_line_num'],
                                                       option_dict['ip_v6'], option_dict['ip_v6_line_num'])

                # ios-xr (ios has no grandchild)
                if mode_bgp_neighbor:
                    self.__search_bgp(__child, option_dict['bgp_policy'], option_dict['bgp_group'])

                __recursive_child(__child)
            return

        originals = self.parse.find_objects(pattern)
        for original in originals:
            """
             description mode
            """
            if mode_description:
                if 'description' not in original.text:
                    continue
                # case of ios
                neighbor_address = re.match(r'^\s+neighbor\s(\d+\.\d+\.\d+\.\d+|[\w:]+::[\w:]*)\sdescription\s',
                                            original.text)
                if neighbor_address:
                    result_str.append('!')
                    result_str.append(original.parent.text)
                    self.__print_ios_neighbor(neighbor_address.group(1), result_str)
                    continue

                original = original.parent
                # omit duplications
                if original.linenum == old_line_num:
                    continue
                old_line_num = original.linenum

            __recursive_parent(original)
            result_str.append(original.text)
            __recursive_child(original)

        self.__print_str_list(result_str)

        regexp_parse = re.compile(r'\s(\d+\.\d+\.\d+\.\d+)(\s|/|$)')
        regexp = re.compile(r'\d+\.\d+\.\d+\.\d+')
        self.__print_interface_ip_address(option_dict['ip_v4'], option_dict['ip_v4_line_num'],
                                          regexp_parse, regexp,
                                          'ipv4 address search')

        regexp_parse = re.compile(r'\s([\w:]*::[\w:]*)(\s|/|$)')
        regexp = re.compile(r'[\w:]*::[\w:]*')
        self.__print_interface_ip_address(option_dict['ip_v6'], option_dict['ip_v6_line_num'],
                                          regexp_parse, regexp,
                                          'ipv6 address search')

        if len(option_dict['bgp_policy']):
            if self.os == 'xr':
                self.__print_notice('route-policy search')
                for bgp_policy in set(option_dict['bgp_policy']):
                    self.config_parse(r'^route-policy\s{}(\s|$)'.format(bgp_policy))
                    print('end-policy')
            else:
                self.__print_notice('route-map search')
                for bgp_policy in set(option_dict['bgp_policy']):
                    self.config_parse(r'^route-map\s{}\s'.format(bgp_policy))

        if len(option_dict['bgp_group']):
            self.__print_notice('neighbor-group search')
            if self.os == 'xr':
                for bgp_group in set(option_dict['bgp_group']):
                    self.config_parse(r'^\s+neighbor-group\s{}(\s|$)'.format(bgp_group), mode_bgp_neighbor=True)
            else:
                for bgp_group in set(option_dict['bgp_group']):
                    # print router bgp <asn>
                    neighbor_group_list = self.parse.find_objects(r'^\s+neighbor\s{}\speer-group'.format(bgp_group))
                    for neighbor_group in neighbor_group_list:
                        print(neighbor_group.parent.text)
                    self.__print_ios_neighbor(bgp_group)

        return result_str

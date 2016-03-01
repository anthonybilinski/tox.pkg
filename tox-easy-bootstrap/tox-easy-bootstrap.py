#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__    = "tox-easy-bootstrap"
__version__  = "0.0.2"
__author__   = "Anton Batenev"
__license__  = "BSD"


import os
import re
import sys
import json
import codecs


# PEP-8
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser


# PEP-3108
try:
    from urllib.request import Request      as Request
    from urllib.request import build_opener as build_opener
except ImportError:
    from urllib2        import Request      as Request
    from urllib2        import build_opener as build_opener


# PEP-469
try:
    dict.iteritems
except AttributeError:
    def iteritems(d):
        return iter(d.items())
else:
    def iteritems(d):
        return d.iteritems()


class ToxBootstrapdConfig(object):
    """
    Tox easy-bootstrap configuration
    """
    def __init__(self, config, filename):
        """
        Parse config dict

        Arguments:
            config   (dict) -- Config in dict of strings
            filename (str)  -- File name for private nodes config
        """
        self.port                  = int(config["port"])
        self.keys_file_path        = str(config["keys_file_path"])
        self.pid_file_path         = str(config["pid_file_path"])
        self.enable_ipv4           = self._bool(config["enable_ipv4"])
        self.enable_ipv6           = self._bool(config["enable_ipv6"])
        self.enable_ipv4_fallback  = self._bool(config["enable_ipv4_fallback"])
        self.enable_lan_discovery  = self._bool(config["enable_lan_discovery"])
        self.enable_tcp_relay      = self._bool(config["enable_tcp_relay"])
        self.tcp_relay_ports       = []
        self.enable_motd           = self._bool(config["enable_motd"])
        self.motd                  = str(config["motd"])
        self.url                   = str(config["url"])
        self.out_file              = str(config["out_file"])
        self.auto_restart          = self._bool(config["auto_restart"])
        self.restart_command       = str(config["restart_command"])
        self.private_nodes         = []

        if self.port < 1 or self.port > 65535:
            raise ValueError("port out of range")

        if not (self.enable_ipv4 or self.enable_ipv6):
            raise ValueError("enable_ipv4 and enable_ipv6 is disabled both")

        if self.enable_tcp_relay:
            for tcp_relay_port in str(config["tcp_relay_ports"]).split(","):
                tcp_relay_port = int(tcp_relay_port)
                if tcp_relay_port < 1 or tcp_relay_port > 65535:
                    raise ValueError("tcp_relay_port out of range")
                self.tcp_relay_ports.append(tcp_relay_port)

            self.tcp_relay_ports = sorted(self.tcp_relay_ports)

            if not len(self.tcp_relay_ports):
                raise ValueError("Empty tcp_relay_ports list")

        for private_node_name in str(config["private_nodes"]).split(","):
            if len(private_node_name):
                self.private_nodes.append(ToxNode(self.loadConfig(filename, private_node_name, ToxNode.defaultConfig())))


    @staticmethod
    def _bool(value):
        """
        Convert string value to boolean

        Arguments:
            value (str|bool) -- String value

        Result (bool):
            Boolean value [true|yes|t|y|1] => True, or False instead
        """
        if type(value) is bool:
            return value

        value = value.lower()

        if value == "true" or value == "yes" or value == "t" or value == "y" or value == "1":
            return True

        return False


    @staticmethod
    def loadConfig(filename, name, config):
        """
        Reads config file

        Arguments:
            filename (str)  -- Config filename
            name     (str)  -- Config section name
            config   (dict) -- Default values

        Result (dict)
            Config in dict of strings
        """
        config = config.copy()

        parser = ConfigParser.ConfigParser()
        parser.read(filename)

        for section in parser.sections():
            if section.lower() == name:
                for option in parser.options(section):
                    config[option.lower()] = parser.get(section, option)

        return config


    @staticmethod
    def defaultConfig():
        """
        Returns default config in dict of strings
        """
        return {
            "port"                 : "33445",
            "keys_file_path"       : "/var/lib/tox-bootstrapd/keys",
            "pid_file_path"        : "/var/run/tox-bootstrapd/tox-bootstrapd.pid",
            "enable_ipv4"          : "true",
            "enable_ipv6"          : "true",
            "enable_ipv4_fallback" : "true",
            "enable_lan_discovery" : "false",
            "enable_tcp_relay"     : "true",
            "tcp_relay_ports"      : "3389,33445",
            "enable_motd"          : "true",
            "motd"                 : "tox-easy-bootstrap",
            "url"                  : "https://nodes.tox.chat/json",
            "out_file"             : "/etc/tox-bootstrapd.conf",
            "auto_restart"         : "false",
            "restart_command"      : "",
            "private_nodes"        : ""
        }


class ToxNode(object):
    """
    Tox Node configuration
    """
    def __init__(self, config):
        """
        Parse config dict

        Arguments:
            config (dict) -- Config in dict of strings
        """
        self.ipv4       = str(config["ipv4"])
        self.ipv6       = str(config["ipv6"]).lower()
        self.port       = int(config["port"])
        self.public_key = str(config["public_key"]).upper()
        self.maintainer = str(config["maintainer"])
        self.location   = str(config["location"]).upper()

        ipv4_re = re.compile("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if not ipv4_re.match(self.ipv4):
            self.ipv4 = None

        ipv6_re = re.compile("^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$")
        if not ipv6_re.match(self.ipv6):
            self.ipv6 = None

        if not (self.ipv4 or self.ipv6):
            raise ValueError("ipv4 and ipv6 is empty both")

        if self.port < 1 or self.port > 65535:
            raise ValueError("Invalid port value")

        public_key_re = re.compile("^[0-9a-fA-F]{64}$")
        if not public_key_re.match(self.public_key):
            raise ValueError("Invalid public key value {0}".format(self.public_key))


    @staticmethod
    def getNodesJson(url):
        """
        Get tox nodes list in raw JSON format

        Arguments:
            url (str) -- URL to query (for example https://nodes.tox.chat/json)

        Result (json):
            Raw JSON nodes list
        """
        headers = {
            "Accept"     : "application/json",
            "User-Agent" : "tox-easy-bootstrap"
        }

        request = Request(url, None, headers)
        opener  = build_opener()
        result  = opener.open(request, timeout = 5)
        code    = result.getcode()

        if code != 200:
            raise RuntimeError("HTTP-{0}".format(code))

        def _json_convert(input):
            if isinstance(input, dict):
                return dict([(_json_convert(key), _json_convert(value)) for key, value in iteritems(input)])
            elif isinstance(input, list):
                return [_json_convert(element) for element in input]
            elif isinstance(input, unicode):
                return input.encode("utf-8")
            else:
                return input

        if sys.version_info < (3, 0):
            result = json.load(result, object_hook = _json_convert)
        else:
            result = json.load(codecs.getreader("utf-8")(result))

        return result["nodes"]


    @staticmethod
    def parseNodesJson(nodes):
        """
        Parse tox nodes list in raw JSON format

        Arguments:
            nodes (json) -- Raw JSON nodes list from _getNodesJson

        Result (array of ToxNode):
            Parsed ToxNode array
        """
        result = []

        for node in nodes:
            # check node is online
            if str(node["status"]).lower() != "true":
                continue

            try:
                result.append(ToxNode(node))
            except ValueError as e:
                pass

        return result


    @staticmethod
    def defaultConfig():
        """
        Returns default node config in dict of strings
        """
        return {
                "ipv4"       : "",
                "ipv6"       : "",
                "port"       : "0",
                "public_key" : "",
                "maintainer" : "",
                "location"   : ""
            }


if __name__ == "__main__":
    try:
        argc = len(sys.argv)

        regexp  = re.compile("--config=(.*)")
        cfgfile = [match.group(1) for arg in sys.argv for match in [regexp.search(arg)] if match]

        if not len(cfgfile):
            cfgfile = "tox-easy-bootstrap.conf"
            if not os.path.isfile(cfgfile):
                cfgfile = "/usr/local/etc/tox-easy-bootstrap.conf"
            if not os.path.isfile(cfgfile):
                cfgfile = "/etc/tox-easy-bootstrap.conf"
        else:
            cfgfile = cfgfile[0]

        if not os.path.isfile(cfgfile):
            raise RuntimeError("config file not found")

        config = ToxBootstrapdConfig.loadConfig(cfgfile, "config", ToxBootstrapdConfig.defaultConfig())

        args   = []
        regexp = re.compile("^--(\S+?)(=(.*)){,1}$")
        for i in range(1, argc):
            arg = sys.argv[i]
            opt = regexp.split(arg)
            if len(opt) == 5:
                if opt[3] == None:
                    opt[3] = True
                config[opt[1].lower()] = opt[3]
            else:
                args.append(arg)

        if len(args):
            raise RuntimeError("Unparsed command line agrs provided")

        config = ToxBootstrapdConfig(config, cfgfile)

        nodes = ToxNode.parseNodesJson(ToxNode.getNodesJson(config.url))
        if not len(nodes):
            raise RuntimeError("Empty node list")

        nodes += config.private_nodes

        # no matter how to sort, but sort needed by all attrs
        nodes.sort(key = lambda x: (x.public_key, x.ipv4, x.ipv6, x.port, x.location, x.maintainer))

        src  = ""
        src += "port = {0}\n".format(config.port)
        src += "keys_file_path = \"{0}\"\n".format(config.keys_file_path)
        src += "pid_file_path = \"{0}\"\n".format(config.pid_file_path)
        src += "enable_ipv6 = {0}\n".format(str(config.enable_ipv6).lower())
        src += "enable_ipv4_fallback = {0}\n".format(str(config.enable_ipv4_fallback).lower())
        src += "enable_lan_discovery = {0}\n".format(str(config.enable_lan_discovery).lower())
        src += "enable_tcp_relay = {0}\n".format(str(config.enable_tcp_relay).lower())
        src += "tcp_relay_ports = {0}\n".format(str(config.tcp_relay_ports))
        src += "enable_motd = {0}\n".format(str(config.enable_motd).lower())
        src += "motd = \"{0}\"\n".format(config.motd)
        src += "bootstrap_nodes = (\n"

        def _strNode(address, node):
            src  = ""
            src += "  {{ // {0}, {1}\n".format(node.maintainer, node.location)
            src += "    address = \"{0}\",\n".format(address)
            src += "    port = {0},\n".format(node.port)
            src += "    public_key = \"{0}\"\n".format(node.public_key)
            src += "  },\n"

            return src

        for node in nodes:
            if config.enable_ipv4 and node.ipv4:
                src += _strNode(node.ipv4, node)
            if config.enable_ipv6 and node.ipv6:
                src += _strNode(node.ipv6, node)

        # remove last comma
        src = src[:-2]
        src += "\n)\n"

        if not len(config.out_file):
            sys.stdout.write("{0}".format(src))
            sys.exit(0)

        dst = ""
        if os.path.isfile(config.out_file):
            with open(config.out_file, "r") as f:
                dst = f.read()

        if src != dst:
            with open(config.out_file, "w") as f:
                f.write(src)

            if config.auto_restart:
                # custom restart command
                if len(config.restart_command):
                    sys.exit(os.system(config.restart_command))
                # Linux initd
                elif os.path.isfile("/etc/init.d/tox-bootstrapd"):
                    sys.exit(os.system("/etc/init.d/tox-bootstrapd restart"))
                # FreeBSD
                elif os.path.isfile("/usr/local/etc/rc.d/tox-bootstrapd"):
                    sys.exit(os.system("/usr/local/etc/rc.d/tox-bootstrapd restart"))
                # Linux systemd
                else:
                    sys.exit(os.system("/bin/systemctl restart tox-bootstrapd"))

        sys.exit(0)

    except Exception as e:
        sys.stderr.write("{0}\n".format(e))
        sys.exit(1)

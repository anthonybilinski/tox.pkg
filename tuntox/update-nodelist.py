#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
import codecs
import random


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


def getNodeList():
    url = "https://nodes.tox.chat/json"

    headers = {
        "Accept"     : "application/json",
        "User-Agent" : "tox.pkg"
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

    return result


def parseNodeList(nodes):
    result = []

    ipv4re  = re.compile("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    ipv6re  = re.compile("^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$")
    fqdn_re = re.compile("^((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}$")
    pkre    = re.compile("^[0-9a-fA-F]{64}$")

    for node in nodes:
        ipv4       = str(node["ipv4"])
        ipv6       = str(node["ipv6"]).lower()
        port       = int(node["port"])
        public_key = str(node["public_key"]).upper()
        maintainer = str(node["maintainer"])
        location   = str(node["location"]).upper()
        udp_status = str(node["status_udp"]).lower()
        tcp_status = str(node["status_tcp"]).lower()
        tcp_ports  = node["tcp_ports"]

        if udp_status != "true" or tcp_status != "true":
            continue
        if not ipv4re.match(ipv4) and not fqdn_re.match(ipv4):
            ipv4 = None
        if not ipv6re.match(ipv6) and not fqdn_re.match(ipv6):
            ipv6 = None
        if not (ipv4 or ipv6):
            continue
        if port < 1 or port > 65535:
            continue
        if not pkre.match(public_key):
            continue
        if len(location) != 2:
            continue

        if ipv4:
            item = {
                "address"    : ipv4,
                "port"       : port,
                "public_key" : public_key,
                "maintainer" : maintainer,
                "location"   : location
            }

            result.append(item)

        if ipv6 and ipv6 != ipv4:
            item = {
                "address"    : ipv6,
                "port"       : port,
                "public_key" : public_key,
                "maintainer" : maintainer,
                "location"   : location
            }

            result.append(item)

    return result


if __name__ == "__main__":
    try:
        nodes = getNodeList();
        nodes = nodes["nodes"]
        nodes = parseNodeList(nodes)

        if len(nodes) == 0:
            raise RuntimeError("Empty node list")

        random.shuffle(nodes)

        result  = ""
        result += "struct bootstrap_node {\n"
        result += "    char *address;\n"
        result += "    uint16_t port;\n"
        result += "    uint8_t key[32];\n"
        result += "} bootstrap_nodes[] = {\n"

        for node in nodes:
            result += "    {\n"
            result += "        \"{0}\", /* {1}, {2} */\n".format(node["address"], node["maintainer"], node["location"])
            result += "        {0},\n".format(node["port"])
            result += "        {\n"
            result += "            "

            bytes = [node["public_key"][i:i + 2] for i in range(0, len(node["public_key"]), 2)]

            index = 0
            for byte in bytes:
                index  += 1
                result += "0x{0}".format(byte)
                if index == 16:
                    result += ",\n            "
                elif index != 32:
                    result += ", "

            result += "\n        }\n"
            result += "    },\n"

        result += "};\n"

        sys.stdout.write(result)
    except Exception as e:
        sys.stderr.write("{0}\n".format(e))
        sys.exit(1)

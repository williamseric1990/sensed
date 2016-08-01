import os
import netifaces


def getIP(ipv6=False):
    ifaces = netifaces.interfaces()
    for ifname in ifaces:
        ifaddr = netifaces.ifaddresses(ifname)
        if ipv6:
            if netifaces.AF_INET6 in ifaddr:
                inet = ifaddr[netifaces.AF_INET6][0]['addr']
                if not inet == '::1':
                    return inet
        else:
            if netifaces.AF_INET in ifaddr:
                inet = ifaddr[netifaces.AF_INET][0]['addr']
                if not inet == '127.0.0.1':
                    return inet
    return None


def getHostname():
    return os.hostname()

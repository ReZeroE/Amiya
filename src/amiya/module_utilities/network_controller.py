import socket
import psutil

from amiya.utils.helper import *

class NetworkController:
    def __get_ip_addresses(self):
        ip_addresses = {
            "IPv4": {},
            "IPv6": {}
        }
        interfaces = psutil.net_if_addrs()

        for interface_name, interface_addrs in interfaces.items():
            for addr in interface_addrs:
                if addr.family == socket.AF_INET:
                    ip_type = "IPv4"
                elif addr.family == socket.AF_INET6:
                    ip_type = "IPv6"
                else:
                    continue

                if interface_name not in ip_addresses[ip_type]:
                    ip_addresses[ip_type][interface_name] = []
                ip_addresses[ip_type][interface_name].append(addr.address)

        return ip_addresses

    def __get_interface_status(self):
        interface_status = {}
        stats = psutil.net_if_stats()
        for interface_name, stat in stats.items():
            interface_status[interface_name] = stat.isup
        return interface_status

    def verbose_ip_addresses(self, connected_only: bool = False):
        ip_addresses = self.__get_ip_addresses()
        interface_status = self.__get_interface_status()

        # Create a combined dictionary to group by interface first
        combined_ip_addresses = {}
        for ip_type, interfaces in ip_addresses.items():
            for iface, addrs in interfaces.items():
                if iface not in combined_ip_addresses:
                    combined_ip_addresses[iface] = {"IPv4": [], "IPv6": [], "Status": interface_status.get(iface, False)}
                combined_ip_addresses[iface][ip_type].extend(addrs)

        sorted_interfaces = sorted(combined_ip_addresses.keys(), key=lambda x: (x != "Wi-Fi" and x != "Ethernet", x))

        for iface in sorted_interfaces:
            ips = combined_ip_addresses[iface]
            if connected_only and ips["Status"] == False: # Print connected IPs only
                continue
            
            status = "Connected" if ips["Status"] else "Disconnected"
            print(Printer.to_lightblue(f"Interface {iface}") + f" ({Printer.to_lightred(status)}):")
            if ips["IPv4"]:
                print(f"  {Printer.to_purple("IPv4 Addresses")}: {', '.join(ips['IPv4'])}")
            if ips["IPv6"]:
                print(f"  {Printer.to_purple("IPv6 Addresses")}: {'\n\t\t  '.join(ips['IPv6'])}")
            print()

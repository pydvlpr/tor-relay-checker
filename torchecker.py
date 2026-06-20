#!/usr/bin/env python3

import sys
import os
import time
from tor_relay_check import TorRelayChecker



if __name__ == '__main__':

  if len(sys.argv) < 3:
    sys.exit("call with <list>|<IP> <yyyy-mm-dd [-d]\n\n"
    "\t<list> file with list of IP addresses\n" \
    "\t<IP> single IP address\n"
    "\t-d: Show additional information\n\n" \
    "Have fun hunting")

  input = sys.argv[1]
  reqdate = sys.argv[2]
  print(f"Check list <{input}> for date <{reqdate}>")
  
  trs = TorRelayChecker()
  if os.path.isfile(input):

    iplist = None
    with open(input, 'r') as file:
      iplist = file.read().splitlines()
      ipcnt = len(iplist)
      print(f"List contains {ipcnt} ip address(es)")

    ip_set = set(iplist)
    ip_list = (list(ip_set))

    #trs = TorRelayChecker()
    print()
    for ip in ip_list:
      print(ip,end=" ")
      trs.set_ip(ip)
      trs.request_exonerator(reqdate)
  else:
    trs.set_ip(input)
    trs.request_exonerator(reqdate)

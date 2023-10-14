#!/usr/bin/env python3

import sys
import time
from tor_relay_check import TorRelayChecker


if __name__ == '__main__':

  if len(sys.argv) != 3:
    sys.exit("call with <list> <yyyy-mm-dd>")

  srcfile = sys.argv[1]
  reqdate = sys.argv[2]
  print(f"Check list <{srcfile}< for date <{reqdate}>")

  iplist = None
  with open(srcfile, 'r') as file:
    iplist = file.read().splitlines()
    ipcnt = len(iplist)
    print(f"List contains {ipcnt} ip address(es)")

  ip_set = set(iplist)
  ip_list = (list(ip_set))

  trs = TorRelayChecker()
  print()
  for ip in ip_list:
    print(ip,end=" ")
    trs.set_ip(ip)
    trs.request_exonerator(reqdate)

#!/usr/bin/env python3

import sys
import time
from tor_relay_check import TorRelayChecker


if __name__ == '__main__':

  if len(sys.argv) != 2:
    sys.exit("call with list")

  srcfile = sys.argv[1]


  iplist = None
  with open(srcfile, 'r') as file:
    iplist = file.read().splitlines()

  ip_set = set(iplist)
  ip_list = (list(ip_set))

  trs = TorRelayChecker()
  for ip in ip_list:
    print(ip,end=" ")
    trs.set_ip(ip)
    trs.request_exonerator("2022-08-28")

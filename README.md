# tor-relay-checker

Simple library to request tor metrics website to check if ip-addresse being tor relay nodes.

Supports requests of ipv4 and ipv6 addresses.

It is possible to request the (Exonerator)[https://metrics.torproject.org/exonerator.html] for a specific date to know if an ip-address was a tor-node, then.

Also the request for information to the (Relay Search)[https://metrics.torproject.org/rs.html] is possible. There you get several technical information about the tor-node.

## Installation

Clone the repository.

```
%> git clone https://github.com/pydvlpr/tor-relay-checker.git
```

Change into repository directory. Use `pipenv` to install dependencies.
```
%> cd tor-relay-checker
%> pipenv sync
```

## Usage

There is the example program `torchecker.py`. It needs a list of ip-addresses and a date to check.

```
%> ./torchecker.py sample.list 2023-01-01                                                     
Check list <sample.list> for date <2023-01-01>
List contains 5 ip address(es)
Using chromedriver by homebrew

89.234.157.254 Exonerator: True
2a0b:f4c1:2::252 Exonerator: True
...
```

The module `tor_relay_check.py` contains several test-cases. They are automatically run by execution of the library as a program.

```
%> python tor_relay_check.py                                                                  
Using chromedriver by homebrew

Checking ip-address 89.234.157.254
Exonerator: True
Technical details
Looking up IP address 89.234.157.254 on or within one day of 2023-10-11. Tor clients could have selected this or these Tor relays to build circuits.
Timestamp (UTC) IP address(es) Identity fingerprint Nickname Exit relay
2023-10-10 00:00:00 89.234.157.254, [2001:67c:2608::1] 4F0C498701A41F4D9CA677EA763FD8CA45348E97 marylou4 Yes
2023-10-10 00:00:00 89.234.157.254, [2001:67c:2608::1] 578E007E5E4535FBFEF7758D8587B07B4C8C5D06 marylou1 Yes
...
```




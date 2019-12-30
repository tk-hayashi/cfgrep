# examples of cfgrep

## Case of IOS

- no option
```
> cfgrep "TenGigabitEthernet7/[12]" ios.txt

!
interface TenGigabitEthernet7/1
 description test1
 ip address 203.0.113.1 255.255.255.252
 ip ospf cost 10
 no cdp enable
!
interface TenGigabitEthernet7/2
 description test2
 ip address 203.0.113.5 255.255.255.252
 ip ospf cost 10
 no cdp enable
!
ip route 0.0.0.0 0.0.0.0 TenGigabitEthernet7/1 203.0.113.2 250
```

- interface mode
```
> cfgrep -i "Vlan10$" ios.txt

!
interface Vlan10
 description test
 ip address 203.0.113.1 255.255.255.252
 ip ospf cost 10
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! ipv4 address search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
router ospf 1
 network 203.0.113.0 0.0.0.3 area 0
```

- bgp mode
```
>  cfgrep -b 203.0.113.1 ios.txt

!
router bgp 65000
 neighbor 203.0.113.1 peer-group TEST
!
router bgp 65000
 neighbor 203.0.113.1 description test
!
access-list 99 permit 203.0.113.1
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! neighbor-group search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
router bgp 65000
 neighbor TEST peer-group
 neighbor TEST remote-as 65000
 neighbor TEST update-source Loopback0
 neighbor TEST route-reflector-client
```

- description mode
```
>  cfgrep -dbi Router ios.txt

!
interface Vlan10
 description Router
 ip address 203.0.113.1 255.255.255.252
 ip ospf network point-to-point
 ip ospf cost 10
 ipv6 address 2001:DB8::1/64
 ipv6 ospf network point-to-point
 ipv6 ospf cost 10
 ipv6 ospf 65000 area 0
!
router bgp 65000
 neighbor 2001:DB8:BEEF::1 remote-as 65000
 neighbor 2001:DB8:BEEF::1 description Router
 neighbor 2001:DB8:BEEF::1 update-source Loopback0
 address-family ipv6
  neighbor 2001:DB8:BEEF::1 activate
  neighbor 2001:DB8:BEEF::1 next-hop-self
!
router bgp 65000
 neighbor 192.0.2.1 remote-as 65000
 neighbor 192.0.2.1 description Router
 neighbor 192.0.2.1 update-source Loopback0
 address-family ipv4
  neighbor 192.0.2.1 activate
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! ipv4 address search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
router ospf 1
 network 203.0.113.0 0.0.0.3 area 0
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! ipv6 address search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
ipv6 route ::/0 Vlan10 2001:DB8::2 250
```

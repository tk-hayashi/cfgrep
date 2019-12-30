# examples of cfgrep

## Case of IOS-XR

- no option
```
> cfgrep "TenGigE0/0/[0-2]/0" XR.txt

!
interface TenGigE0/0/0/0
 description test1
 ipv4 address 203.0.113.1 255.255.255.252
 ipv6 address 2001:db8:1::1/64
!
interface TenGigE0/0/2/0
 description test2
 ipv4 address 203.0.113.5 255.255.255.252
 ipv6 address 2001:db8:2::1/64
!
router ospf 1
 area 0
  interface TenGigE0/0/0/0
   cost 10
   network point-to-point
!
router ospf 1
 area 0
  interface TenGigE0/0/2/0
   cost 10
   network point-to-point
!
router ospfv3 1
 area 0
  interface TenGigE0/0/0/0
   cost 10
   network point-to-point
!
router ospfv3 1
 area 0
  interface TenGigE0/0/2/0
   cost 10
   network point-to-point
!
rsvp
 interface TenGigE0/0/0/0
  bandwidth 10000000
!
mpls traffic-eng
 interface TenGigE0/0/0/0
  backup-path tunnel-te 1
!
mpls ldp
 interface TenGigE0/0/0/0
!
multicast-routing
 address-family ipv4
  interface TenGigE0/0/2/0
   disable
!
router pim
 address-family ipv4
  interface TenGigE0/0/0/0
```

- interface mode
```
>  cfgrep -i TenGigE0/0/2/0 XR.txt

!
interface TenGigE0/0/2/0
 description test
 ipv4 address 203.0.113.5 255.255.255.252
 ipv6 address 2001:db8:1::1/64
!
router static
 address-family ipv4 unicast
  192.0.2.0/24 TenGigE0/0/2/0 203.0.113.6
!
router static
 address-family ipv6 unicast
  ::/0 TenGigE0/0/2/0 2001:db8:1::2
!
router static
 address-family ipv6 unicast
  2001:db8:beef::/48 TenGigE0/0/2/0 2001:db8:1::2
!
router ospf mpls1
 area 0
  interface TenGigE0/0/2/0
   cost 10
   passive enable
!
multicast-routing
 address-family ipv4
  interface TenGigE0/0/2/0
   disable
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! ipv4 address search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
router static
 address-family ipv4 unicast
  192.0.2.0/24 TenGigE0/0/2/0 203.0.113.6
!
prefix-set TEST
  203.0.113.4/30,
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! ipv6 address search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
prefix-set TEST
  2001:db8:1::/64,
!
router static
 address-family ipv6 unicast
  ::/0 TenGigE0/0/2/0 2001:db8:1::2
!
router static
 address-family ipv6 unicast
  2001:db8:beef::/48 TenGigE0/0/2/0 2001:db8:1::2
```

- bgp mode
```
>  cfgrep -b 203.0.113.1 XR.txt

!
router bgp 65000
 neighbor 203.0.113.1
  use neighbor-group TEST
  description test
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! neighbor-group search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
router bgp 65000
 neighbor-group TEST
  remote-as 65000
  update-source Loopback0
  address-family ipv4 unicast
   route-policy PASS in
   route-policy PASS out
   next-hop-self
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! route-policy search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
route-policy PASS
  pass
end-policy
```

- description mode
```
>  cfgrep -dbi CoreRouter XR.txt

!
interface TenGigE0/0/0/0
 description CoreRouter Te0/0/0/0
 ipv4 address 203.0.113.5 255.255.255.252
 ipv6 address 2001:db8:beef:1::1/64
 ipv6 enable
!
interface TenGigE0/1/0/0
 description CoreRouter Te0/1/0/0
 ipv4 address 203.0.113.9 255.255.255.252
 ipv6 address 2001:db8:beef:2::1/64
 ipv6 enable
!
router bgp 65000
 neighbor 198.51.100.2
  use neighbor-group CoreGroup
  description CoreRouter
  address-family ipv4 unicast
   route-policy PASS out
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! route-policy search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
route-policy PASS
  pass
end-policy
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! neighbor-group search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
router bgp 65000
 neighbor-group CoreGroup
  remote-as 65000
  update-source Loopback0
  address-family ipv4 unicast
   route-policy DROP in
   route-policy PASS out
   next-hop-self
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!
! route-policy search
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
route-policy PASS
  pass
end-policy
!
route-policy DROP
  drop
end-policy
```

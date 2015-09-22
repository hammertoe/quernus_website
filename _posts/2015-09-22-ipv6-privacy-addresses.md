---
layout: post
title: IPv6 Privacy Addresses
comments: True
tags: ipv6
summary: IPv6 has a mechanism for generating random addresses to maintain some privacy for hosts
---

I'm starting to play with IPv6 at home and in the office. I'll be detailing some of what I've learnt here. 

One thing I noticed, was that once configured I ended up with *two* IPv6 addresses on my interfaces:

```
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether 04:0c:ce:e1:3a:7b 
	inet6 fe80::60c:ceff:fee1:3a9a%en0 prefixlen 64 scopeid 0x4 
	inet 192.168.1.19 net mask 0xffffff00 broadcast 192.168.1.255
	inet6 en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether 04:0c:ce:e1:3a:9a 
	inet6 fe80::60c:ceff:fee1:3a9a%en0 prefixlen 64 scopeid 0x4 
	inet 192.168.1.19 netmask 0xffffff00 broadcast 192.168.1.255
	inet6 2001:470:1f1d:33a:60c:ceff:fee1:3a9a prefixlen 64 autoconf 
	inet6 2001:470:1f1d:33a:3826:36d7:fbd6:16f prefixlen 64 autoconf temporary 
	nd6 options=1<PERFORMNUD>
	media: autoselect
	status: active
 prefixlen 64 autoconf 
	inet6 2001:470:1f1d:33a:3826:36d7:fbd6:16f prefixlen 64 autoconf temporary 
	nd6 options=1<PERFORMNUD>
	media: autoselect
	status: active
```

The first IPv6 address `2001:470:1f1d:33a:60c:ceff:fee1:3a9a` has been auto configured and includes the MAC address of the interface `04:0c:ce:e1:3a:9a` encoded in it using the [Modified EUI-64 format](https://en.wikipedia.org/wiki/IPv6_address#Modified_EUI-64). But this means that the publicly visible source address of my connections can be tied directly to my hardware.

The second IPv6 address `2001:470:1f1d:33a:3826:36d7:fbd6:16f` has been generated randomly by the OS and router and has the `temporary` keyword attached. It is this address that the OS uses by default for outbound connections to that tracking is much harder.

The full detail of these privacy extensions are detailed in [RFC4941 - Privacy Extensions for Stateless Address Autoconfiguration in IPv6](https://tools.ietf.org/html/rfc4941).

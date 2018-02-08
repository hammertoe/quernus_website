---
layout: post
title: Local DNS for local people
comments: True
tags: dns, unbound, openbsd, split horizon
summary: Using the Unbound DNS server on OpenBSD you are able to easily create a 'split horizon' DNS in which you serve some additional information locally that is not visible globally.
---

I have a local DNS server running at home that serves my computers, phones, tablets etc running in the house. This is running on Unbound, the DNS server that comes with OpenBSD. If you have used Bind before, you will find Unbound to be a refreshing change. Like most of the services in OpenBSD they do a simple job well.

I have my main DNS for my domain name `quernus.co.uk` hosted with my domain name registrar (name.com). This has records for things like `www.quernus.co.uk` and `mail.quernus.co.uk`. But I also run some services at home and in my office that I want to set up DNS records for. I don't necessarily want to put those on name.com as 1) they are not needed for those externally, and in most cases resolve to private IP addresses (`192.168.0.0/16` or `fc::/7`).

So I'd like to have entries set up for them in my local DNS server, so that devices at home can look them up. But I don't want to have to replicate the public records at name.com as then I have to update them in two places (e.g. if the public address of `www.quernus.co.uk` moved).

Unbound has a nice feature that allows you to define local records that it will use, but then can still look up the result elsewhere if not found. So in `unbound.conf` I have records like:

```bash
# my local entries
local-zone: "quernus.co.uk" typetransparent
local-data: "topsecret.quernus.co.uk AAAA fd60::1"
local-data: "ultrasecret.quernus.co.uk AAAA fd60::2"

forward-zone:
        name: "."                               # use for ALL queries
        forward-addr: 8.8.8.8                   # google.com
```

The key is the `typetransparent` keyword which mean that Unbound will attempt to look the query up with local data and if it can't find a match will transparently pass it on to a forwarding server.

and so now, I can look up both the private addresses at home:

```bash
Matts-iMac:~ matt$ nslookup
> set type=AAAA
> topsecret.quernus.co.uk
Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
topsecret.quernus.co.uk	has AAAA address fd60::1

Authoritative answers can be found from:
> www.quernus.co.uk
Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
www.quernus.co.uk	has AAAA address 2001:41c8:11a:5::1

Authoritative answers can be found from:

```

But not from the outside world:

```bash
Matts-Air:~ matt$ nslookup
> set type=AAAA
> topsecret.quernus.co.uk
Server:		10.250.108.1
Address:	10.250.108.1#53

** server can't find topsecret.quernus.co.uk: NXDOMAIN
> www.quernus.co.uk
Server:		10.250.108.1
Address:	10.250.108.1#53

Non-authoritative answer:
www.quernus.co.uk	has AAAA address 2001:41c8:11a:5::1

Authoritative answers can be found from:

```


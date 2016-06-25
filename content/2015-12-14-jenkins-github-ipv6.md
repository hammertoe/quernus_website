---
layout: post
title: Jenkins, Github, and IPv6
comments: True
tags: technology, jenkins, github, ipv6, openbsd, networking, DNS64, NAT64
summary: Github and some other sites don't yet support IPv6. But I want our build servers to be IPv6 only. Here is how I achieved it using OpenBSD's NAT64 and unbound's DNS64 functions
---

I've been setting up my local network to be IPv6 for as much of things as I can. I've even been trying to achieve the holy grail in terms of future-proofing the networking by making some of the hosts IPv6 only.
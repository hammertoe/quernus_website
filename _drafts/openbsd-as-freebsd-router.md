---
layout: post
title: Using OpenBSD as a FreeBSD Router
---

## FreeBSD is a Great Server

[FreeBSD](https://www.freebsd.org/) is a great OS. I use it for my office fileserver due to it's ZFS implementation, and general robustness as a fileserver and general office server.

However one thing I don’t like about FreeBSD is that even though it has had IPSEC baked into it for many many years, it is still not enabled by default in the `GENERIC` kernel. Most kernel options in FreeBSD can be loaded as loadable modules, but IPSEC is not one of them.

I’ve been using FreeBSD [since 1996](http://marc.info/?l=freebsd-bugs&m=103030758511075&w=2) and used to sit there leaving it running a `make kernel` overnight to build new kernel on my lie 386sx-16 that I had at the time. In those days, any changes or options required compiling your own custom kernel. But this is 2015 now, and to be frank, I just don’t have the inclination or patience to do that any more. Even if hardware improvements mean what used to take 8 hours, takes minutes to do.

But more importantly FreeBSD now has a [binary updates system](https://www.freebsd.org/doc/handbook/updating-upgrading-freebsdupdate.html) which means that interim binary security patches can be applied without needing to do a ‘build world’. But if I’ve compiled my own kernel to get IPSEC, this is no longer an option. It seemed FreeBSD update will clobber those changes. This what what I found updating my FreeBSD 10.1 office server using `freebsd-update` when suddenly my IPSEC VPN from home to office stopped working.

## OpenBSD is a Great Router

Whilst as [Netsight](https://www.netsight.co.uk), in 2004 [I started looking](http://marc.info/?l=openbsd-misc&m=110261323606356&w=2) at using [OpenBSD](http://www.openbsd.org/) for routing. We were using big Cisco 5505 switches with Route Switch Modules in to provide routing. The problem was, they soon became quite slow. They were great if you wanted to do very simple routing, and they could do Layer 3 switching in silicon on the linecards. But as soon as you started to do access lists then they had to route the packets on the main CPU. Not only that, but Cisco’s ACL syntax quickly became very cumbersome as you had no way of doing any kind of macros or variables in the language.

OpenBSD on the other hand comes with the amazing `pf` packet filter. This is a fantastic stateful packet filter that is extremely fast, and with a very nice expressive language to write firewall rules.

At Netsight’s datacentre we soon ended up with a pair of x86 boxes running as OpenBSD firewalls. They were configured with pf and [CARP](http://www.openbsd.org/faq/pf/carp.html) to provide failure. These two boxes protected the entire datacentre network and acted as a main filter and choke point to sanitise our traffic. They ensured that spoofed packets were not leaving our network from any customers and that we could quickly and easily help protect against any attacks on the network.

After not long we replaced all the Cisco routers with OpenBSD boxes as they turned out to be extremely reliable, flexible and fast for gigabit-level L3 intra-vlan routing.

## FreeBSD *and* OpenBSD?!

FreeBSD has it’s own Hypervisor, [bhvye](http://bhyve.org/), allowing you to run FreeBSD, OpenBSD, or Linux guests as virtual machines on a FreeBSD host.

So could I potentially have my cake *and* eat it? Could I have a FreeBSD host and run an OpenBSD guest to do the IPSEC termination? Well, virtualised routers have started to become quite a hot topic with the increase of virtualisation on servers. If you are virtualising a number or servers, why not virtualise the networking infrastructure too? You can leverage the redundancy you have in the VM cluster and also move the network functions closer to the hosts they are supporting.


---
layout: post
title: Cloning a ZVol for a new VM
comments: True
tags: FreeBSD, ZFS
summary: How to clone ZFS zvols to replicate VMs
---

I am using bhyve as a VM system for OpenBSD, Linux and FreeBSD guests running on a FreeBSD host.

I wanted to create a new OpenBSD VM to set up a local mail server VM. And realised I could probably clone one of my existing OpenBSD VM's filesystem and just start with that. [I'm using ZFS zvols for the underlying data store for the VM](https://www.geeklan.co.uk/?p=1521).

So, firstly I took a snapshot of the running OpenBSD VM:

```
zfs snapshot storage/vms/openbsd@booted
```

Then clone it:

```
zfs clone -p storage/vms/openbsd@booted storage/vms/mailserver
```

Listing the zvols you can see the new one:

```
root@jenna:/storage/vms # zfs list -r storage/vms
NAME                   USED  AVAIL  REFER  MOUNTPOINT
storage/vms            111G  4.82T  4.54G  /storage/vms
storage/vms/mailserver 1.93M 4.82T  2.92G  -
storage/vms/openbsd    106G  4.92T  2.92G  -
```

What is interesting is the amount of storage used, in this case just 1.93M, so the new OpenBSD server seems to only consume space where different to the existing one. ZFS' copy on write is pretty awesome :)



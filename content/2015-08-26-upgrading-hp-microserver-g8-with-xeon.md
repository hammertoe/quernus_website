---
layout: post
title: Upgrading HP Microserver G8 with a Xeon
comments: True
tags: FreeBSD, Hardware
summary: A cheap and simple CPU upgrade to a HP Microserver for many more cores and virtualisation features
---

I've got a small HP Microserver G8 in my office as a general office fileserver, VM host for software projects, network server etc.

![HP Microserver G8](/public/hp_microserver.jpg)

It originally came with a 2.3 Ghz dual core Xeon. This server was insanely good value for money, at only £179 (inc VAT) for the bare server with a Celeron G1610T processor and 2GB RAM. I spent a further £350 on 4 x WD Red 4GB disks and £110 on a 16GB memory kit for it.

The way I have the server set up, it boots from an internal SD Card into FreeBSD and starts the internal network interfaces. The majority of the actual data is then on a 4-disk ZFS raidz2 with each disk being a GELI encrypted filesystem:

```
root@jenna:~ # zpool list -v
NAME             SIZE  ALLOC   FREE  EXPANDSZ   FRAG    CAP  DEDUP  HEALTH  ALTROOT
storage         10.9T   384G  10.5T         -     1%     3%  1.00x  ONLINE  -
  raidz2        10.9T   384G  10.5T         -     1%     3%
    ada0p2.eli      -      -      -         -      -      -
    ada1p2.eli      -      -      -         -      -      -
    ada2p2.eli      -      -      -         -      -      -
    ada3p2.eli      -      -      -         -      -      -
  da0             58G   656K  58.0G         -     0%     0%
```

On boot, I SSH into the server from my desktop and manually run a script mount the main storage:

```
root@jenna:~ # cat mountstorage.sh
geli attach -k /root/storage.key ada0p2 || exit 
geli attach -k /root/storage.key ada1p2 || exit
geli attach -k /root/storage.key ada2p2 || exit
geli attach -k /root/storage.key ada3p2 || exit
zfs mount -a
```

I then run a script to start all the guest VMs (including [The OpenBSD virtual router](/2015/07/27/openbsd-as-freebsd-router/)). This way if the server is ever stolen, the data is at least secure.

A while back I bought a more powerful CPU for it. After doing some searching around I found that an Intel BX80637E31230V2 processor at £181 should be a drop in replacement. It should run cool enough to still be OK in the small case of the server. This is a Xeon class processor which has some more virtualisation features:

* Intel Turbo Boost Technology 2.0
* Intel vPro Technology
* Intel Hyper-Threading Technology
* Intel Virtualization Technology (VT-x)
* Intel Virtualization Technology for Directed I/O (VT-d)

Having VT-d means I can do PCI passthru on bhyve and pass PCI devices, such as network ports directly through to a guest OS on the VM. It also features AES-NI meaning it can do the AES crypto for the filesystem in hardware. I'm not entirely sure I trust onboard crypto these days, maybe me just being paranoid.

One great thing about this little server, is that it has an ethernet-based ILO port which gives you remote console access. When I replaced the CPU I was never expecting it to 'just work' first time. Inevitably *something* was going to cause trouble. I was expecting some kind of 'New CPU detected, Press F1'-type message on the console. But as it was it just booted up straight away without even needing me to go into the ILO console.

Physically replacing the CPU was dead simple, and pretty much tool-less. Just a couple of thumb-screws on the back to get the case off. Then unplug about five cables from the motherboard and slide the motherboard tray out the back of the chassis. Then unbolting the CPU was a case of just undo-ing 4 torx bolts holding the heatsink on using the supplied torx wrench. Swap the CPU, then put it back together, and voila. Back and running about 10 minutes later.

But anyway, here is the relevent bits of dmesg output before and after the upgrade:


Before:

```
CPU: Intel(R) Celeron(R) CPU G1610T @ 2.30GHz (2294.84-MHz K8-class CPU)
  Origin = "GenuineIntel"  Id = 0x306a9  Family = 0x6  Model = 0x3a  Stepping = 9
  Features=0xbfebfbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,CLFLUSH,DTS,ACPI,MMX,FXSR,SSE,SSE2,SS,HTT,TM,PBE>
  Features2=0xd9ae3bf<SSE3,PCLMULQDQ,DTES64,MON,DS_CPL,VMX,EST,TM2,SSSE3,CX16,xTPR,PDCM,PCID,SSE4.1,SSE4.2,POPCNT,TSCDLT,XSAVE,OSXSAVE>
  AMD Features=0x28100800<SYSCALL,NX,RDTSCP,LM>
  AMD Features2=0x1<LAHF>
  Structured Extended Features=0x281<FSGSBASE,SMEP,ERMS>
  VT-x: PAT,HLT,MTF,PAUSE,EPT,UG,VPID
  TSC: P-state invariant, performance statistics

...
FreeBSD/SMP: Multiprocessor System Detected: 2 CPUs
FreeBSD/SMP: 1 package(s) x 2 core(s)
 cpu0 (BSP): APIC ID:  0
 cpu1 (AP): APIC ID:  2
ioapic0: Changing APIC ID to 8
ioapic0 <Version 2.0> irqs 0-23 on motherboard
random: <Software, Yarrow> initialized
kbd1 at kbdmux0
cryptosoft0: <software crypto> on motherboard
acpi0: <HP ProLiant> on motherboard
acpi0: Power Button (fixed)
cpu0: <ACPI CPU> on acpi0
cpu1: <ACPI CPU> on acpi0
```

After:

```
CPU: Intel(R) Xeon(R) CPU E3-1230 V2 @ 3.30GHz (3292.59-MHz K8-class CPU)
  Origin="GenuineIntel"  Id=0x306a9  Family=0x6  Model=0x3a  Stepping=9
  Features=0xbfebfbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,CLFLUSH,DTS,ACPI,MMX,FXSR,SSE,SSE2,SS,HTT,TM,PBE>
  Features2=0x7fbae3ff<SSE3,PCLMULQDQ,DTES64,MON,DS_CPL,VMX,SMX,EST,TM2,SSSE3,CX16,xTPR,PDCM,PCID,SSE4.1,SSE4.2,x2APIC,POPCNT,TSCDLT,AESNI,XSAVE\
,OSXSAVE,AVX,F16C,RDRAND>
  AMD Features=0x28100800<SYSCALL,NX,RDTSCP,LM>
  AMD Features2=0x1<LAHF>
  Structured Extended Features=0x281<FSGSBASE,SMEP,ERMS>
  XSAVE Features=0x1<XSAVEOPT>
  VT-x: PAT,HLT,MTF,PAUSE,EPT,UG,VPID
  TSC: P-state invariant, performance statistics

FreeBSD/SMP: Multiprocessor System Detected: 8 CPUs
FreeBSD/SMP: 1 package(s) x 4 core(s) x 2 SMT threads
 cpu0 (BSP): APIC ID:  0
 cpu1 (AP): APIC ID:  1
 cpu2 (AP): APIC ID:  2
 cpu3 (AP): APIC ID:  3
 cpu4 (AP): APIC ID:  4
 cpu5 (AP): APIC ID:  5
 cpu6 (AP): APIC ID:  6
 cpu7 (AP): APIC ID:  7
```

Checking the IPMI sensors, and the processor is running at 40 degrees C at the moment, when fairly idle:

```
root@jenna:~ # ipmitool sensor
UID Light        | 0x0        | discrete   | 0x0080| na        | na        | na        | na        | na        | na        
Health LED       | 0x0        | discrete   | 0x0080| na        | na        | na        | na        | na        | na        
Power Supply 1   | 0x0        | discrete   | 0x0180| na        | na        | na        | na        | na        | na        
Fan 1            | 12.544     | percent    | ok    | na        | na        | na        | na        | na        | na        
01-Inlet Ambient | 22.000     | degrees C  | ok    | na        | na        | na        | na        | 42.000    | 46.000    
02-CPU           | 40.000     | degrees C  | ok    | na        | na        | na        | na        | 70.000    | 0.000     
03-P1 DIMM 1-2   | 37.000     | degrees C  | ok    | na        | na        | na        | na        | 87.000    | 0.000     
04-HD Max        | na         |            | na    | na        | na        | na        | na        | 60.000    | 0.000     
05-Chipset       | 59.000     | degrees C  | ok    | na        | na        | na        | na        | 105.000   | 0.000     
06-Chipset Zone  | 46.000     | degrees C  | ok    | na        | na        | na        | na        | 68.000    | 73.000    
07-VR P1 Zone    | 52.000     | degrees C  | ok    | na        | na        | na        | na        | 93.000    | 98.000    
08-Supercap Max  | na         |            | na    | na        | na        | na        | na        | 65.000    | 0.000     
09-iLO Zone      | 47.000     | degrees C  | ok    | na        | na        | na        | na        | 72.000    | 77.000    
10-PCI 1         | na         |            | na    | na        | na        | na        | na        | 100.000   | 0.000     
11-PCI 1 Zone    | 37.000     | degrees C  | ok    | na        | na        | na        | na        | 64.000    | 69.000    
12-Sys Exhaust   | 50.000     | degrees C  | ok    | na        | na        | na        | na        | 68.000    | 73.000    
13-LOM           | na         |            | na    | na        | na        | na        | na        | 100.000   | 0.000     
Memory           | 0x0        | discrete   | 0x4080| na        | na        | na        | na        | na        | na        
```

Any questions, then let me know in the comments below.






 


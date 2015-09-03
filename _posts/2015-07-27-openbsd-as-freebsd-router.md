---
layout: post
title: Using OpenBSD as a FreeBSD Router
comments: True
tags: OpenBSD, FreeBSD, networking
summary: FreeBSD is a great general server, OpenBSD is great at networking and security. This is how I run a virtual router using OpenBSD and bhyve on a FreeBSD host
---

## FreeBSD is a Great Server

[FreeBSD](https://www.freebsd.org/) is a great OS. I use it for my office fileserver due to its ZFS implementation, and general robustness as a fileserver and general office server.

However one thing I don’t like about FreeBSD is that even though it has had IPSEC baked into it for many many years, it is still not enabled by default in the `GENERIC` kernel. Most kernel options in FreeBSD can be loaded as loadable modules, but IPSEC is not one of them.

I’ve been using FreeBSD [since 1996](http://marc.info/?l=freebsd-bugs&m=103030758511075&w=2) and used to sit there leaving it running a `make kernel` overnight to build new kernel on my little 386sx-16 that I had at the time. In those days, any changes or options required compiling your own custom kernel. But this is 2015 now, and to be frank, I just don’t have the inclination or patience to do that any more. Even if hardware improvements mean what used to take 8 hours, takes minutes to do.

But more importantly FreeBSD now has a [binary updates system](https://www.freebsd.org/doc/handbook/updating-upgrading-freebsdupdate.html) which means that interim binary security patches can be applied without needing to do a ‘build world’. But if I’ve compiled my own kernel to get IPSEC, this is no longer an option. It seemed FreeBSD update will clobber those changes. This what what I found updating my FreeBSD 10.1 office server using `freebsd-update` when suddenly my IPSEC VPN from home to office stopped working.

## OpenBSD is a Great Router

In 2004, whilst at [Netsight](https://www.netsight.co.uk), [I started looking](http://marc.info/?l=openbsd-misc&m=110261323606356&w=2) at using [OpenBSD](http://www.openbsd.org/) for routing. We were using big Cisco 5505 switches with Route Switch Modules in to provide routing. The problem was, they soon became quite slow. They were great if you wanted to do very simple routing, and they could do Layer 3 switching in silicon on the linecards. But as soon as you started to do access lists then they had to route the packets on the main CPU. Not only that, but Cisco’s ACL syntax quickly became very cumbersome as you had no way of doing any kind of macros or variables in the language.

OpenBSD on the other hand comes with the amazing `pf` packet filter. This is a fantastic stateful packet filter that is extremely fast, and with a very nice expressive language to write firewall rules.

At Netsight’s datacentre we soon ended up with a pair of x86 boxes running as OpenBSD firewalls. They were configured with pf and [CARP](http://www.openbsd.org/faq/pf/carp.html) to provide redundancy. These two boxes protected the entire datacentre network and acted as a main filter and choke point to sanitise our traffic. They ensured that spoofed packets were not leaving our network from any customers and that we could quickly and easily help protect against any attacks on the network.

After not long we replaced all the Cisco routers with OpenBSD boxes as they turned out to be extremely reliable, flexible and fast for gigabit-level L3 intra-vlan routing.

## FreeBSD *and* OpenBSD?!

FreeBSD has it’s own Hypervisor, [bhvye](http://bhyve.org/), allowing you to run FreeBSD, OpenBSD, or Linux guests as virtual machines on a FreeBSD host.

So could I potentially have my cake *and* eat it? Could I have a FreeBSD host and run an OpenBSD guest to do the IPSEC termination? Well, virtualised routers have started to become quite a hot topic with the increase of virtualisation on servers. If you are virtualising a number or servers, why not virtualise the networking infrastructure too? You can leverage the redundancy you have in the VM cluster and also move the network functions closer to the hosts they are supporting.

As it turns out [someone else has already done something similar](https://forums.freebsd.org/threads/howto-bhyve-using-openbsd-as-main-firewall-in-freebsd.50470/). They are using PCI passthru that allows you to pass a PCI device to a guest and have them control it completely. I was not able to do that due to not having a processor with the required VT-d feature to do this. But also, my external network interface is actually a USB ethernet adapter. My server is a HP Microserver G8 with two built in gigabit ports. I wanted to use both those ports for internal connections — one to my desktop, an iMac and one to a Mac Mini iOS build server. In order to do passthru, I’d have to pass the entire USB hub through to the guest. In reality this would probably not be an issue, as there are four different USB hubs on the server, and so I could pass a USB 2.0 hub to the guest, and keep a USB 3.0 hub for the host to use for transferring data to/from USB sticks.

But for now I can achieve the same effect by bridging the physical interface on the host with the virtual interface to the guest. In fact I’ve got two bridges, one representing the ‘inside’ of the network, and one the ‘outside’.


## The Actual Configs

So to boot the vm itself, I have a script that starts the OpenBSD VM and configures the devices for it. Due to needing GRUB to boot it, you need the `grub-bhyve` packages and a custom script such as below:

{% highlight sh %}
matt@jenna:~root % cat startvm.sh
cd /storage/vms
grub-bhyve -m /storage/vms/obsd.map -r cd0 -M 256M obsd57 < obsd57.in
bhyve -m 256M -A -H -P -s 0:0,amd_hostbridge -s 1:0,lpc -s 3:0,virtio-net,tap0 -s 4:0,virtio-blk,/dev/zvol/storage/vms/openbsd -s 5:0,virtio-net,tap1 -l com1,stdio -W obsd57
{% endhighlight %}

{% highlight sh %}
matt@jenna:~root % cat /storage/vms/obsd57.in 
kopenbsd -h com0 -r sd0a (hd0,openbsd1)/bsd
boot
{% endhighlight %}

In the bhyve command above you can see I have configured two virtual ethernet adapters bound to `tap0` and `tap1` on the host FreeBSD server. 

I have this as a manual script I run, as my server uses GELI to encrypt my main storage, a ZFS array over 4 disks. When my server boots, it boots to a minimal system with none of the ZFS mounted. I need to SSH in and start the ZFS array from another script and supply the passphrase to decrypt the disks. Once the ZFS array is up, I can run the script above to start the OpenBSD server and get connectivity to the outside world.

My complete `/etc/rc.conf` file to set up the networking. Note I also have a wifi adapter and the server acts as a base station in the office for my phone and laptop. I also have two vlans to the iMac: a high MTU one for direct data between the iMac and the server, and a regular MTU one for external data and bridging to the wifi.

{% highlight sh %}
matt@jenna:~root % cat /etc/rc.conf
hostname=“jenna”
keymap=“uk.iso-ctrl.kbd”

# Configure wifi interface
wlans_run0=“wlan0”
create_args_wlan0=“wlanmode hostap country GB”
ifconfig_wlan0=“ssid quernus indoor mode 11a channel 100”
hostapd_enable=“YES”

# Configure physcial interfaces
ifconfig_bge0=“mtu 1500 up”
ifconfig_bge1=“mtu 9000 up”
ifconfig_ue0=“up”

# bring up vlans on bge1 link to iMac
vlans_bge1=“1 2”
ifconfig_bge1_1=“inet 192.168.66.1 netmask 255.255.255.0 mtu 9000”
ifconfig_bge1_2=“up mtu 1500”

# Create cloned interfaces
cloned_interfaces=“bridge0 bridge1 tap0 tap1”

# Configure tap interfaces for OpenBSD router VM to use
ifconfig_tap0=“up”
ifconfig_tap1=“up”

# Bring up bridges
# bridge0 is internal facing bridge
ifconfig_bridge0=“inet 192.168.64.2 netmask 255.255.255.0 addm wlan0 addm bge0 addm tap0 addm bge1.2”
# bridge1 is external facing bridge
ifconfig_bridge1=“addm ue0 addm tap1”

# Route all traffic to OpenBSD VM
defaultrouter=“192.168.64.1”

# Configure services and ZFS
sshd_enable=“YES”
ntpd_enable=“YES”
powerd_enable=“YES”
dumpdev=“AUTO”
zfs_enable=“YES”
samba_server_enable=“YES”
rsyncd_enable=“YES”
avahi_daemon_enable=“YES”
{% endhighlight %}

One thing in particular to note, is that we are *not* forwarding packet at all on the FreeBSD host:

{% highlight sh %}
root@jenna:~ # sysctl net.inet.ip.forwarding
net.inet.ip.forwarding: 0
{% endhighlight %}

That is because *all* of the routing is happening on the OpenBSD box itself.

So lets look at the OpenBSD router VM. Firstly see that is has two virtual network interfaces as per the `bhyve` command we ran to create it:

{% highlight sh %}
$ dmesg | grep virtio
virtio0 at pci0 dev 3 function 0 “Qumranet Virtio Network” rev 0x00: Virtio Network Device
vio0 at virtio0: address 00:a0:98:52:db:56
virtio0: msi
virtio1 at pci0 dev 4 function 0 “Qumranet Virtio Storage” rev 0x00: Virtio Block Device
vioblk0 at virtio1
virtio1: msi
virtio2 at pci0 dev 5 function 0 “Qumranet Virtio Network” rev 0x00: Virtio Network Device
vio1 at virtio2: address 00:a0:98:e9:8d:9c
virtio2: msi
{% endhighlight %}

I have configured the two virtual interfaces, one with an internal IP address, and one with my public static external address assigned to me by my upstream provider:

{% highlight sh %}
$ cat /etc/hostname.vio0                                                                                                                                       
inet 192.168.64.1 255.255.255.0
$ cat /etc/hostname.vio1 
inet 31.210.128.9 255.255.255.224
$ cat /etc/mygate                                                                                                                                              
31.210.128.1
$ cat /etc/sysctl.conf                                                                                                                                         
net.inet.ip.forwarding=1
ddb.panic=0
{% endhighlight %}

I have configured `pf` to do the NAT for me, and allow in some servers such as SSH. It also allows in IPSEC traffic from my home router. I also run a SIP proxy on here to allow my SIP client on my desktop to connect to my VOIP provider.

{% highlight sh %}
# cat /etc/pf.conf
ext_if=“vio1”
int_if=“vio0”
home_ip=“x.x.x.x”

set skip on lo
set skip on $int_if

match out on $ext_if from 192.168.0.0/16 to any nat-to (egress:0)

block in log
pass out        # establish keep-state


# Allow ping etc
pass in on $ext_if proto icmp from any to any

# Allow ssh
pass in on $ext_if proto tcp from any to port 22

# Allow in IPSEC VPN traffic
pass in on $ext_if proto esp from $home_ip to (egress:0)
pass in on enc0

# Allow in SIP traffic
pass in on $ext_if proto udp from any to port { 5060, 7070:7080 }

{% endhighlight %}


Looking at the output from `ifconfig -a` we can see the two interfaces 

{% highlight sh %}
$ ifconfig -a  
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 32768
        priority: 0
        groups: lo
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x4
        inet6 ::1 prefixlen 128
        inet 127.0.0.1 netmask 0xff000000
vio0: flags=8b43<UP,BROADCAST,RUNNING,PROMISC,ALLMULTI,SIMPLEX,MULTICAST> mtu 1500
        lladdr 00:a0:98:52:db:56
        priority: 0
        media: Ethernet autoselect
        status: active
        inet 192.168.64.1 net mask 0xffffff00 broadcast 192.168.64.255
vio1: flags=8b43<UP,BROADCAST,RUNNING,PROMISC,ALLMULTI,SIMPLEX,MULTICAST> mtu 1500
        lladdr 00:a0:98:e9:8d:9c
        priority: 0
        groups: egress
        media: Ethernet autoselect
        status: active
        inet 31.210.128.9 net mask 0xffffffe0 broadcast 31.210.128.31
enc0: flags=0<>
        priority: 0
        groups: enc
        status: active
pflog0: flags=141<UP,RUNNING,PROMISC> mtu 33144
        priority: 0
        groups: pflog
{% endhighlight %}

As for the actual IPSEC setup itself. This was a breeze on OpenBSD and detail in various places:

* [Zero to IPSec in 4 minutes](http://www.symantec.com/connect/articles/zero-ipsec-4-minutes)
* [Building VPNs on OpenBSD](http://www.kernel-panic.it/openbsd/vpn/vpn3.html) 

My `/etc/ipsec.conf` file is shown below. The remote end of this connection is a Draytek Vigor 2860 router at home.

{% highlight sh %}
# more ipsec.conf                                                                                                                                              
ike dynamic  esp from 192.168.64.0/22 to 192.168.1.0/24 local 31.210.128.9 peer x.x.x.x \
         main auth hmac-sha1  enc aes group modp1024 \
         quick auth hmac-sha1 enc aes \
         srcid 31.210.128.9 dstid x.x.x.x \
         psk MYSECRET
{% endhighlight %}

## Conclusion

So, a few weeks on, and this is all working really well. Not had any issues with stability or performance with the network at all. I’ve since been able to set up OpenBSDs fantastic `relayd` to proxy incoming HTTPS traffic to the Mac Mini build server in the office. 

At some point I might try the PCI passthru route. I do have a new CPU sat on my desk with VT-d to plug into the server, but not got around to it yet. But for now the bridging route works well and also gives me an additional point at which to run `tcpdump` to test anything.

Any questions, then let me know in the comments below.






 


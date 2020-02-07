---
layout: post
title: Creating a Ripple Wallet with FreeBSD and Raspberry Pi 3
comments: True
tags: ripple, xrp, blockchain, freebsd, raspberry pi
summary: Here are the steps I went through to create a secure Ripple Wallet on a Raspberry Pi
status:  draft
---

## The Idea

As I've been getting in Ripple more and more, I've been more aware of security around storage of the keys for my XRP. As with all things security related there is always a trade-off between absolute security and usability. For the most part, I use paper wallets for the XRP. These are offline generate keypairs with the secret key kept on a piece of paper and not shared anywhere. That is great for long term storage, but when you want to actually make a transaction out of that wallet, you need to enter the secret key into something.

One solution to this is to use a dedicated hardware 'wallet' such as a Nano Ledger. But I've never been particularly fond of 'closed' solutions and generally like to try and roll my own. Partly for my own learning, but also in order to better trust what is going on. Nano had some issues recently submitting transactions to the Ripple network as they were using some public nodes that Ripple Inc supply for testing. But they were overloaded.

So I decided to build my own hardware 'wallet' using a Raspberry Pi 3. Again, those that know me, know I generally prefer and trust OpenBSD and FreeBSD over Linux, and so wanted to use them. What I hadn't realised at the time is the Raspberry Pi 3 is a bit of an odd beast and it requires a working graphic driver in order to start the main processor cores. Currently OpenBSD is not able to boot on a Raspberry Pi3 as far as I know. So next up in my preference is FreeBSD.

## The Risks

So here is where were start to work out compromises. In order of most secure I could:

1. Have a dedicated monitor and keyboard plugged in to the Raspberry Pi and no network connection. I sign the transactions using this dedicated system and then transfer the transactions via USB stick to my main desktop for submission to the Ripple Network.

2. As above, but have a network connection so the Raspberry Pi can submit the transactions to the Ripple Network itself.

3. Not bother with a keyboard and monitor, and connect the Raspberry Pi to the house network and allow SSH in to run transaction generation and signing commands and submit them to Ripple.

What are the actual attack vectors?

1. Malware on my desktop has a screen recorder / keyboard logger and intercepts what I type.

2. Compromise in the software / hardware of the Raspberry Pi causes the keys to be disclosed somehow.

3. Someone gets into the network and attempts to intercept traffic to the Raspberry Pi, or attempts to break into it.

4. Someone physically steals the Raspberry Pi.

5. Rubber hose attack on me.

So how am I going to minimise the risk of each of these? Note I said 'minimise' and not 'eliminate'. Nothing is absolute in security terms and all you can try and do is reduce the probability of a comprise happening, or the damage that compromise can cause.

1. By running this on a separate machine, the Raspberry Pi, it is isolated from any other software that would be running on my desktop. So any attack similar to meltdown or spectre invoked by some rogue app I am running, or nasty javascript from a web page would not be possible. 

I will be interacting with the Raspberry Pi via my desktop so I will need to ensure, that at no point are my private keys or secrets displayed on the console (where it could be observed by screen capture software on my desktop). I will also set up two-factor auth using time-based one-time passwords using an authenticator on my phone. This means that even if my keys are logged on my desktop, there is no way to replay a login onto the Raspberry pi.

2. By running FreeBSD and only running the bare minimum I need on the Raspberry Pi, I can reduce the chance that rogue software could cause trouble. The Raspberry Pi is not susceptible to either the meltdown or spectre vulnerabilities in other systems due to the slightly less advanced processor it uses ([details here](https://www.raspberrypi.org/blog/why-raspberry-pi-isnt-vulnerable-to-spectre-or-meltdown/)). I am able to lock the Raspberry Pi down with a minimum of users, firewall all the inbound (and outbound) connections to just allow SSH in from my desktop, and a websocket connection to Ripple out. Plus DNS and NTP which I can restrict down to specific hosts as well.

3. If someone gets into my network and attempts to SSH into the Raspberry Pi, they would have trouble as it would be physically switched off most of the time unless in use. Also, they would require to know both my SSH password and have the OTP generator (my phone, with PIN / fingerprint).

4. If someone physically steals the Raspberry Pi then they will again, have trouble doing much with it. Even if they were to remove the SD card, the partition with my keys on will be encrypted. It is also small enough, if I wanted to I could lock it in a safe, hide it somewhere, or take it with me.

5. Rubber hose attack. Well. Umm... that pretty much trumps everything. I could set up a second login that gives access to some dummy keys, or a login that wipes the card or similar.

## The Implementation

So, I have a brand shiny new Raspberry Pi 3. It came with an SD card supposedly with NOOBS, a specific Linux distro for it, but the card appeared dead. Neither the RPi or my desktop iMac would recognise it. So I bought a new SD card and tried again.

### Installing FreeBSD

This was actually surprisingly easy. I copied the OS onto the SD card on my iMac, with a built-in SD card slot it has hiding at the back. To be honest, I totally forgot it even had the slot as never use it.

I downloaded the FreeBSD 12 snapshot image from the FreeBSD FTP site for the Raspberry Pi 3:

[https://download.freebsd.org/ftp/snapshots/ISO-IMAGES/12.0/FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180110-r327788.img.xz](https://download.freebsd.org/ftp/snapshots/ISO-IMAGES/12.0/FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180110-r327788.img.xz)

By the time you read this there will likely be a newer snapshot or even a full FreeBSD 12 release out.

First uncompress the image:

```bash
$ unxz FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180110-r327788.img.xz
```

After checking that the SD card was `disk2` on my system, I copied the image to the SD card:

```bash
$ sudo dd if=FreeBSD-12.0-CURRENT-arm64-aarch64-RPI3-20180110-r327788.img of=/dev/rdisk2 bs=1m conv=sync
```

Then take the SD card out the iMac and put it in the RPi. The RPi 3 takes a micro-sd card, which this one was, so took it out the adapter to the full size card it was in originally.

I needed to plug the RPi into an HDMI display, the only one of which I have in the house it the TV in the living room, so plugged it into that, plugged the supplied micro-USD power source in, and a USB keyboard.

FreeBSD booted straight up and brought me up with a prompt. The default root password is just 'root'. So first thing was to log in, and create myself a user. Unlike Linux, most BSDs don't allow root to ssh in by default. The command to add a user is `adduser` and just follow the prompts. When asked if you want to add the user to any other groups, enter `wheel` so that they can `su` to root. I checked the networking settings and saw it was already set to DHCP.

So I could then shut it down (`shutdown -h now`) and unplug it and take it back to my study and plug it into the ethernet switch.

Once powered up, I saw from my router that it had grabbed an IP address via DHCP and I was able to SSH in to it and login with the user I just created. First task, change the root password:

```sh
Matts-iMac:~ matt$ ssh 192.168.1.99
Password for matt@generic:
Last login: Thu Jan 11 17:32:17 2018 from 192.168.1.69
FreeBSD 12.0-CURRENT (GENERIC) #0 r327788: Thu Jan 11 17:16:59 UTC 2018

Welcome to FreeBSD!

Release Notes, Errata: https://www.FreeBSD.org/releases/
Security Advisories:   https://www.FreeBSD.org/security/
FreeBSD Handbook:      https://www.FreeBSD.org/handbook/
FreeBSD FAQ:           https://www.FreeBSD.org/faq/
Questions List: https://lists.FreeBSD.org/mailman/listinfo/freebsd-questions/
FreeBSD Forums:        https://forums.FreeBSD.org/

Documents installed with the system are in the /usr/local/share/doc/freebsd/
directory, or can be installed later with:  pkg install en-freebsd-doc
For other languages, replace "en" with a language code like de or fr.

Show the version of FreeBSD installed:  freebsd-version ; uname -a
Please include that output and any error messages when posting questions.
Introduction to manual pages:  man man
FreeBSD directory layout:      man hier

Edit /etc/motd to change this login announcement.
You can use "whereis" to search standard binary, manual page and source
directories for the specified programs. This can be particularly handy
when you are trying to find where in the ports tree an application is.

Try "whereis firefox" and "whereis whereis".
		-- Konstantinos Konstantinidis <kkonstan@duth.gr>
matt@generic:~ % uname -a
FreeBSD generic 12.0-CURRENT FreeBSD 12.0-CURRENT #0 r327788: Thu Jan 11 17:16:59 UTC 2018     root@releng3.nyi.freebsd.org:/usr/obj/usr/src/arm64.aarch64/sys/GENERIC  arm64
matt@generic:~ % su
Password:
root@generic:/home/matt # passwd root
Changing local password for root
New Password:
Retype New Password:
root@generic:/home/matt # 
```

### Securing the machine

So, firstly, let's setup two-factor auth on it:

We need to install the relevant packages for PAM, the Pluggable Authentication Module:

```none
 # pkg install pam_google_authenticator-20140826_1
 # pkg install libqrencode
```

Then run the command to set up 2FA for my user:

```none
 # su - matt -c google-authenticator
```

Answer a bunch of questions, I think I said yes to all of them. Note down your emergency codes. There will also be a URL for a QR code generated by Google. Copy and paste that into your browser and it will give you a QR code you can scan with your 2FA app on your phone (e.g. Google Authenticator, or Authy).

Actually, if you want to run FreeBSD with root mounted read only, as I do further down, you will need to answer 'no' to the two questions about rate limiting access. This is because the PAM module attempts to write to a file `.google_authenticator` in the user's home directory. And if that is on a read-only filesystem then login will fail. It is probably possible to copy this file to a r/w bfs mount on boot and use it there.

At this point I realised the clock was not set on the Raspberry Pi and it was about a week out of date... not good for time based OTP. So enabled ntp in `/etc/rc.conf` by adding following lines:

```sh
ntpd_enable="YES"
ntpdate_enable="YES"
```

Then manually syncing the date with ntpdate to bring it in line, then starting ntpd to keep it in sync

```none
root@wallet:/home/matt # service ntpdate start
Setting date via ntp.
20 Jan 19:00:07 ntpdate[987]: step time server 62.242.89.196 offset 774548.975807 sec
root@wallet:/home/matt # service ntpd start
Starting ntpd.
```

Now we need to enable 2FA in PAM and sshd. firstly edit `/etc/pam.d/sshd` to add the following line:

```sh
auth            required        /usr/local/lib/pam_google_authenticator.so
```

then edit `/etc/ssh/sshd_config` to get it to use it for my user but adding the following line at the end:

```sh
Match User matt
    AuthenticationMethods keyboard-interactive
```

Now, restart sshd:

```sh
root@wallet:/home/matt # service sshd restart
```

Now when I try and ssh in I get asked for the 2FA code after my password:

```none
Matts-iMac:~ matt$ ssh 192.168.1.99
Password for matt@wallet:
Verification code: 
Last login: Thu Jan 11 17:32:32 2018 from 192.168.1.69
FreeBSD 12.0-CURRENT (GENERIC) #0 r327788: Thu Jan 11 17:16:59 UTC 2018

Welcome to FreeBSD!
...
```

Running the system on read-only mounts:

I want to run FreeBSD mounted read-only. That is partly for security, but mainly due to it running on an SD card, and they don't take to high number of writes. Also if the wallet boots up with the disks mounted read-only then it can by shut down just by powering it off with no risk of filesystem corruption.

With the root mounted r/o I can just pull the power to shut it down, and when I plug the power in, it takes about 35 seconds to get to the point I can ssh in, which is fast enough for me. I imagine about 10 seconds of which is waiting at the boot prompt and could be reduced with a bit of work.

Firstly you need to alter the `fstab` file to mount root at read only, and you might as well set the dump order to `0` as it isn't used.

```sh
 # Custom /etc/fstab for FreeBSD embedded images
/dev/ufs/rootfs   /       ufs     ro      0       1
/dev/msdosfs/MSDOSBOOT /boot/msdos msdosfs rw,noatime 0 0
tmpfs /tmp tmpfs rw,mode=1777,size=50m 0 0
```

Note that `/tmp` is already mounted on an 50m memory filesystem.

To set the `/var` partition to be on MFS as well, just add the following two lines to `/etc/rc.conf`:

```sh
varmfs="YES"
varsize="32m"
```

now on reboot you will find that the partitions are all mounted read only or are on memory filesystems:

```sh
root@wallet:/home/matt # df -h
Filesystem                Size    Used   Avail Capacity  Mounted on
/dev/ufs/rootfs            14G    2.2G     11G    17%    /
devfs                     1.0K    1.0K      0B   100%    /dev
/dev/msdosfs/MSDOSBOOT     50M    7.5M     42M    15%    /boot/msdos
tmpfs                      50M    4.0K     50M     0%    /tmp
tmpfs                      32M    152K     32M     0%    /var

root@wallet:/home/matt # mount 
/dev/ufs/rootfs on / (ufs, local, read-only)
devfs on /dev (devfs, local, multilabel)
/dev/msdosfs/MSDOSBOOT on /boot/msdos (msdosfs, local, noatime)
tmpfs on /tmp (tmpfs, local)
tmpfs on /var (tmpfs, local)
```

To mount the filesystem as read-write after boot:

```sh
 # mount -o rw -u /
```

Setting up the firewall:

I am going to set up a simple firewall on this box just to allow in SSH, DNS and NTP. As well as ICMP pings. I'm letting all traffic out, but could restrict it further if needed.

So, in `/etc/pf.conf` I have:

```none
set skip on lo
set block-policy drop

block drop in log on ue0
pass out on ue0

antispoof quick for ue0

pass in log on ue0 inet proto tcp from any to any port ssh
pass in on ue0 inet proto udp from any to any port ntp
pass in on ue0 inet proto udp from any to any port domain
pass in on ue0 inet proto icmp from any to any icmp-type 8 code 0
```

and added to `/etc/rc.conf`:

```none
pf_enable="YES"
pflog_enable="YES"
```

This enables the pf firewall on boot, and also the pf logging daemon that will keep a log of firewall rule violations. Bear in mind this is logging to an mfs mounted `/var` and so will be lost on reboot.

### Setting up the wallet software

Install node:

```sh
pkg install node npm
```



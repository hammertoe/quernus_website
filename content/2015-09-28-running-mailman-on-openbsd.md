---
layout: post
title: Running Mailman on OpenBSD
comments: True
tags: mailman, openbsd, opensmtpd, httpd
summary: Here is a recipe for running Mailman 2 on OpenBSD 5.7 using OpenBSD's own smtpd and httpd
---

I maintain a mailing list for the local web and digital community in Bristol and Bath. This mailing list is coming up to 18 years old and until now has been hosted at my previous company Netsight. It was running on their main mail server, which had evolved into quite a complex setup of Exim, Cyrus Imap, SpamAssassin, Mailman, Squirrelmail, and a number of related tools. All running on FreeBSD.

It came time to move the mailing list off onto it's own to simplify the complex setup and enable parts to be upgraded with less risk. So I thought I'd move it off onto it's own OpenBSD virtual machine, as it is pretty lightweight and running on it's own VM it would stay fairly self contained.

I wanted to try and use as much of the 'built in' components in OpenBSD as possible, namely the MTA (OpenSMTP) and the HTTP server (httpd). The mailing list runs Mailman version 2. There has since been a complete re-write of Mailman, version 3, which is a totally different beast, and based on Django app. As I wanted to keep this pretty minimal and try and move over as much of the setup as I could, I stuck with the legacy mailman 2 setup.

Oh, and just one more thing, as I'm currently doing a lot of experimentation with IPv6 at the moment I thought I'd try and set  it up with just IPv6. The VM is running on a server in my office, and my ISP has given me just a single IPv4 address, but an entire /60 IPv6 address space to play with. So by putting it on IPv6 I don't have to worry about NAT to get it accessible from the outside world. As the rest of the world is still mainly IPv4 I set up an SMTP route on my main mail server, hosted with Bytemark to forward mail from IPv4 to the IPv6 mailman server. Similarly with HTTP traffic.

OpenBSD's https server tries to chroot itself to `/var/www` in order to limit the potential damage an exploit could do. Alas, mailman is quite tricky to get running in a chroot environment. As this whole VM will be exclusively running this mailman server and nothing else, I decided to forego the chroot side of things and get the httpd server to chroot to `/` which effectively negates the benefits of chroot, but allows us to more easily run mailman.

I installed `mailman-2.1.17p0` from OpenBSD's packages collection. Then for `/etc/mail/smtpd.conf`

```
# $OpenBSD: smtpd.conf,v 1.7 2014/03/12 18:21:34 tedu Exp $

# This is the smtpd server system-wide configuration file.
# See smtpd.conf(5) for more information.


listen on 2a01:500:6:200:2::2
listen on ::1

table aliases db:/etc/mail/aliases.db

accept from any for domain "under-score.org.uk" alias <aliases> deliver to mbox

accept from local for any relay via smtp://mail.quernus.co.uk
```

and in `/etc/mail/aliases` appended the aliases for mailman:

```
...
# underscore mailing list
underscore:              "|/usr/local/lib/mailman/mail/mailman post underscore"
underscore-admin:        "|/usr/local/lib/mailman/mail/mailman admin underscore"
underscore-bounces:      "|/usr/local/lib/mailman/mail/mailman bounces underscore"
underscore-confirm:      "|/usr/local/lib/mailman/mail/mailman confirm underscore"
underscore-join:         "|/usr/local/lib/mailman/mail/mailman join underscore"
underscore-leave:        "|/usr/local/lib/mailman/mail/mailman leave underscore"
underscore-owner:        "|/usr/local/lib/mailman/mail/mailman owner underscore"
underscore-request:      "|/usr/local/lib/mailman/mail/mailman request underscore"
underscore-subscribe:    "|/usr/local/lib/mailman/mail/mailman subscribe underscore"
underscore-unsubscribe:  "|/usr/local/lib/mailman/mail/mailman unsubscribe underscore"
```

Then set up `/etc/httpd.conf` to serve up the mailman web UI. This is based on classical CGI scripts. OpenBSD's httpd doesn't support the classical CGI setup, but only the newer 'fastcgi' which is a way of passing requests to a long running process, rather than spawn a process per request.

Luckily OpenBSD also includes `slowcgi` a gateway from FastCGI to the traditional CGI process. So firstly `/etc/httpd.conf`

```
ext_addr="egress"
chroot "/"
logdir "/var/www/logs"

server "default" {
       listen on 2a01:500:6:200:2::2 port 80

       root "/var/www/htdocs"

       # The actual mailman CGI scripts
       location "/mailman/*" {
               fastcgi socket "/var/www/run/slowcgi.sock"
               root { "/usr/local/lib/mailman/cgi-bin/", strip 1 }
       }

       # The icons referred to by the web interface
       location "/icons/*" {
               root { "/usr/local/lib/mailman/icons/", strip 1 }
       }

       # The mailing list archives
       location "/pipermail/*" {
               root { "/var/spool/mailman/archives/public/", strip 1 }
       }
}
```

Note that I set the chroot parameter to `/`. This in effect disables the chroot security mechanism. You need to be OK with that. In theory you shouldn't need to do this, as only the slowcgi process needs to be able to see the actual mailman CGI scripts, but due to the way the path to the scripts is calculated, you have to disable the chroot in httpd too. The first location block above is the one that points to the main CGI scripts for mailman. It passes the location via the unix domain socket specified.

The slowcgi process doesn't need any setup, just starting. So my `/etc/rc.conf.local` file looks like:

```
ntpd_flags="-s"
smtpd_flags=""
slowcgi_flags="-p /"
httpd_flags=""
pkg_scripts="mailman"
```

Passing the `-p /` flag to slowcgi disables the chroot as well, so that it is able to find the mailman scripts to run.

So there we have a pretty minimal setup, just enough to accept mail via SMTP, process it in mailman and send mail out to smarthost relay, also access to the archives and web management interface via HTTP. 

In total there are about 40 processes running:

```
load averages:  0.15,  0.17,  0.14    linda.quernus.co.uk 21:34:22
43 processes: 42 idle, 1 on processor
CPU states:  0.0% user,  0.0% nice,  0.2% system,  0.0% interrupt, 99.8% idle
Memory: Real: 173M/445M act/tot Free: 540M Cache: 187M Swap: 0K/480M

  PID USERNAME PRI NICE  SIZE   RES STATE     WAIT      TIME    CPU COMMAND
14917 _mailman   2    0   23M   32M sleep     select    0:43  0.00% python2.7
25162 _mailman   2    0   21M   30M sleep     select    0:42  0.00% python2.7
25278 _mailman   2    0   17M   25M sleep     select    0:40  0.00% python2.7
14513 _mailman   2    0   20M   30M sleep     select    0:40  0.00% python2.7
 5857 _mailman   2    0   16M   24M sleep     select    0:39  0.00% python2.7
26636 _mailman   2    0 8704K   15M sleep     select    0:38  0.00% python2.7
 7008 _mailman   2    0 8440K   15M sleep     select    0:38  0.00% python2.7
13568 _pflogd    4    0  684K  404K sleep     bpf       0:20  0.00% pflogd
19428 _smtpq     2    0 1900K 2876K idle      kqread    0:02  0.00% smtpd
 3726 _smtpd     2    0 2868K 5004K idle      kqread    0:01  0.00% smtpd
11513 root       2    0  792K 1136K sleep     poll      0:01  0.00% cron
    1 root      10    0  536K  552K sleep     wait      0:01  0.00% init
12359 matt       2    0 3680K 3028K idle      select    0:01  0.00% sshd
32041 _smtpd     2    0 1608K 2520K idle      kqread    0:00  0.00% smtpd
  428 _smtpd     2    0 1756K 2644K idle      kqread    0:00  0.00% smtpd
 2484 www        2    0 1212K 2316K sleep     kqread    0:00  0.00% httpd
 8653 _mailman   2    0   16M   24M idle      select    0:00  0.00% python2.7
19052 root       3    0  652K  760K idle      ttyin     0:00  0.00% ksh
 2330 www        2    0 1156K 2180K sleep     kqread    0:00  0.00% httpd
 1102 _smtpd     2    0 1668K 2476K idle      kqread    0:00  0.00% smtpd
19445 _syslogd   2    0 1124K 1504K idle      kqread    0:00  0.00% syslogd
16320 matt       2    0 3692K 3056K sleep     select    0:00  0.00% sshd
28230 _ntp       2  -20 1084K 2896K idle      poll      0:00  0.00% ntpd
26805 root       3    0  664K  772K idle      ttyin     0:00  0.00% ksh
 1199 www        2    0 1140K 2180K idle      kqread    0:00  0.00% httpd
23519 www        2    0  996K 1884K idle      kqread    0:00  0.00% httpd
19390 www        2    0  696K 1288K idle      kqread    0:00  0.00% slowcgi
28522 root      18    0  656K  752K sleep     pause     0:00  0.00% ksh
 2809 root       2    0 3800K 3556K idle      poll      0:00  0.00% sshd
30896 root       2    0 3792K 3564K idle      poll      0:00  0.00% sshd
 7317 root       2    0 1544K 2300K idle      kqread    0:00  0.00% smtpd
14527 _smtpd     2    0 1396K 2104K idle      kqread    0:00  0.00% smtpd
12559 _mailman  10    0 8484K 5232K idle      wait      0:00  0.00% python2.7
 9705 root       2    0 1036K 1436K idle      select    0:00  0.00% sshd
 3165 matt      18    0  632K  732K idle      pause     0:00  0.00% ksh
 6618 matt      18    0  628K  728K idle      pause     0:00  0.00% ksh
18860 root       2    0 1124K 1336K idle      netio     0:00  0.00% syslogd
 5870 root       2    0 1136K 2164K idle      kqread    0:00  0.00% httpd
17986 root       2  -20  668K 1528K idle      poll      0:00  0.00% ntpd
23120 root       2    0  620K  600K idle      netio     0:00  0.00% pflogd
17361 root      -6    0  236K  200K sleep     piperd    0:00  0.00% cat
17714 root      28    0  592K 1760K onproc    -         0:00  0.00% top
11321 _ntp       2    0  944K 1260K idle      poll      0:00  0.00% ntpd
```


The VM has 1G of memory, but looks like it could probabaly get away with 512MB just fine.
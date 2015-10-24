---
layout: post
title: Force git to use ssh instead of HTTPS
comments: True
tags: ios, git, ssh
summary: Sometimes you have tools that reference a github url with https and you want them to use ssh instead so your ssh key works
---

Sometimes you have tools that reference a github url with https and you want them to use ssh instead so your ssh key works.

In my case it is Cocoapods trying to clone a spec repo. Since I just enabled two-factor auth on my account it now stopped working:

{% highlight bash %}
Matts-iMac:Nutrition matt$ pod install
Cloning spec repo `enquos` from `https://github.com/enquos/mib.ios.pod.podspec`
Username for 'https://github.com': hammertoe
Password for 'https://hammertoe@github.com': 
[!] Unable to add a source with url `https://github.com/enquos/mib.ios.pod.podspec` named `enquos`.
You can try adding it manually in `~/.cocoapods/repos` or via `pod repo add`.
{% endhighlight %}

By putting the following in your `~/.gitconfig` file you can force git to use SSH whenever it is asked to use a HTTPS url:

```
[url "git@github.com:"]
  insteadOf = https://github.com/
[url "git@github.com:"]
  pushInsteadOf = "git://github.com/"
[url "git@github.com:"]
  pushInsteadOf = "https://github.com/"

```
---
layout: post
title: Safer deleting of a directory
comments: True
tags: unix, tips, sysadmin
summary: A safer alternative to rm -rf for use in scripts
---

I have just been refactoring our build servers and need to wipe out a directory as part of the build script. This is something Jenkins used to be able to do itself, but can't be used now as part of the Multibranch Pipeline builds they have introduced.

So I needed a way to delete the contents of a directory. I needed to keep the directory itself, but wanted to remove the contents of the directory (including subdirectories).

The usual way to do this, assuming the directory was `/home/jenkins/workspaces/foo` would be to do:

```rm -rf /home/jenkins/workspaces/foo```

But that would remove the directory itself. You could do:

```rm -rf /home/jenkins/workspaces/foo/*```

...but that would leave any dotfiles in the directory.

Also, we will be passing the path in as a variable, e.g.

```rm -rf ${workspace}```

And if somehow the `workspace` variable was set to `/` then it would cause the entire server to be wiped. Given there has recently been a couple of [very high profile cases of exactly this in the media recently](http://www.independent.co.uk/life-style/gadgets-and-tech/news/man-accidentally-deletes-his-entire-company-with-one-line-of-bad-code-a6984256.html) I was keen not to add yet another.

I happened to ask my friend, Stewie, if he had any better ideas, and he came with with a great one using `find`:

```find "${workspace}" -mindepth 4 -depth -delete```

The great thing here is the `mindepth` argument, that would prevent an accidental value of `/` or in fact any path with less than 4 path elements from being deleted. This greatly reduces the change of accidental damage due to a bad script.

The double quotes around the argument also help protect it a bit from any malicious input that might attempt to inject extra arguments in the variable. This script is not intended to take input from untrusted sources, but it always pays to be as careful as you can and assume the worst.

In fact we can make this even safer, as we know the root in which the workspaces are, so can pass that in as a hardcoded `path` argument to find, e.g.:

```find "${workspace}" -path /home/jenkins/workspaces -mindepth 4 -depth -delete```

So the worst that could now happen is that *all* of the workspaces could be deleted. Better than the entire server ;)

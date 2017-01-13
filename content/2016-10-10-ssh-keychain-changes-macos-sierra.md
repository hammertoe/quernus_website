---
layout: post
title: Changes to Keychains in macOS Sierra
comments: True
tags: jenkins, ci, keychain, ssh
summary: I upgraded a build server to macOS Sierra and the keychain unlocking stopped working, here is how I fixed it.
---

*Update: It looks like this issue has now been fixed in MacOS 10.12.2 (Darwin 16.3.0). Thanks to 'Kumazatheef' for the update.*

I recently upgraded one of our Mac Mini build servers to macOS Sierra. This was needed in order to build for iOS 10 and Xcode 8. Well I could have held back on previous OSX version for a while, but with Apple it is an inevitable upgrade tide you are swimming against!

The upgrade went well, however something broke when trying to get our Jenkins server (FreeBSD) to build our iOS app on the Mac Mini as a build slave.

At the start of our build script we need to set the keychain path (our iOS keys are in their own keychain to keep things nice and clean) and unlock the keychain so that the keys and certs for signing the apps can be found by Fastlane:

```groovy
sh "security list-keychains -s ~/Library/Keychains/iosbuilds.keychain"
sh "security unlock-keychain -p ${env.KEYCHAIN_PASSWORD} /Users/iosbuilds/Library/Keychains/iosbuilds.keychain"
```

This needed to be changed due to the extension of the keychain files changing to `.keychain-db`. No idea why they felt they needed to make this change, but there we go.

```groovy
sh "security list-keychains -s ~/Library/Keychains/iosbuilds.keychain-db"
sh "security unlock-keychain -p ${env.KEYCHAIN_PASSWORD} /Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db"
```

Then I had a very strange issue. When I logged in to the build server myself, they keychain was not found, and instead it listed the system keychain twice:

```sh
matt@jenkins:~ ssh iosbuilds@goram.quernus.co.uk
Password:
Last login: Fri Sep 30 12:52:26 2016
Goram:~ iosbuilds$ security list-keychains -s ~/Library/Keychains/iosbuilds.keychain-db
Goram:~ iosbuilds$ security unlock-keychain -p topsecret /Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db
Goram:~ iosbuilds$ security list-keychains
    "/Library/Keychains/System.keychain"
    "/Library/Keychains/System.keychain"

```

However, if I do the same from a host that *has* a public key setup with the build server (ie. I don’t need to supply a password):

```sh
Ghyston:~ iosbuilds$ ssh iosbuilds@goram.quernus.co.uk
Last login: Mon Oct 10 17:40:34 2016 from 2a01:500:6:200:1::31
Goram:~ iosbuilds$ security list-keychains -s ~/Library/Keychains/iosbuilds.keychain-db
Goram:~ iosbuilds$ security unlock-keychain -p topsecret /Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db
Goram:~ iosbuilds$ security list-keychains
    "/Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db"
    "/Library/Keychains/System.keychain"

```
The keychain is there in the path!

Now, this isn’t an issue when the Jenkins process itself runs as that uses a ssh key to login so it doesn’t need to ask for a password interactively. But as I was trying to debug the first issue (the extension change of keychain files) it cause me to chase a red herring for quite a while.

I’ve still no idea what is causing this or why logging in via a password means that running the `security` command doesn’t work as intended. And, no, there is no credential forwarding enabled or anything like that. My guess is that there is something set in the environment, but I’ve yet to track it down.
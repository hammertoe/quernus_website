---
layout: post
title: Duplicate Keychain Entries in macOS Sierra
comments: True
tags: jenkins, ci, keychain, macOS
summary: I upgraded a build server to macOS Sierra and the keychain unlocking stopped working, here is how I fixed it.
---

I recently upgraded one of our Mac Mini build servers to macOS Sierra. After doing so, I noticed something very strange happening when trying to sign our app builds. The signing process was failing for some reason. I went to check the keychain using the `security` command to see if I could see what was going on, and if it couldn’t find the relevant certificates and private keys.

```sh
Ghyston:~ iosbuilds$ security find-identity -v -p codesigning
  1) 7A0DB9A50051B6DDCCB00409D9A82B118C67B301 "iPhone Developer: Build Master (FBC3BVZSH8)"
  2) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
  3) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
  4) 7337E32BCB5C6E68099707B93107D55B1AD888EB "iPhone Developer: Build Master (FBC3BVZSH8)"
  5) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
     5 valid identities found
```

What?! Where were the duplicates coming from? I tried the same command on the other build node we have, which has already been running Sierra for the past few months:

```sh
Goram:~ iosbuilds$ security find-identity -v -p codesigning
  1) 7A0DB9A50051B6DDCCB00409D9A82B118C67B301 "iPhone Developer: Build Master (FBC3BVZSH8)"
  2) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
     2 valid identities found
```

That is what I’d expect.

The very odd thing is that if I look in each of the keychains in my keychain path manually I can’t see any duplicates:

```sh
Ghyston:~ iosbuilds$ security list-keychains
    "/Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db"
    "/Users/iosbuilds/Library/Keychains/login.keychain-db"
    "/Library/Keychains/System.keychain"

Ghyston:~ iosbuilds$ security find-identity -v -p codesigning /Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db
  1) 7A0DB9A50051B6DDCCB00409D9A82B118C67B301 "iPhone Developer: Build Master (FBC3BVZSH8)"
  2) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
     2 valid identities found

Ghyston:~ iosbuilds$ security find-identity -v -p codesigning /Library/Keychains/System.keychain
     0 valid identities found

Ghyston:~ iosbuilds$ security find-identity -v -p codesigning /Users/iosbuilds/Library/Keychains/login.keychain-db
     0 valid identities found
```

I tried exporting, deleting, re-importing the entries in my keychains. I tried creating new login keychain. Rebooting, etc. Still couldn’t work out why it was displaying the duplicate keychain entries.

After a lot of looking about, I found the issue. There was a copy of the *private key* for ‘Legacy Parts Corporation’ in my system keychain. Not the certificate… hence why it didn’t show up above. But for some very unknown reason, having a duplicate *key* in another keychain without the corresponding certificate causes macOS to get a bit confused and show the cert multiple times. 

Deleting the private key from the system keychain and suddenly things look much better again:

```sh
Ghyston:~ iosbuilds$ security find-identity -v -p codesigning 
  1) 7A0DB9A50051B6DDCCB00409D9A82B118C67B301 "iPhone Developer: Build Master (FBC3BVZSH8)"
  2) 8FB1A0E186254DAFA3D5ED116F77E78964278F08 "iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)"
     2 valid identities found
```

And our code signing and builds now work again.
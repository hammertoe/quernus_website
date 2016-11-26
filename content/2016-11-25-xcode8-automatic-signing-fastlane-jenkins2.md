---
layout: post
title: Finding Provisioning Profiles by Name Rather than UUID
comments: True
tags: technology, jenkins, iOS, Xcode, signing, fastlane
summary: Despite my previous thoughts, you can actually use Xcode 8’s find-by-name functionality for manual signing on a CI setup.
---

I recently blogged about (and spoke at SWMobile) about [Xcode 8's automatic code signing features]({filename}/2016-09-28-xcode8-automatic-signing-fastlane-jenkins.md) and how to get them working with a CI setup such as Jenkins.

However, I was advocating at the time to hard-code the provisioning profile UUID into the `.xcconfig` file to make it explicit. One of the problems with that approach is that whenever you update the provisioning profile on the Apple Developer Portal the UUID changes. So this means every time you add a new device for testing, you then need to update the `.xcconfig` file with the new UUID.

From what I had read, it implied that you *had* to use UUIDs as using the new `PROVISIONING_PROFILE_SPECIFIER` variable would require switching over to fully automatic signing.

After a lot of playing about I managed to get it so that you could specify the name of the profile rather than the UUID, but *not* have it try to automatically manage the profiles. This means that the provisioning style is still `manual` but that it will look for the profile by name. So if you use Fastlane and use `sigh` to pull down the latest profile when the build job runs, it means it will always use the latest profile.

We have three different build configurations `develop`, `feature`, and `release`. The first two are AdHoc builds and are for testing. The latter uses an `AppStore` profile for uploading to TestFlight and the App Store.

TotalHealth-develop.xcconfig:
```
DEVELOPMENT_TEAM = 9Q5433VBYW
PROVISIONING_PROFILE_SPECIFIER_app = com.enquos.totalhealth.develop AdHoc
PROVISIONING_PROFILE_SPECIFIER = $(PROVISIONING_PROFILE_SPECIFIER_$(WRAPPER_EXTENSION))
CODE_SIGN_IDENTITY = iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)
PROVISIONING_PROFILE = 
```

TotalHealth-feature.xcconfig:
```
DEVELOPMENT_TEAM = 9Q5433VBYW
PROVISIONING_PROFILE_SPECIFIER_app = com.enquos.totalhealth.feature AdHoc
PROVISIONING_PROFILE_SPECIFIER = $(PROVISIONING_PROFILE_SPECIFIER_$(WRAPPER_EXTENSION))
CODE_SIGN_IDENTITY = iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)
PROVISIONING_PROFILE = 
```

As the app store profile doesn't contain UUIDs and doesn't change regularly, we still refer to that one by UUID in our `xcconfig` file:

TotalHealth-release.xcconfig:
```
DEVELOPMENT_TEAM = 9Q5433VBYW
PROVISIONING_PROFILE_SPECIFIER =
PROVISIONING_PROFILE = cb29a583-df74-4a2b-8424-bcc55b56090c
CODE_SIGN_IDENTITY = iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)
```



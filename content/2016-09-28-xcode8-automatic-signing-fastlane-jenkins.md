---
layout: post
title: Using Xcode 8’s New Automatic Signing with Jenkins and Fastlane
comments: True
tags: technology, jenkins, iOS, Xcode, signing, fast lane
summary: Xcode 8 brings with it a new automatic code signing system. It is meant to make life a lot easier for developers, but needs a bit of work to get working with headless CI systems like Fastlane and Jenkins.
---

With Xcode 8, Apple have provided a new code signing system which aims to make it much easier to deal with code signing on projects. It provides an ‘Automatic’ code signing management. This seems like a great idea and is a much better system than the old ‘fix issues’ button. However it’s automatic nature actually doesn’t work very well on CI build systems such as the one we have using Jenkins and Fastlane.

A great introduction to the new code signing process and where you should start is Samantha Marshall’s excellent blog post on [Migrating Code Signing Configurations to Xcode 8](https://pewpewthespells.com/blog/migrating_code_signing.html) (and also a recap on what Xcode 7 does). 

The crux of the issue is that the new automatic signing system attempts to manage the provisioning profiles directly within Xcode itself. Which is a nice idea. But, doesn’t work unless you actually interactively run Xcode. It is useless for when you are running a headless CI system doing automated builds. Not only that, but I have a bit of an aversion to anything too ‘magic’ in automated deployments. Borrowing from the Zen of Python:

> “Explicit is better than Implicit.”

I want to pin down my CI system such that when it builds a package I know exactly what it is doing and what provisioning profile it will be using.

What we would like to achieve:

1. Allow the developers to use automatic provisioning on their local environments so that they can easily sign apps for deployment to their local testing devices
2. To override anything set above such that we use a specific provisioning profile already set up on the Apple Developer Portal and downloaded using `sigh` as part of Fastlane. This means we add/remove device UUIDs and entitlements via the Apple Developer Portal.
3. To allow us to have multiple build types: `develop`, `feature`, and `release` that we use for the different code streams we have during development.

To get this to work we have to do two things:

1. Explicitly change the `ProvisioningStyle` to `manual` in the `project.pbxproj` file. Whilst ugly, the best way I’ve found to do this is to alter the file itself.

2. Pass in a `.xcconfig` file as a parameter to `gym` in our `Fastlane` file.

So our logic for this part of the Fastlane file looks like:

```ruby
      # Set the provisioning style to manual
      Actions.sh "sed -i '' 's/ProvisioningStyle = Automatic;/ProvisioningStyle = Manual;/' ../#{project}/project.pbxproj"

      if configuration == 'Release' 
        sigh(
            app_identifier: 'com.enquos.totalhealth',
          )
        gym(
           configuration: configuration,
           xcconfig: 'TotalHealth-release.xcconfig',
          )
      elsif configuration == 'Feature'
        sigh(
            app_identifier: 'com.enquos.totalhealth.feature',
            adhoc: '1',
          )
        gym(
           configuration: configuration,
           xcconfig: 'TotalHealth-feature.xcconfig',
          )
      else
        sigh(
            app_identifier: 'com.enquos.totalhealth.develop',
            adhoc: '1',
          )
        gym(
           configuration: configuration,
           xcconfig: 'TotalHealth-develop.xcconfig',
          )
      end

```
Then in the `.xcconfig` files we have the settings we need to manually set. E.g. `TotalHealth-develop.xcconfig` contains:

```sh
CODE_SIGN_IDENTITY = 9Q5433VBYW
PROVISIONING_PROFILE_SPECIFIER =
PROVISIONING_PROFILE_app = f3f8d4cb-a975-4529-8dcd-60e277d92fae
PROVISIONING_PROFILE = $(PROVISIONING_PROFILE_$(WRAPPER_EXTENSION))
CODE_SIGN_IDENTITY = iPhone Distribution: Legacy Parts Corporation (9Q5433VBYW)
```

A couple of notes:

1. The `PROVISIONING_PROFILE_SPECIFIER` is kept blank. This is because this is only used then doing automatic provisioning
2. The indirection of `PROVISIONING_PROFILE_app` and `PROVISIONING_PROFILE` means that the profile will only be used to sign the app itself and not the pods as they are built.
3. We set the `CODE_SIGN_IDENTITY` and `CODE_SIGN_IDENTITY` to override anything the developers might have set in their local configuration.
4. We have a separate file for `develop`, `feature` and `release` builds of our app. They have a different provisioning profile UUID specified.

I’d love to have a better way to set the provisioning style to manual if possible. I did try to see if I could override it in the .xcconfig file, but alas it doesn’t seem you can.


---
layout: post
title: Using Xcode 8’s New Automatic Signing with Jenkins and Fastlane
comments: True
status: draft
tags: technology, jenkins, iOS, Xcode, signing, fast lane
summary: Xcode 8 brings with it a new automatic code signing system. It is meant to make life a lot easier for developers, but needs a bit of work to get working with headless CI systems like Fastlane and Jenkins.
---

With Xcode 8, Apple have provided a new code signing system which aims to make it much easier to deal with code signing on projects. It provides an ‘Automatic’ code signing management. This seems like a great idea and is a much better system than the old ‘fix issues’ button. However it’s automatic nature actually doesn’t work very well on CI build systems such as the one we have using Jenkins and Fastlane.

A great introduction to the new code signing process and where you should start is Samantha Marshall’s excellent blog post on [Migrating Code Signing Configurations to Xcode 8](https://pewpewthespells.com/blog/migrating_code_signing.html) (and also a recap on what Xcode 7 does). 


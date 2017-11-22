---
layout: post
title: My Last Three Years in Numbers
comments: True
tags: quantified self, iOS, android, mobile, python, xrp, ripple
summary: A look at the last three years of my work in numbers.
---

I am coming to the end of three years of working on a long running contract on a 'quantified self' system for a client, [enquos](https://www.enquos.com/). This is a system to help people measure and track their nutrition, exercise and wellbeing in order to effect change in their life. It has been a fascinating three years, but gave me an idea for a blog post: Some of the numbers of the last three years of some of the work I've been doing. Both for enquos, and also side-projects I've been working on.

So here we go...

![enquos team sprint](/public/enquos_team_sprint.jpg)

I've been working on enquos for **1117 days**. In that time I built our mobile development team from scratch and I have found/hired/managed a total of **12 developers**. We have built **6 apps** in total across both iOS and Android platforms. I set up a continuous integration test and build server that has started at least **3876 complete signed, distributable builds of the apps**. 

The iOS app has been developed over **two languages** (Swift and Obj-C) and **three major version of Xcode** (7,8 9). 

Between the Android and iOS versions of the latest app 'enquos Total Health', we have over **1250 automated tests**.

![enquos mobile app jenkins pipeline view](/public/jenkins_ci_pipelines.png)

The final iOS app take approx **37 minutes to build, test, package and deploy**. The Android app takes approx **8 minutes to build test, package, and deploy**. So assuming we built the same number for each, and over the life of the app the build time average is half the final time, then the build server has spent a total of **31 days** solid building the app. Our build numbering system changed halfway through, so I reckon that 3876 is only half the number of builds we have done. And the total time and number of builds is likely double that, more like **2 months** solid building.

I introduced Slack into the company and in that time there have been a total of **324,964 messages** sent on Slack between us.

When I first started, the iOS app I inherited from an outsourced app development company in another country, was over **1 GB in size**. It is now **84 MB**, yet still retains a complete offline searchable database of nutrition items. Each entry containing up to **160 different nutrients**.

![enquos iOS app screenshots](/public/total_health_app.png)

In this time I have given **five talks** at **3 conferences and 2 user groups**. I have also given **four talks** at schools and universities as a STEM Ambassador.

I now know more about iOS app signing and provisioning profiles than any sane human should.

<img alt="Global Festival of Ideas conference game" src="/public/gfi4sd-game.jpg" style="float:right" />

In other projects, I built the Python back end for a budget simulation game for a UN conference on sustainable development. The game was used by **450 people** at the conference over **3 days** and processed a peak of **10,000 financial transactions per second**. It was a collaboration between **three** different companies, one doing the mobile apps, one the overall idea and strategy and myself doing the backend.

<img alt="Ripple trading bot app screenshot" src="/public/crypto_trader2.png" style="float:left; margin-right: 20px; box-shadow: 0px 0px 10px #eeeeee" />

I have also stared to learn Node.js and get more interested in cryptocurrencies. Specifically, the real-time settlement network, Ripple. You know how an international SWIFT payment takes four days to complete? Ripple does the same in **4 seconds**. So fast, you can actually try and make money foreign exchange trading by sending currency back and forth across the network. I wrote a bot to do just that, which is currently trading **£1.2 million per month** between **eight currency pairs**. And making a small profit in the process.

Oh, and I've lost **10kg** in weight in this time.

So if any of this experience sounds like it would benefit your project, then get in touch and let's chat! For more background on me and past experience in Plone and Python, then see my [bio](/about) or [linkedin profile](https://www.linkedin.com/in/matthamilton77/)
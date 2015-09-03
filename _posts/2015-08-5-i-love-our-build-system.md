---
layout: post
title: I Love our Build System
comments: True
tags: iOS, apple
summary: It's 7:30am, a director has reported a problem with our app whilst at a trade show. Help! How our build system saved the day.
---

<p class="message">
  This is part of a series of blog posts about iOS deployment and experiences setting up a continuous testing and build server for iOS apps. These posts are of interest to individual developers wanting to understand more, but mainly targeting small development teams trying to manage their development, testing and deployment process.
</p>

## Wednesday Morning, 7:30am

I love our build system. Yes, I'm biased as I was the one the put it together (using awesome software written by others of course). And in this series I will be detailing how it was built. But I can't help but interject with this interlude as it just shows *why* it is so awesome.

Yesterday we were working on polishing up a number of aspects of an app we are working on. One of our directors, Nicole, is at a trade show in New Orleans and will be wanting to show off the work-in-progress app. So we have been polishing up what is there and testing it all. Last night I pushed a build of the app to Apple's TestFlight service so Nicole can install it on her iPhone. For some unknown reason TestFlight was being slow in processing apps. As I was tucking up into bed last night, TestFlight had only just processed the app.

* 7:30am

    Wake up (my daughter is on school holiday, so a luxury of extra hour in bed), roll over and grab my iPhone to check Slack for any updates and feedback from Nicole. 

    There is a message from her. "There is an error in the app. Some of the numbers displayed are not correct". I check the app and sure enough, two of the numbers have been transposed in the display.

* 7:37am

    Due to TestFlight being slow last night, I want to get on this issue as soon as possible. It needs to be fixed before Nicole wakes up in a timezone 7 hours behind me. She needs the updated app before the trade show starts. 

    I file a bug in our Pivotal Tracker, and tag two of our developers on a message on Slack about it:

    > @pablo or @marc whichever of you gets in first today could you please take the above ticket. Once fixed merge to master and it should start a new Testflight build. Hopefully will process quicker than last night's one.

* 7:48am

    Marc replies on Slack that he is on it. He is in a timezone an hour ahead of me and already started working. I jump into the shower.

* 8:04am

    Marc has found and fixed the bug. Seems just a display issue, rather than underlying data problem. Two labels transposed. He wonders why no-one has spotted it yet. This is why we have continuous builds, so the people with domain-specific knowledge in our team can spot things like this quicker... and we can deploy new, fixed, builds quicker.

* 8:09am

    Marc marks the bug finished in Pivotal. He pushes the feature branch he fixed this in to Github (note: I guess should be a fix/ branch rather than feature/ one? Oh well, does the same job). He issues a pull request for one of the other developers to check.

* 8:18am

    I'm now out of the shower, dressed, and brushing my teeth. Marc asks if he should go ahead and merge the pull request himself for a minor change. I tap on the link in Slack, and Github opens. I can see that the commit really is just transposing two labels and very low risk. Just as I'm about to reply, our build server sends a message on Slack:

    ![Slack notification of build by Jenkins / Fastlane](/public/fastlane_slack_notification.png)

    The build server saw the push of the feature branch by Marc and went ahead and built it, signed it, created a new app for it in Hockey, and uploaded the binary.

    I tap on the link and the app downloads and installs on my iPhone. I check it out and see that the numbers are now in the correct place.

    I reply to Marc to tell him it looks good, to merge the pull request himself.

    I rinse off my toothbrush and put it down.

* 8:29am

    Marc confirms he has merged the PR into the develop/ branch. I tell him to go ahead and merge to master/. This will trigger our build server to do a beta build and upload it to TestFlight so Nicole can get it.

    I finish getting dressed, head downstairs to get breakfast and help get my daughter ready for Summer Camp today.

* 8:53am

    I get an email from Apple saying that there is a new version of our app in TestFlight and available for download:

    ![Email from Apple iTunes Store about updated beta of app](/public/itunes_testflight_notification.png)

* 8:55am

    I get my daughter into the bike trailer and cycle off to drop her at summer camp for the day and head to the office. a great start to the day so far! The new app build is there waiting for Nicole when she wakes up in a few hours.





---
layout: post
title: Global Build Numbers in Jenkins Multibranch Pipeline Builds
comments: True
tags: technology, jenkins, ios, fastlane, ci, pipelines, github
summary: We wanted to have build numbers that were unique and incremental across all of our build jobs. Here is how I did it with a small python microservice.
---

We have a setup for CI that uses Jenkins to continually build our iOS and Android apps. We use the Jenkins multibranch pipeline plugin to allow us to have automatically created separate build jobs for each branch in our project. We use Git Flow and so there are feature branches created for each piece of development work carried out.

![Jenkins 2.0 Multibranch jobs](/public/jenkins_multibranch_view.png)

This was great, and we had a system that would dynamically generate a new App Id or package id for each feature branch and upload them to HockeyApp for distribution. This meant that you could easily install an app built from a specific branch to test it out pre-merge. The problem being as we are using more and more external APIs a lot of them depend upon the App Id or package id. As these ids change dynamically then it causes problems with the 3rd party APIs.

So we decided to scale things back a bit and instead of having multiple feature packages e.g. `com.enquos.totalhealth.feature.analytics` and `com.enquos.totalhealth.feature.exercise_ui` we would just have a single package id of `com.enquos.totalhealth.feature`. The develop and release ids would stay the same. 

We wanted to keep the separate jobs in Jenkins though, as it made it easier to see which specific branches were failing tests. 

The problem then is that each branch build job started it's build number at `1`. So if we got to the `10`th build of `com.enquos.totalhealth.feature.analytics` then there would be an app to download with build number `10`. If we then had the first build of another branch e.g.  `com.enquos.totalhealth.feature.exercise_ui` then the build numbering would restart at `1`.


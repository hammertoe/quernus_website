---
layout: post
title: Uploading Git Changelog to Fabric Beta for Android Gradle Builds in Jenkins
comments: True
tags: technology, jenkins, android, cradle, ci, pipelines, github, fabric, crashlytics
summary: The git changelog is not exposed as a variable in Jenkins for pipeline builds to use. This is how we got it and send it via Gradle to Fabric Beta when we distribute our automated builds
---

We now use Fabric Beta to distribute our automated builds of our iOS and Android apps that are built by Jenkins. However it makes it much easier to see what is in a build if you can have the changelog uploaded with the binary.

For some reason I don’t quite understand, whilst `GIT_BRANCH` and various other Git environment variables are exposed by the Git SCM module in Jenkins, the changelog is not.

Based on some [code I found in a Jenkins ticket](https://issues.jenkins-ci.org/browse/JENKINS-30412) I put a method in our Jenkinsfile to get the changelogs so we can put them in an environment variable:

```groovy
def getChangelog() {
    def changeLogSets = currentBuild.rawBuild.changeSets
    def changelog = ""
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            changelog += entry.msg + ‘\n’
        }
    }
    return changelog
}

env.GIT_CHANGELOG = getChangelog()
```

We then need to pass this to the Gradle task we run to include the notes when we upload the .apk to Crashlytics / Fabric Beta:

```groovy
def releaseNotes = "${env.GIT_BRANCH}\n\n${env.GIT_CHANGELOG}"
env.ORG_GRADLE_PROJECT_BETA_RELEASE_NOTES=releaseNotes
sh "./gradlew crashlyticsUploadDistributionDevRelease"
```

I discovered that [if you set an environment variable with the prefix `ORG_GRADLE_PROJECT_`](https://docs.gradle.org/current/userguide/build_environment.html#sec:gradle_properties_and_system_properties) then Gradle will pick that up and set it as a project property. This neatly gets around trying to pass it using the `-P` flag to the `gradlew` command and having to worry about escaping quotes in shell parameters. [Also saves trouble if little Bobby Tables writes a commit log](https://xkcd.com/327/). ;)

We add in the Git branch to the top of the release notes so that when you look at the list of builds in the Fabric Beta app you can easily see which branch they came from.

Then in out `build.gradle` file we can find this project property and put that where Crashlytics task will be expecting it:

```Groovy
    buildTypes {
        debug {
        }
        release {
            if (project.hasProperty("BETA_RELEASE_NOTES")) {
                ext.betaDistributionReleaseNotes = project.property('BETA_RELEASE_NOTES')
                println(String.format("Beta Distribution Release Notes: %s", ext.betaDistributionReleaseNotes))
            }
            ext.betaDistributionNotifications = false
            ext.betaDistributionGroupAliases = "android-testers"
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
```

The end result is that in the Fabric Beta mobile app on Android you can easily see the branch name and commit notes for each build. As we automatically build each feature branch the is pushed to Github this makes it much easier to see which build is which when you want to go and install a particular build to check out a particular feature branch:

![A screenshot of the branch name and commit log showing in the Android Fabric Beta app.](/public/android_fabric_beta_screenshot.png)

---
layout: post
title: Lockable Resources Jenkins 2.0 pipeline builds
comments: True
tags: jenkins, ci, fastlane, gradle
summary: If you want to increase concurrency in your Jenkins pipeline builds, but need to ensure that certain resources are not used concurrently, then you can use lockable resources
---

With Jenkins 2.0 pipeline builds you can improve the utilisation of your build servers by increasing the concurrency of the jobs. In our case, we are using Jenkins to build iOS apps with Fastlane and Android apps with Gradle. In both cases we run unit tests that involve the build server (a Mac Mini) firing up a simulator to run the tests on. Unless you do a lot of clever workarounds, you can only run one instance of the iOS simulator at a time. In our case, that is not a bad thing as we only have limited CPU power on the server anyway.

However it would be great if we could have a number of concurrent jobs running such that one could be checking source code out, one could be running tests on the simulator, and one could be uploading a build to a distribution service all at the same time.

To do this you need to have the [Lockable Resources Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Lockable+Resources+Plugin) installed and then use the `lock` directive. 


```groovy
...
stage('Tests') {
	lock(resource: "simulator_${env.NODE_NAME}", inversePrecedence: true) {
	  // reset the simulators before running tests
	  sh "killall Simulator || true"
	  sh "SNAPSHOT_FORCE_DELETE=yes snapshot reset_simulators"
	  sh "fastlane tests"   

	  step([$class: 'JUnitResultArchiver', testResults: 'build/reports/*.xml'])
	}
}

...

stage('Build') {
	lock(resource: "compiler_${env.NODE_NAME}", inversePrecedence: true) {
	  milestone 1
	  sh "security list-keychains -s ~/Library/Keychains/iosbuilds.keychain-db"
	  sh "security unlock-keychain -p ${env.KEYCHAIN_PASSWORD} /Users/iosbuilds/Library/Keychains/iosbuilds.keychain-db"
	  if (isRelease()) {
	    sh "fastlane build_release"
	  } else {
	    sh "fastlane build_alpha"
	  }
	}
}
```

In this case we have two 'resources' one for the compiler and one for the simulator. We have suffixed these with the node name. This is because the resources are global across all build nodes and we want a lock per node.

![Screenshot of concurrent builds in queue](/public/concurrent_builds1.png)

The `inversePrecedence` argument means that the newest build will pass through first if there are multiple ones waiting. Combined with the `milestone` directive it means that if two builds are started at similar time that the newest one will pass through the milestone and the older one will be cancelled. This means we don't waste time building older build jobs if the build queue gets full with a lot of jobs (common when we are running a development sprint and have a lot of commits going on).
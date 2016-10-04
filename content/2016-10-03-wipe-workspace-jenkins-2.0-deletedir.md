---
layout: post
title: Wiping the workspace in Jenkins 2.0 pipeline builds
comments: True
tags: jenkins, ci
summary: Instead of the 'wipe workspace' checkbox that used to be in Jenkins, you can now use deleteDir() to clear the workspace before building.
---

With Jenkins there used to be a 'Wipe out repository & force a clone' behaviour you could add to the source code section of a build. This would ensure that you are building from a completely clean workspace.

In Jenkins 2.0 pipeline builds this option is no longer available. Originally I used `find` to find and delete the contents of the directory, which took a bit of fiddling to ensure it would run safely without the chance of an empty variable causing it to delete the entire server.

However there is now in Jenkins a `deleteDir()` function that will delete the contents of the current directory. So you can now just do:

```groovy
node('xcode8') {
  // Wipe the workspace so we are building completely clean
  deleteDir()
  // Mark the code checkout 'stage'....
  stage('Checkout') {
    // Checkout code from repository
    checkout scm
  }

...

}
```
---
layout: post
title: Getting Proper UTF-8 Output From Fastlane on Jenkins 2.0 Pipeline builds
comments: True
tags: jenkins, utf-8, ios, fastlane
summary: Jenkins 2.0 pipeline jobs get their locale from the master not slave, so you need to set the local on master to get UTF-8 output working correctly
---

I've just been upgrading our Jenkins 1.x server to Jenkins 2.0. I've been migrating our previous jobs to new Multibranch Pipeline Jobs.

One of the snags I hit was that the previous nice ANSI sequences and UTF-8 symbols that we used to have were getting mangled and coming up as a series of escape characters and question marks.

![Screenshot of broken ANSI and UTF-8 in Jenkins 2.0 pipeline build jobs](/public/screenshot_utf8_ansi_broken.png)

There were actually two parts to fix this:

1. The ANSI Color plugin needs to be called in the Pipeline code, you can't just select a checkbox
2. The pipeline jobs start on the master and then get allocated a slave to run. So they take the locale of the *master* not the *slave*

So to fix:

Call the ANSI color plugin using a wrap statement. e.g.:

{% highlight groovy %}
node('xcode7') {
   // Manually set the workspace to deal with clang 
   // choking on %2f in the directory
   ws(getWorkspace()) {
     // Wrap to enable ANSI escape sequences
     wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm', 'defaultFg': 1, 'defaultBg': 2]) {
       workspace = pwd()
       // Mark the code checkout 'stage'....
       stage 'Checkout'
       // Checkout code from repository
       checkout scm

       ...
     }
  }
}   
{% endhighlight %}

Secondly, you need to ensure the master runs as UTF-8. To do this I passed in an argument to the start script for Jenkins:

{% highlight bash %}
-Dfile.encoding=UTF-8
{% endhighlight %}


So, in my case on FreeBSD, the statements I have in `rc.conf` are:

{% highlight bash %}
jenkins_enable="YES"
jenkins_args="--webroot=/usr/local/jenkins/war --httpPort=8180"
jenkins_java_opts="-Djava.net.preferIPv6Addresses=true -Dfile.encoding=UTF-8" 
{% endhighlight %}

Now it looks all pretty again and we get all the colouring and symbols from the output of Fastlane:

![Screenshot of working ANSI and UTF-8 in Jenkins 2.0 pipeline build jobs](/public/screenshot_utf8_ansi_working.png)


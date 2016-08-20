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

It appears that a 'global' build number is not something Jenkins supports, or does any of the plugins I found. I did find some that looked like they might help, but ultimately didn't support Jenkins 2.0's pipeline DSL.

So, instead I wrote a very simple small HTTP server in Python that serves up an incremental integer every time you connect to it. The integer is stored in a file so can carry on after a restart. It is a simple single-threaded server based on the built-in Python `BaseHTTPServer` so that sorts out any concurrency issues. 

```python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket

class NumberServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        
        # Try and open number file and read number
        try:
            f = open("number.txt", "r")
            number = int(f.read())
            f.close()
        except IOError, ValueError:
            # if we fail then just assume 1
            number = 1

        # send the number to the client
        self.wfile.write(str(number))
        
        # write incremented number back to file
        f = open("number.txt", "w")
        number = str(number+1)
        f.write(number)
        f.close()

    def do_HEAD(self):
        self._set_headers()

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6        
        
def run(server_class=HTTPServerV6, handler_class=NumberServer, port=80):
    server_address = ('::', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting number server...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

```

[The latest version of the code is available on Github](https://github.com/hammertoe/numberserver). 

```bash
Matts-iMac:~ matt$ curl http://jenkins:9999/
28Matts-iMac:~ matt$ curl http://jenkins:9999/
29Matts-iMac:~ matt$ curl http://jenkins:9999/
30Matts-iMac:~ matt$ 
```

Testing it you can see it returns a new number each time: `28`, `29`, `30`. There is no newline returned as the output is intended to be consumed directly by a script.

The `Jenkinsfile` has been modified to make a call to the URL and use the result in a variable for later use. Groovy makes this surprisingly easy and concise to do:

```groovy
env.BUILD_ID = 'http://numberserver.quernus.co.uk:9999/'.toURL().text
```

From the `Jenkinsfile` we can also set the build number displayed in Jenkins so that it matches the one we use:

```groovy
currentBuild.displayName = "#" + env.BUILD_ID
```

You can see then the global build numbers for a particular job as they show up non sequential as other jobs have run in-between these ones:

![Jenkins 2.0 global build numbers](/public/jenkins_global_build_numbers.png)

This puts the build number in an environment variable. This is then looked at later by both the Gradle build script for our Android builds: 

```groovy
int getVersionCodeFromEnv(String versionName) {
    System.getenv("BUILD_ID”) as Integer ?: 0
}
```

…and the Fastlane config for our iOS builds:

```ruby
      increment_build_number(
        xcodeproj: project,
        build_number: ENV['BUILD_ID']
      )
```

And the end result is that the feature branch app on Fabric has a combination of jobs built from different branches, but that the build number is both unique and increasing for each build:

![Fabric Beta feature branch builds with unique build numbers across branches](/public/fabric_beta_unique_build_numbers.jpg)

I can tap to install any previous build of this app from any of the feature branches for testing.

Oh, and I suppose I can now cross ‘microservices’ off my buzzword bingo sheet now, right? ;)


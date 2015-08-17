---
layout: post
title: iOS Deployment and Provisioning - Part III - Tools in Detail - Fastlane
comments: True
tags: iOS, iPhone, apple
published: false
---

<p class="message">
  This is the fourth in a series of blog posts about iOS deployment and experiences setting up a continuous testing and build server for iOS apps. These posts are of interest to individual developers wanting to understand more, but mainly targeting small development teams trying to manage their development, testing and deployment process.
</p>

## Fastlane

Fastlane is a collection of about a dozen different tools for communicating with iTunes Connect, the Apple Developer Portal and 3d party services in a scriptable manner.

It has a notion of ‘lanes’ these are separate pipelines of tasks that can be run in sequence. In our configuration we have just three lanes, `test`, `alpha` and `release`. It may seem odd to jump all the way from an alpha to release, with no apparent beta, but in fact there is no real distinction between a beta, a release candidate and a production release. When a `release` build is uploaded to TestFlight it is make as ‘beta’ meaning it is available for testing via TestFlight. But any one of those builds could be submitted to Apple for review for the App Store.

The test lane just builds the app for testing and runs the unit tests over the app. Both the alpha and release lanes also run the full test suite before building the app for being uploaded. We could keep the test and build lanes separate, but as we’d want to run the tests before any build, I thought I might as well include them in the lane.

So we have two convenience methods, `do_build` and `run_tests` that are called by the respective lanes:

```
  def run_tests

    for scheme in [‘Nutrition’, ‘NutritionAppTest’]

      xctest(
        scheme: scheme,
        workspace: ‘Nutrition/Nutrition.xcworkspace’,
        destination: ‘platform=iOS Simulator,name=iPhone 6’,
        reports: [
          {
            report: “junit”,
            output: “build/reports/#{scheme}-tests.xml”
          }
        ],
        clean: nil,
        derivedDataPath: ‘./build’,
      )
    end

  end
``` 

We have multiple test suits that we want to run in isolation of each other, hence we loop over the two test suites: `Nutrition` and `NutritionAppTest`. It calls `xctest` which fires up an iOS simulator on the Mac Mini and runs the tests on it. If you VNC into the Mac Mini you can see the simulator start up and the tests run. We output the tests in `junit` format for Jenkins to be able to parse later. I’ve set `clean: nil` as Jenkins is set to wipe the workspace between each build anyway, so no need to clean. The `derivedDataPath` argument means all the build artefacts end up in the workspace, rather than put in a shared space in the user’s home directory by default. This means they too are cleared when the workspace is wiped, and multiple Jenkins jobs don’t taint each other with build artefacts.

```
  def do_build(scheme, configuration)
      increment_build_number(
        build_number: ENV[‘BUILD_ID’]
      )

      profile = ‘build/nutrition.mobileprovision’

      if configuration == ‘Release’     
        app_identifier = ‘com.enquos.nutrition’
        display_name = ‘enquos nutrition’
        set_istest_false
        sigh(
          app_identifier: app_identifier,
          filename: profile,
        )
      else
        app_identifier = ‘com.enquos.Nutrition.alpha.’ + GIT_BRANCH_ID
        display_name = ‘enquos nutrition ‘ + GIT_BRANCH
        sigh(
          app_identifier: ‘*’,
          adhoc: ‘1’,
          filename: profile,
        )
      end

      update_info_plist(
        app_identifier: app_identifier,
        display_name: display_name,
        plist_path: ‘Nutrition/Info.plist’,
        xcodeproj: ‘Nutrition/Nutrition.xcodeproj’,
      )

      update_project_provisioning(
        xcodeproj: “Nutrition/Nutrition.xcodeproj”,
        build_configuration_filter: “.*Nutrition.*”,
        profile: profile,
      )

      ipa(
        scheme: scheme,
        configuration: configuration,
        embed: profile,
        xcargs: ‘-derivedDataPath ./build’,
      )

  end
```

The `do_build` function does a number of steps:

1. Work out the build number, in this case we take it from an environment variable supplied by Jenkins.
2. Set the app identifier and the display name depending on whether this is a release build or alpha. It is is an alpha build then we create the app id and display name based on the Git branch. This allows us to have multiple distinct apps on a device at one time, each from a different branch of the code.
3. Download the correct provisioning profile from the Apple Developer Portal (`sigh`). If this is a release, then use our main app store distribution profile. If it is an alpha, then use our wildcard adhoc profile. This profile contains the UDIDs of our developers and anyone we want to test the app. By downloading this each time, it means we always build with the latest list of devices.
4. Update the info.plist and provisioning files in the app to contain the information calculated above. This basically overrides any settings that might be already contained in the code from Xcode.
5. Finally, build the ipa file using the specified configuration and scheme. It should be possible to infer the configuration from the scheme, as that is where you set it in Xcode, but due to a bug in xcodebuild it picks the wrong configuration, so we specify it manually here.

Before we run any of the lanes, we set a few variables based on variables supplied by Git and we run the tests. We set the text to use for the testing notes shown by TestFlight / Hockey to be the git commit log. We explicitly choose which certificate ID to use as we have two registered in the Apple Developer Portal. And we munge the Git branch into something that looks like an id.

```
  before_all do

     ENV[‘DELIVER_WHAT_TO_TEST’] = git_commit_log
     ENV[‘SIGH_CERTIFICATE_ID’] = ‘XXXXXXXXXX’
     GIT_BRANCH = ENV[‘GIT_BRANCH’] || ‘unknown’

     GIT_BRANCH_ID = GIT_BRANCH.dup
     GIT_BRANCH_ID.gsub! ‘/‘, ‘.’
     GIT_BRANCH_ID.gsub! /[^A-Za-z0-9\-.]/, “-“

     run_tests
  end
```

Now we have the actual lanes themselves. The test lane is short and sweet. It doesn’t actually do anything as the tests themselves are run in the `before_all` block above:

```
  lane :test do
    # Tests run in before_all
  end
```

The alpha lane is the first lane that does any real work:

```
  lane :alpha do

    do_build(‘Nutrition’, ‘Beta’)
 
    hockey(
      api_token: ‘deadbeefdeadbeefdeadbeef’,
      notes: git_commit_log,
      notify: ‘0’, # Means do not notify
      status: ‘2’,
      release_type: ‘2’,
    )

    if ENV[“SLACK_URL”]
      slack(
        message: “New alpha build available for download”,
        success: true,
        payload: {
          ‘Build number’ => ENV[‘BUILD_ID’],
          ‘Git branch’ => ENV[‘GIT_BRANCH’],
          ‘Download URL’ => Actions.lane_context[ Actions::SharedValues::HOCKEY_DOWNLOAD_LINK ],
          ‘What\’s new’ => git_commit_log,
          },
        default_payloads: [],
     )
    end

  end
```

First we call the `do_build` routine with the schema `Nutrition` and the configuration `Beta`. Xcode projects start off by default with two configurations: `beta` and `release`. These control whether things like profiling and debugging symbols are left in or stripped. So we just use the default name of ‘Beta’ here.

Then we upload the build to Hockey. We pass in the release notes and tell Hockey what sort of build this is (2: alpha). Then, if we have a Slack URL environment variable defined, we post a message to Slack announcing the successful build and with a link to the download URL on Hockey.

The `release` lane is very similar:

```
  lane :release do

    do_build(‘Nutrition Release’, ‘Release’)
 
    hockey(
      api_token: ‘deadbeefdeadbeefdeadbeef’,
      notes: git_commit_log,
      notify: ‘0’, # Means do not notify
      status: ‘1’, # Means do not make available for download
      release_type: ‘1’,
      public_identifier: ‘deadbeefdeadbeefdeadbeef’,
    )

    deliver(
       beta: true,
    )

    if ENV[“SLACK_URL”]
      slack({
        message: “Nutrition Release build #{ENV[‘BUILD_ID’]} uploaded to Testflight”
      })
    end

 end
```

We do the build with the `Release` configuration. This strips out debug symbols and the likes. We upload it to Hockey, and set the release type to be a proper release (1) and we set the status so that it is not downloadable from Hockey. This is due to it being uploaded to TestFlight instead. As it will have been signed with an App Store provisioning profile, it can’t be uploaded to Hockey for download anyway.

The `deliver` command is the one that actually uploads to Testflight. 

We then send a message to Slack. There is no point putting a public URL here as TestFlight will automatically notify testers on their device and by email that a new build is available.

After all this is done, we reset the Git repo. This is not necessary for the Jenkins run builds, as the workspace is wiped anyway, but is nice for when running manually as it means you are back to a clean slate:

```
after_all do |lane|
      reset_git_repo(
        force: true,
        files: [
          “Nutrition/Nutrition.xcodeproj/project.pbxproj”
        ]
      )
end
```

In the next post I’ll go into detail about Jenkins and how we automatically run Fastlane when changes are committed.
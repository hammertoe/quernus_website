---
layout: post
title: Adding Photos to iOS Simulator
comments: True
tags: iOS, apple, fastlane, snapshot
summary: A simple way for scripting the adding of photos to the iOS simulator when using snapshot to take photos of your app
---

I'm currently using [Snapshot](https://github.com/KrauseFx/snapshot), part of Fastlane to automate the testing and screenshot capture of our app.

The problem I had, is that a part of our app involves capturing a photo from the camera or photo library for display in the app. And to do the screenshots justice I needed to use a specific image as opposed to the images shipped with the simulators. You can't use the camera on the simulator (obviously!).

You can simply just drag an image onto the simulator and it will put it into the Photos app on the device. But I needed to script the addition of the photos as the simulators are reset at the start of each run.

Well, I found a way to do it using the hooks provided in Snapshot to prepare the simulator before run, and `simctl`.

Just add the following callback to your `fastlane/Snapfile` file:

{% highlight ruby %}
setup_for_device_change do |device, udid, language|
    puts "Adding food photo to #{device}"
    system("xcrun simctl boot #{udid}")
    system("xcrun simctl addphoto #{udid} kale_salad_photo.jpg")
end
{% endhighlight %}

Obviously change the filename to the image you want to load. You could extend it to load all images from a directory if you wanted.


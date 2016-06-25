---
layout: post
title: NSScotland 2015 Conference
comments: True
tags: iOS, conference, community
summary: A write up of some of the talks I found interesting at the NSScotland conference in Edinburgh. Dealing with maps; Building a mental health app; Working with distributed teams; and a 30-year old calculator codebase
---

![Photo of talks at NSScotland](/public/nsscotland_talks.jpg)

This weekend I attended the [NSScotland conference](http://nsscotland.com/) in Edinburgh. A friendly small conference for iOS and Mac developers with a focus on chatting to people and the 'hallway tracks'. It was also a great chance to meet up in person with some of my colleagues in Edinburgh.

Below is a write up of some of the talks that caught my attention specifically.

## Top Ten Tips for Building Apps with Maps - Rachel Hyman, VOKAL Interactive

This is the sort of talk I love at a conference. You can see the battle scars of what has been tried and tested. What worked and what failed. Rachel talked about various tips and approaches for working with maps and mapping in iOS. 

[Her slides are up on Github](https://github.com/rachelhyman/nsscotland).

But some specific tips I found useful:

- Encapsulate obtaining permission and getting location in one method.
Don’t assume you always have permission, a use can at any time disable permissions for your app to use the location info. This is actually good advice for any permission stuff in iOS, e.g. accessing the camera or photo library. A user can switch that permission off at any time, so your app needs to be able to handle this gracefully in the future.

- MKMapCamera.heading != CLLocation.heading necessarily. There are two headings you might get. One is from the compass in the device. The other is based on the direction you are heading. They may be different. Think: sitting backwards in a moving taxi.

- Use gpx routes to simulate routes. You can record a GPX track with an app such as MapMyWalk and then import that GPX track into Xcode to use when testing an app in the iOS Simulator. Apple provide a few sample routes, but sometimes you want to get your own.

## PCalc Through the Ages - James Thomson

This talk was way more entertaining than any talk about a 30 year old code base on a scientific calculator app has any right to be.

James talked about the original app writen by himself whilst a student and wanting a scientific calculator. It was written in Pascal and then over time bits an pieces have been wrapped and re-writen in various languages. I can't do justice in a blog post to his presentation, so I hope the video will be out soon and I'll link that here.

## Building an ecosystem for mental wellbeing apps and why Heathkit is missing a trick - Kate Ho - Product Manager - Health and Social Care Integration, Scottish Government

This talk was originally titled "Touch Interfaces (and the Watch)", but actually ended up mainly being a history and status of the [Ginsberg Project](https://www.ginsberg.io/). Ginsberg is a project funded and run by the Scottish government to produce mood tracking app for mental health wellbeing. It is similar to enquos in terms of it's ability to integrate with a number of different other data sources, but focusses exclusively on mental health. Their motto is "Creating an emotional web". They had a look at what other 'mood tracker' apps there are on the app store, and in fact their are loads of them, but none of them took the holistic view that they wanted to take.

<iframe width="560" height="315" src="https://www.youtube.com/embed/VIsuXsseAdE" frameborder="0" allowfullscreen></iframe>

Ginsberg is a non-judgemental app and intended to enable users to spot patterns in their mood and wellbeing.

It total the app was built over 18 months. This was the first app to be developed inside the Scottish Government itself. The first prototype was developed in about 3 months, and released to a group of about 12 people to test. It was scrapped and rebuilt again in about 2 months with the help of a psychologist. They originally started developing native apps for iOS and Android, but switched to Cordova to iterate quicker, but might switch back to native in the future.

One of the main issues they had was that most existing mood tracking apps just asked you to rate your mood on a scale of 1-10. But mood is much more fine grained than that. Ginsberg is instead based on the [Warwick-Edinburgh Mental Well Being Scale (WEMWBS)](http://www.healthscotland.com/scotlands-health/population/Measuring-positive-mental-health.aspx). They present the user a number of questions from a selection of 18 total questions such as "Do you feel connected to other people today?". One of the main complaints Kate has was that Apple's Healthkit does not yet take mental heath very seriously. It only has a single category for 'mood' at the moment.

They have found that users fall into one of three categories:

- Externalisers - who want a place to write privately. A diary.
- Pattern spotters - the 'data geeks'. They want to upload as much data as possible and be able to stop patterns in the data
- Trouble shooters - They work on one thing at a time. They may use a tool to reach a goal and once reached, stop using it.

I had a chance to have a great chat with Kate after the talk. It seems that some of the issue they are having regarding standardised scales for assessment are similar to what we are seeing tracking fitness and health data. For instance, one app might record sleep time as time you went to bed until time you got out of bed. Others might record time asleep. In most cases the most interesting bit of information is how long the person was in bed, but *not* asleep. The project development is currently on hold whilst they seek further funding, but the app itself is still running.

## Managing Distributed Teams - Maria Gutierrez - Senior Director of Engineering, Living Social

This was another talk I was looking forward to, as I am currently managing a distributed team of developers. What was interesting was that Living Social, and enquos's current selection of tools is near identical. We both use Slack for daily comms and Google Hangouts for daily stand-ups.

Her top key qualities to being an effective manager of distributed teams:

- being visible
- being honest and open
- being responsive
- delivering
- being consistent

So I am going to strive to keep these all in mind and make sure that I am doing them as much as possible. I think I am hitting most of them, but there are some I could always do with some more work on. I want to start doing more 1-to-1 hangouts with individuals on a weekly basis.

Her tips for distributed teams working together effectively:

- group devs with compatible timezones
- agreement on "how we work"
- consistent working hours
- notify changes to plan
- shared calendars

The last of these three points all concern with scheduling and making sure people know how and when they can expect colleagues to be around. We have a shared calendar with holidays and the likes marked on, but Living Social have a much better system I think, with more granularity than just 'here' or 'away':

![Living Social's team calendar showing when people are available](/public/livingsocial_calendar.jpg)

Each day for each person on the team is colour coded with their availability. They code the availability as:

- Working, business as usual
- Working normally but remote
- Working irregular times. Will check online often
- PTO (personal time off). Not available, but will answer for an emergency
- PTO. No chance you'll find me
- Public holiday in my country

I really like this, as I personally work pretty flexibly. Most of the time I am in my office 9-5 in my timezone. But sometimes, for instance I might work from home looking after my daughter. It would be good to be able to distinguish this easily. Ie. I am around and working, but I might be distracted periodically. Or it is good to be able to distinguish between taking some time off to catch up on some personal errands around town, versus I'm camping on the top of the mountain and have no connectivity even if I wanted some.

## Kids at the conference

There was childcare available at the event, which is a great idea for parents and allowing people that might not be able to addend a conference. Alas, this wasn't publicised as well as it could have been, and I didn't find out about it until the day before. Our 4 year old might have been too young for it though. The kids were doing some kind or art project, and at one point I spotted them dressed up being filmed... so I'm waiting to see the results as they seemed to be having a great time!

![Kids doing an art project at the conference](/public/nsscotland_kids.jpg)

## Thanks

Thanks to Alan for putting the conference on again, and hope the event continues to run and get even better.

![Edinburgh at night](/public/edinburgh_night.jpg)

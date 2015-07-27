---
layout: page
title: Talks
---

Slides / Videos from various talks I've given at events.

{% for talk in site.talks %}
  * {{ talk.date | date_to_string }} &raquo; [ {{ talk.title }} ]({{ talk.url }})  
    _{{ talk.event }}_
{% endfor %}

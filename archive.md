---
layout: page
title: Archive
---

{% for post in site.posts %}
  <div class="date">{{ post.date | date_to_string }}</div><div class="title"><a href="{{ post.url }}">{{ post.title }}</a> &mdash; <span class="summary">{{ post.summary }}</span></div>
{% endfor %}



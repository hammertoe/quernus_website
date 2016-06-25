Title: Lipstick On a Pig (+Audio)
Date: 2009-07-01 06:38
Author: hammertoe@slideshare.net(hammertoe)
Slug: lipstick-on-a-pig-audio

<iframe src="//www.slideshare.net/slideshow/embed_code/key/qxjpHAfypyrT64" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/hammertoe/lipstick-on-a-pig" title="Lipstick On a Pig (+Audio)" target="_blank">Lipstick On a Pig (+Audio)</a> </strong> from <strong><a href="//www.slideshare.net/hammertoe" target="_blank">Matt Hamilton</a></strong> </div>

Dynamically skinning a legacy portal using Python, WSGI (the Python Web
Server Gateway Interface), and Deliverance.

So you have a big legacy portal application which you want to change the
look of, but are contractually not allowed to touch?

Here is a case study on how we used the power and flexibility of Python
and WSGI and the wonder lxml to dynamically re-skin a proprietary .NET
portal without even touching it.

We take a giant lump of messy invalid HTML markup and dynamically strip
it back, add semantic markup and CSS and present the user with a nice
svelte valid site.

I will cover the history of the legacy portal, the problems encountered,
our cunning plan to dynamically re-skin the site, a technical overview
of the parts of the system (lxml, WSGI, etc), and what we learned along
the way.


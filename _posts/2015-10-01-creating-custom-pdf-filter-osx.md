---
layout: post
title: Creating Custom PDF Filter on OS X
comments: True
tags: osx, pdf
summary: Sometimes you want to reduce the size of a PDF, say with images embedded. OS X has a built in filter for this, but it is a bit harsh. You can create you own custom ones though.
---

Each month I send an invoice to my clients. Included in that invoice are photos of any receipts for expenses incurred (taxis,etc.). I typically just take a photo of these recipes flat on my desk and then save them as PDFs and drag those PDFs into the main invoice PDF in Preview to create a single file with both the invoice and all the receipts.

This month, I went to send the invoice to the client and Gmail balked at me as the file size was too large. The PDF was 22MB, but I guess once Base64 encoded and S/Mime encrypted it was over the 40MB-ish limit it appears we have on Gmail.

I remember seeing a filter when saving a PDF from preview called 'Reduce File Size'. Sure enough, that reduced the file size down from 22MB to 250KB. But the images of receipts were so heavily compressed that you could not read some of the numbers on them.

Hunting around online I came across [this post from several years ago said you can create your own filters](http://hints.macworld.com/article.php?story=20120629091437274). I check on my Mac running Yosemite (10.10.5) and it still works!

The filters are found in `/System/Library/Filters` and so I copied the 'Reduce File Size' one and increased the quality and max image resolution as per the post above:

```
sudo cp Reduce\ File\ Size.qfilter Reduce\ File\ Size\ Best.qfilter
```

My filter contents:

{% highlight xml %}
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Domains</key>
	<dict>
		<key>Applications</key>
		<true/>
		<key>Printing</key>
		<true/>
	</dict>
	<key>FilterData</key>
	<dict>
		<key>ColorSettings</key>
		<dict>
			<key>DocumentColorSettings</key>
			<dict>
				<key>CustomLHSCorrection</key>
				<array>
					<integer>8</integer>
					<integer>8</integer>
					<integer>8</integer>
				</array>
			</dict>
			<key>ImageSettings</key>
			<dict>
				<key>Compression Quality</key>
				<real>0.75</real>
				<key>ImageCompression</key>
				<string>ImageJPEGCompress</string>
				<key>ImageScaleSettings</key>
				<dict>
					<key>ImageScaleFactor</key>
					<real>0.5</real>
					<key>ImageScaleInterpolate</key>
					<true/>
					<key>ImageSizeMax</key>
					<integer>3508</integer>
					<key>ImageSizeMin</key>
					<integer>128</integer>
				</dict>
			</dict>
		</dict>
	</dict>
	<key>FilterType</key>
	<integer>1</integer>
	<key>Name</key>
	<string>Reduce File Size Best</string>
</dict>
</plist>
{% endhighlight %}

You can then choose this new filter when you select 'export' from within Preview to export the large PDF to a smaller one:

 ![Screenshot of choose an output filter for PDFs](/public/screenshot_reduce_filesize_filter.png)

This resulted in the PDF dropping from 22.7MB to 1.4MB and the text in the images all still being legible. Result!


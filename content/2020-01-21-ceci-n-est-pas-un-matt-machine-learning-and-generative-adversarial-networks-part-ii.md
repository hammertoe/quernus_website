---
layout: post
title: Ceci n'est pas un Matt - Machine Learning and Generative Adversarial Networks - Part II
comments: True
tags: AI, machine learning, CNN, GAN, Python
summary: Playing with Generative Adversarial Networks (GANs) to create a new profile photo of myself.
---

<p class="message">
This post was originally written on my Coil site, which is currently my main blogging platform. 
On there you will also see bonus content if you are a Coil subscriber.<br />
<a href="https://coil.com/p/hammertoe/Ceci-n-est-pas-un-Matt-Machine-Learning-and-Generative-Adversarial-Networks-Part-II/0irA1Ppib">https://coil.com/p/hammertoe/Ceci-n-est-pas-un-Matt-Machine-Learning-and-Generative-Adversarial-Networks-Part-II/0irA1Ppib</a>
</p>


<p>
 So following on from
 <a href="https://coil.com/p/hammertoe/Ceci-n-est-pas-un-canard-Machine-Learning-and-Generative-Adversarial-Networks/JYC0urIr7" style="color:#0080FF;text-decoration:none">
  my last post about trying to generate cartoon ducks using AI
 </a>
 -- and accidentally producing something quite Warhol-ish, I decided to try and generate a new profile pic for myself on our intranet at work. A colleague of mine said that my current pic makes me look
 <a href="https://en.wikipedia.org/wiki/Mr._Noodle" style="color:#0080FF;text-decoration:none">
  Mr Noodle from sesame street
 </a>
 . No. You can't see the pic. But maybe my beard was a bit too unruly at the time, and maybe the wall behind me was a bit too bright and primary-colourish.
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/Jha7xztbT5yRfpxmqAJf7w.png"/>
<p>
 <a href="https://coil.com/p/hammertoe/Blog-Machine-Learning-and-Artificial-Intelligence/1xVFVh1yj" style="color:#0080FF;text-decoration:none">
  <em>
   This is a post in my series on machine learning and artificial intelligence. You can find more posts on this topic at the main index.
  </em>
 </a>
</p>
<p>
 <a href="https://coil.com/p/hammertoe/Blog-Machine-Learning-and-Artificial-Intelligence/1xVFVh1yj" style="color:#0080FF;text-decoration:none">
  <em>
  </em>
 </a>
</p>
<p>
 So could I use the same technique of Generative Adversarial Networks (GANs) to produce a new image of "me"?
</p>
<p>
</p>
<p>
 Let's recap how these networks work with a little analogy:
</p>
<p>
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "So Sir, can you describe to us the person who robbed you of your wallet?"
 </strong>
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "Yes officer, he was male, early forties, caucasian, 5'9", short brown hair, glasses, a beard and moustache"
 </strong>
</p>
<p>
 [sketch artist works furiously]
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "Like this?"
 </strong>
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "No, the glasses were thinner, wire-framed type"
 </strong>
</p>
<p>
 [sketch artist draws a new drawing with different glasses]
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "Like this?"
 </strong>
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  "Yeah... maybe smaller nose"
 </strong>
</p>
<p>
 [sketch artist draw a new drawing with smaller nose]
</p>
<p>
</p>
<p>
 We have two neural networks, one, the
 <em>
  generator
 </em>
 (the sketch artist) and a second one, the
 <em>
  discriminator
 </em>
 (me). The first one is creating new images and the second one is trying to critique them. If the critic can't tell the difference between a 'fake' and a 'real' image, then the generator (sketch artist) has learned how to produce good likenesses of the subject.
</p>
<p>
</p>
<p>
 So first, I needed a whole load of real images for the generator to feed to the discriminator in amongst its 'fake' ones to see if it could tell the difference.
</p>
<p>
</p>
<p>
 Luckily Apple iPhones already have some machine learning in them to identify and categorise people. So I can easily copy 300 pictures from the last 5 years of myself from the phone to my desktop computer for processing.
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/_2WkFc-hT-C2ZaBMq3eKLw.png"/>
<p>
 I then opened them all up in Preview and very quickly and roughly cropped them to just have my face in. I discarded those that I was wearing sunglasses, or at a very odd angle to the camera.
</p>
<p>
</p>
<p>
 I then fed those images into the GAN from before. And out of the gaussian noise, started to emerge a somewhat recognisable me...
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/Il_QToA_TXWJ6aWNk9PoTg.jpg"/>
<p>
 Further...
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/EKBc0MKhRcyzW1B7SEqOlg.jpg"/>
<p>
</p>
<p>
 So there, are definitely some likenesses there, but still in most of them I look like some apparition from a horror film.
</p>
<p>
</p>
<p>
 I realised, that the images all being slightly different crops and orientations was giving the GAN a hard time. Bearing in mind this is a fairly simple network and we are far from the state of the art.
</p>
<p>
</p>
<p>
 So I realised that I could use another bit of machine learning to pre-process the images. I could use a computer vision library to detect my facial features and then rotate, shift and scale the image such that at least my eyes were in the same place in each photo.
</p>
<p>
</p>
<p>
 If you want to know the full technical details and code on this, I've written a separate (subscribers only) post on
 <a href="https://coil.com/p/hammertoe/Using-OpenCV2-to-Align-Images-for-DCGAN/HxJ6NOM2O" style="color:#0080FF;text-decoration:none">
  Using OpenCV2 to Align Images for DCGAN
 </a>
 .
</p>
<p>
</p>
<p>
 But the end result was pretty cool... and quite spooky. So here is an animated gif showing a few of the input images:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/3q6SwbrQSJax77tLVSZwqw.gif"/>
<p>
 Notice how my face is slightly different size, and eyes moving about in different locations? Compare that to the aligned images:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/bQDK_WUbTmWGom5FGC6kWA.gif"/>
<p>
 Pretty eerie, right? Those are the same images as above, but the pre-processing AI has calculated the location of my eyes, and transformed the image such that my eyes are in the same location in each image.
</p>
<p>
</p>
<p>
 So lets feed that back into the GAN and see how we do...
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/h2eOOjCST5O8R2yXaQsWwA.jpg"/>
<p>
 Not bad! There are certainly some ones there were it looks like I've been hit in the face with a shovel a few times... but actually overall it has done pretty well.
</p>
<p>
</p>
<p>
 Again, what is pretty amazing is that
 <strong class="EditorRules__BoldText-sc-1bp7rl0-5 gJKqDR">
  none of these images ever existed
 </strong>
 . They are not distorted photos, but they are the result of a machine learning algorithm learning what my facial features look like and creating an entirely new and unique image of me.
</p>
<p>
</p>
<p>
 So to recap, in the end there were three entirely separate machine learning / AI algorithms used in this process:
</p>
<ol>
 <li>
  <span>
   The machine learning on my iPhone that had analysed all my photos and clustered the ones of the same same people together, such that I could easily find photos of me
  </span>
 </li>
 <li>
  <span>
   The OpenCV script used to pre-process the images that located my facial features in the photos and the rotated, scaled, and shifted the image such that my eyes were in the same place on each image
  </span>
 </li>
 <li>
  <span>
   The Generative Adversarial Network (GAN) that was used to generated entirely new images from the existing ones.
  </span>
 </li>
</ol>
<p>
</p>
<p>
 For coil subscribers, there is another animation showing the learning as it progressed.
</p>
<p>
</p>
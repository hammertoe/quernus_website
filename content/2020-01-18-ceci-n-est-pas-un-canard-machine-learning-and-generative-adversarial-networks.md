---
layout: post
title: Ceci n'est pas un canard - Machine Learning and Generative Adversarial Networks
comments: True
tags: AI, machine learning, CNN, GAN, Python
summary: An attempt to generate cartoon ducks via Generative Adversarial Networks (GANs)
---

<p class="message">
This post was originally written on my Coil site, which is currently my main blogging platform. 
On there you will also see bonus content if you are a Coil subscriber.<br />
<a href="https://coil.com/p/hammertoe/Ceci-n-est-pas-un-canard-Machine-Learning-and-Generative-Adversarial-Networks/JYC0urIr7">https://coil.com/p/hammertoe/Ceci-n-est-pas-un-canard-Machine-Learning-and-Generative-Adversarial-Networks/JYC0urIr7</a>
</p>


<p>
 So, firstly, thanks to
 <a href="https://twitter.com/alloynetworks" style="color:#0080FF;text-decoration:none">
  Alloy
 </a>
 for the
 <a href="https://en.wikipedia.org/wiki/The_Treachery_of_Images" style="color:#0080FF;text-decoration:none">
  Magritte reference
 </a>
 for the title of this post.
</p>
<p>
 <a href="https://coil.com/p/hammertoe/Blog-Machine-Learning-and-Artificial-Intelligence/1xVFVh1yj" style="color:#0080FF;text-decoration:none">
  <em>
  </em>
 </a>
</p>
<p>
 <a href="https://coil.com/p/hammertoe/Blog-Machine-Learning-and-Artificial-Intelligence/1xVFVh1yj" style="color:#0080FF;text-decoration:none">
  <em>
   This is a post in my series on machine learning and artificial intelligence. You can find more posts on this topic at the main index.
  </em>
 </a>
</p>
<p>
</p>
<p>
 Yesterday, a friend on Twitter, Munch, put out an art challenge:
</p>
<div class="coil-embedly-iframe EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX" data-embed-height="456" style="padding-bottom:456px">
 <iframe class="embedly-embed" height="456" src="//cdn.embedly.com/widgets/media.html?type=text%2Fhtml&amp;key=fbeb5062dd1941c49b690a10c2ce6fa7&amp;schema=twitter&amp;url=https%3A//twitter.com/muncheds/status/1217964089894264832&amp;image=https%3A//pbs.twimg.com/media/EOcT4nBVAAQ0Dyh.jpg%3Alarge" width="500">
 </iframe>
</div>
<p>
 Well, I'm rubbish at art. But for a bit of fun, decided that rather than showcase
 <em>
  my
 </em>
 rubbish art, could I instead showcase a
 <em>
  computer's
 </em>
 attempt at art? What could go wrong? Can I teach a computer to draw a duck and fill in the blank template above?
</p>
<p>
</p>
<p>
 So, introducing to you the concept of
 <em>
  Generative Adversarial Networks
 </em>
 ... or GANs for short. Gen...what? These are a type of machine learning neural network that attempt to generate new data (generative) from learning from a series of samples, by trying to out-wit a second neural network (a
 <em>
  dversarial).
 </em>
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/YXdacvpVTDe93F7rmtzqxA.jpg"/>
<p>
 So how does it work? Let's imagine you and I play a game. Your job is to show me a series of James Bond films some of which are real, and some of which are ones that you have produced yourself. My job is to try and guess which of the films is real, and which is fake. Got it so far?
</p>
<p>
</p>
<p>
 So firstly, you watch all 26 James Bond films and try to distil down the
 <em>
  essence
 </em>
 of a James Bond film. What features make it a James Bond film if you had to describe it to someone?
</p>
<ul>
 <li>
  <span>
   Athletic male lead, who is a British secret service agent
  </span>
 </li>
 <li>
  <span>
   Lots of gadgets like X-ray glasses, and camera tape recorders
  </span>
 </li>
 <li>
  <span>
   Car chases... cars with guns in them etc
  </span>
 </li>
 <li>
  <span>
   Esoteric villains
  </span>
 </li>
 <li>
  <span>
   A sexy adversary
  </span>
 </li>
 <li>
  <span>
   Great music
  </span>
 </li>
 <li>
  <span>
   etc
  </span>
 </li>
</ul>
<p>
 Using that list of 'features' of a Bond film, you now produce your own Bond film... you might be good at it you might be bad at it. To start with you are going to be pretty lousy at it on your first attempt.
</p>
<p>
</p>
<p>
 My job is to look at the film you produce and decide if it is a real Bond film or fake. If it is very easy for me to guess a real one from a fake and I get them all right, then that means you are doing a poor job at making fakes.
</p>
<p>
</p>
<p>
 The goal here, is for you to keep trying to make fakes to fool me. And my job is to keep feeding back to you how well I can tell the real from the fake. If I can't tell the difference from a real Bond film and a fake one, then you have done a very good job in producing a new, unseen, fake Bond film.
</p>
<p>
</p>
<p>
 In terms of a machine learning architecture, it looks like this:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/79FPwi7kQ_i0kI2fw5ao8g.png"/>
<p>
 <em>
  source:
 </em>
 <em>
  <a href="https://www.slideshare.net/xavigiro/deep-learning-for-computer-vision-generative-models-and-adversarial-training-upc-2016" style="color:#0080FF;text-decoration:none">
   https://www.slideshare.net/xavigiro/deep-learning-for-computer-vision-generative-models-and-adversarial-training-upc-2016
  </a>
 </em>
</p>
<p>
</p>
<p>
 You have one branch at the top (yellow) feeding in real Bond films, and you have a
 <em>
  generator
 </em>
 at the bottom (blue) creating fakes ones (your job). And you have me, the
 <em>
  discriminator
 </em>
 (red), trying to tell if they are real or fake. My error rate in judging them,
 <em>
  loss
 </em>
 , is fed back to the start for the next iteration. Based on that loss, you can determine which features were important or not. ie. if you put a dragon in your Bond film and I feed back that clearly this is not a Bond film you can infer that dragons are not a legitimate element of a Bond film.
</p>
<p>
</p>
<p>
 <strong class="coil-small-title EditorRules__SmallTitle-sc-1bp7rl0-3 lohAQC">
  Show me the ducks!
 </strong>
</p>
<p>
</p>
<p>
 So, I needed:
</p>
<ul>
 <li>
  <span>
   a working GAN algorithm
  </span>
 </li>
 <li>
  <span>
   some ducks
  </span>
 </li>
</ul>
<p>
 For the algorithm,
 <a href="https://github.com/gsurma/image_generator" style="color:#0080FF;text-decoration:none">
  I found one on Github
 </a>
 (a code sharing/collaboration site) that I could use for this task. This one had been used originally to try and generate new Simpson's characters, so might be good, as already tuned to cartoons:
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/_9_dj64uRTapWR9vF8eC-w.png"/>
<p>
 I loaded the code into
 <a href="https://colab.research.google.com/" style="color:#0080FF;text-decoration:none">
  Google Colab
 </a>
 , which is another collaborative tool that allows you to run python code on a cluster of computer run by Google. This is helpful as GANs take quite a lot of computing power, and means I could run it faster than I could on my computer at home.
</p>
<p>
</p>
<p>
 I also needed a bunch of 'real' images of duck drawings for it to use. I search Google for "draw a duck share your art" which is the meme this was from, and downloaded a whole bunch of them:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/gbaJABXnRrO03GXm2ULCVQ.jpg"/>
<p>
</p>
<p>
 I uploaded them to where my code could load them and then set the algorithm to run. My first attempt was for 300 'epochs', that is there were 300 iterations of trying to generate duck images and trying to fool the disciminator.
</p>
<p>
</p>
<p>
 The first attempts you can't see anything duck-like at all, as the generator has started with random data and still not worked out what 'features' the output images should have. Here is 5 samples of 'ducks' from epoch 24:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/RDtvN3X-SLyMr-dYpEyw-Q.png"/>
<p>
 Not very exciting, huh? Just grey blobs...
</p>
<p>
 As it progresses, it starts to try various colours... and we end up with a nice tweed sort-of colour coming up. Great for cushions perhaps, but still not a duck. Epoch 100:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/8Ssgo6ILQRaHYGN33UNMzA.png"/>
<p>
 By the time we get to epoch 250, we are now getting some slight duck-like features show in the images. You can spot the yellow feet and beak emerging:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/6EOOXGKkTXCvTCtopOoxOA.png"/>
<p>
 But by the time we get to epoch 300, it's all gone wrong again:
</p>
<p>
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/9G36nLGeQX-6ohuNRgn7qA.png"/>
<p>
 What happened?! Well it turns out it looks like the algorithm kinda overshot the mark. There is actually a graph produced of the learning losses of both the generator and the discriminator:
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/6061hQKZRjeXDFZR8aWmVw.png"/>
<p>
 You can see that they were converging until around epoch 250, then the generator kinda went a bit nuts.
</p>
<p>
</p>
<p>
 So, I decided to run it again, reducing the 'learning rate' of the algorithm. This means it will learn a bit slower, but hopefully won't overshoot as much. I left it running overnight for 600 epochs to see how it got on. The graph of the learning looks a lot more positive this time. As you can see by the time it got to the end it was still pretty stable. It looks like it still has a bit of a 'wobble' around 300, but then seems to stabilise again.
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/LDA5RbubRCmxENZUErUHHg.png"/>
<p>
 So... the moment of truth... let's see what our ducks looked like!
</p>
<p>
</p>
<p>
 Here is a sample of them, from near the end at iteration 589:
</p>
<img class="EditorRules__Image-sc-1bp7rl0-0 hjLKDC" src="/coil_images/zhnVUwkVTUiUiriu6IZTLg.png"/>
<p>
 Whilst I don't think I will be winning any awards with these ducks, I think it has certainly managed to get along the right tracks!
</p>
<p>
</p>
<p>
 I think due to the high variance of input duck images, it had a hard time trying to work out what a duck should look like. With more samples, and perhaps more iterations it might do better. There are also a number of parameters to the algorithm that can be tuned to try and get better results. But for a quick un-tuned attempt, I'm pretty impressed.
</p>
<p>
</p>
<p>
 And for Coil subscribers below you can see a really cool animation of the 'evolution' of the algorithm learning what a duck is :)
</p>
<p>
</p>
<p>
 Part II of this adventure continues with:
 <a href="https://coil.com/p/hammertoe/Ceci-n-est-pas-un-Matt-Machine-Learning-and-Generative-Adversarial-Networks-Part-II/0irA1Ppib" style="color:#0080FF;text-decoration:none">
  Ceci n'est pas un Matt - Machine Learning and Generative Adversarial Networks - Part II
 </a>
</p>
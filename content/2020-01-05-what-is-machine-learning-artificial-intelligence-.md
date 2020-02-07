---
layout: post
title: What is Machine Learning / Artificial Intelligence?
comments: True
tags: machine learning, AI
summary:  So, I'm about to start a series of posts on machine learning and artificial intelligence. This set of posts will be somewhat technical but, the idea will be to introduce people to the concepts of machine learning and artificial intelligence and to de-mystify it a bit.

---

<p class="message">
This post was originally written on my Coil site, which is currently my main blogging platform. 
On there you will also see bonus content if you are a Coil subscriber.<br />
<a href="https://coil.com/p/hammertoe/What-is-Machine-Learning-Artificial-Intelligence-/SxshuUm0U">https://coil.com/p/hammertoe/What-is-Machine-Learning-Artificial-Intelligence-/SxshuUm0U</a>
</p>


<p>
 So, I'm about to start a series of posts on machine learning and artificial intelligence. This set of posts will be somewhat technical but, the idea will be to introduce people to the concepts of machine learning and artificial intelligence and to de-mystify it a bit.
</p>
<p>
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
 So hopefully the first few articles at least should be followable by people without any specific technical or programming experience. As the series progresses I will start to bring in python code showing some examples of using machine learning for various tasks.
</p>
<p>
</p>
<p>
 So the first thing to cover... what even is it? We hear so much about artificial intelligence and everything from Terminator to Teslas come to mind. Some may even remember the 1980s film
 <a href="https://en.wikipedia.org/wiki/WarGames" style="color:#0080FF;text-decoration:none">
  Wargames
 </a>
 in which a young hacker (Matthew Broderick) accidentally breaks into a US defence computer controlling nuclear missiles. The film culminates with Broderick playing a game of tic-tac-toe with the computer and it learning that the best way to win is not to play at all. And hence nuclear armageddon is averted. This is a great simple example of machine learning, and an example I'll come back to.
</p>
<p>
</p>
<p>
 Generally, in 'classical' computer programming, a programmer writes a series of instructions for the computer to follow. Those instructions are explicit in what to do and contain logical flow: e.g. "If the temperature is above 20 degrees then turn the heater off". This code is pretty simple to look at and reason with. But it requires the programmer to know what the logical statements are. In essence, all computer programs take some kind of
 <em>
  input
 </em>
 and produce some kind of
 <em>
  output
 </em>
 . In this case the temperature is the
 <em>
  input
 </em>
 , and the state of the switch that turns the heater on and off is the
 <em>
  output
 </em>
 .
</p>
<p>
</p>
<p>
 In this case, it is pretty easy. The code would look something like this. It is a function that takes an input
 <em>
  temperature
 </em>
 and returns either 1 or 0 to represent the state the heater switch should be.
</p>
<div class="coil-embedly-iframe EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX" data-embed-height="640" data-embed-url="https://gist.github.com/hammertoe/7524e935cfa05cb652ff67cd58be0dd0" style="padding-bottom:320px">
 <iframe data-cy="coil-embedly-iframe" height="640" scriptstring="&lt;script src='https://gist.github.com/hammertoe/7524e935cfa05cb652ff67cd58be0dd0.js' type=&quot;text/javascript&quot;&gt;&lt;/script&gt;" scrolling="no" src="about:blank" style="width:1px;min-width:100%" title="&lt;script src='https://gist.github.com/hammertoe/7524e935cfa05cb652ff67cd58be0dd0.js' type=&quot;text/javascript&quot;&gt;&lt;/script&gt;">
 </iframe>
</div>
<p>
</p>
<p>
 But what if instead we wanted to instead code something a bit more generic e.g. "If the temperature is
 <em>
  too hot
 </em>
 then turn the heater off". How do we define "too hot"? A computer is a pretty 'unfeeling' object. How does it know that "too hot" even means? Well, with machine learning we can try and teach it what that means.
</p>
<p>
</p>
<p>
 This could be achieved by a branch of machine learning called "supervised learning" in which we give a program a set of known
 <em>
  inputs
 </em>
 and
 <em>
  outputs
 </em>
 called the
 <em>
  training data
 </em>
 and get it to learn the "bit in the middle". Here is what the training data could look like.
</p>
<div class="coil-embedly-iframe EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX EditorRules__EmbedDiv-sc-1bp7rl0-2 elPbsX" data-embed-height="640" data-embed-url="https://gist.github.com/hammertoe/20366fa70acc034e7324a5eb2342b8c8" style="padding-bottom:320px">
 <iframe data-cy="coil-embedly-iframe" height="640" scriptstring="&lt;script src='https://gist.github.com/hammertoe/20366fa70acc034e7324a5eb2342b8c8.js' type=&quot;text/javascript&quot;&gt;&lt;/script&gt;" scrolling="no" src="about:blank" style="width:1px;min-width:100%" title="&lt;script src='https://gist.github.com/hammertoe/20366fa70acc034e7324a5eb2342b8c8.js' type=&quot;text/javascript&quot;&gt;&lt;/script&gt;">
 </iframe>
</div>
<p>
 Can you spot the pattern here? Yes, it is what we described before, that if the input temperature is 20 or below, then output a 1, otherwise output a 0.
</p>
<p>
</p>
<p>
 With a machine learning algorithm we could train it to learn the pattern so that we don't have to explicitly code the rule. This might seem strange with such a trivial example, but where machine learning excels is when we have much more complex input data and patterns we might not be able to spot as humans. What if our input data wasn't just temperature, but was temperature, humidity, number of people in the house, time of day, output temperature? And the output was what we
 <em>
  feel
 </em>
 whether the heater should be on or off? That would be very hard to try and write rules for explicitly. But if we had a whole lot of training data taken from actual human experience then the program could learn what the rules are. The goal is for it to learn a generic set of rules that it can then apply to input data it has not been trained on and come out with the right answer.
</p>
<p>
</p>
<p>
 Hopefully this 'sets the scene' for what it is I will be writing about in these posts and give people a starting point.
</p>
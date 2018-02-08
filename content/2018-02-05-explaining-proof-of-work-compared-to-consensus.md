---
layout: post
title: Explaining Proof-of-Work, and how it compares to consensus
comments: True
tags: blockchain, pow, ripple, bitcoin, consensus
summary: I was asked to explain how Proof of Work on a blockchain worked, here is a transcript. And how it compares to Ripple's consensus algorithm.
---

Whilst in the [Ripple (XRP) discord chat group](https://discordapp.com/channels/367033345403518984/398919239093846017) the other day, I got explaining to a user there, Fisher_47, how the basics of cryptography work, and how Proof of Work is built on that, and how it compares to Ripple's consensus algorithm. I think the conversation started along the lines of asking 'What happens when quantum computing takes off'. The explanation was deemed useful, so I thought I'd put it here in case it helps anyone else. 

It is not intended to be a comprehensive coverage of all the details, it was just a quick overview of the concepts, but here it is:

All cryptography relies on a mathematical problem that is very difficult to solve, but very easy to prove right. And relies on the fact that we don't have enough computing power to brute force that problem in any realistic timeframe to be usable.

As soon as those assumption are broken, then everything else falls and the guys holed up in their caves, with their stash of tins of baked beans, and their AK47s.... COULD BE [expletive] RIGHT.

Let's try an example of this kind of problem. You can just type 7 * 13 into a calculator, or do it on your head or on paper... very easy. But what if I, instead, asked you "What two whole numbers multiplied together produce exactly 91?" That is very hard for you to work out. You'd probably sit down and try plugging various numbers into a calculator until you got a pair that worked.

Hashing and things like Bitcoin work similarly...

Say, I have a simple hash algorithm... say a substitution of each letter, a=1, b=2, c=3 etc.... and I add them all up So 'dog' = 4+15+7 = 26. The hash of 'dog' = 26. It is very easy for you to verify that, as you can just do the same calculation yourself easily.

But if I posed the question 'What other words result in a hash of 26'.... that is much harder You’d try cat... nope.... pig... nope... etc.

When a block is to be added to the blockchain in Bitcoin... the job of the miners is to try and compute 'What number can I add to this other number, such that the resultant hash value starts with 8 zeros'.

That is a 'hard' problem, and can only be done by brute force... i.e. trying every value. So all the miners race to see who can solve it first... that is why you see mining rigs rated at TH/s terahashes per second... how many trillion hashes they can compute and try per second. The winner is then rewarded with a gift of a certain number of bitcoin (12.5 I think it is now)
It is not that they add security, it is just that they have done something 'non-trivially hard' such that it could not be easily replicated. Every so often the difficulty level is raised and another zero is added to the problem.

Just in the same way you trust a £10 bank note because you know that making a forgery of such an item is 'hard' If anyone could draw a picture of the queen on a piece of paper and call it a £10 note then you wouldn't trust it. You trust that it takes a certain level of skill, machinery and materials to manufacture a legitimate looking banknote.

This approach uses a lot of computing power... hence why bitcoin uses so much electrical power. It is why the big bitcoin mining companies are based near cheap power sources in China (cheap coal) or Iceland (cheap geothermal).

Ripple's approach is much simpler. You just trust that if a certain number of independent people tell you that that piece of paper with Liz on it is a valid £10 note then you believe it is one.

So with Bitcoin the trust is implicit in that the task is 'hard' and so if completed must be valid. With Ripple the trust is explicit in that you have decided to trust a number of 3rd parties to attest that that is indeed a valid banknote.

Now, here is the nice bit.... you don't actually have to trust each individual 3rd party. You just need to trust that enough of them will say the right thing, such that you can ignore the liars. If Microsoft, Apple, and the Linux Foundation each ran a validator.... you don't need to actually trust each of them.... i.e. you might not trust Microsoft... but you can trust that Apple, Microsoft and the Linux Foundation are unlikely to collude together to come up with a lie that that all agree on.

If you are a detective investigating a crime... and have 100 witnesses to the crime... you don't need to actually trust each witness individually... you just need to trust that if you asked each witness what happened that more than 80% of them would agree on the truth. And not only that, but if they didn't come to an agreement, say 50 said one thing happened, and 50 said something different happened... you know that there is an issue.

So as long as you can be confident that there is no way 80 of they would collude to come up with the same false story, then you are OK. And if you pick a wide enough set of witnesses then you are OK. This is the high-level basis of Ripple's consensus protocol on the XRP Ledger.

The 3rd parties are any of the Validator nodes running on the XRP Ledger... some by Ripple Inc., some by other independent 3rd parties. Again, you don't have to trust them individually, you just need to trust that 80% of the validators you chose would not collude to defraud you.

I really should write this up as a blog post.... as quite a good way to explain it...
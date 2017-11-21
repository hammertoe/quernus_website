---
layout: post
title: Intro to Ripple and XRP
comments: True
tags: ripple, xrp, cryptocurrency, swift, bitcoin
summary: I've recently started playing about with the cryptocurrency XRP and the Ripple network, here is a quick introduction to it.
---

![Ripple logo](/public/Ripple-Logo.png)

Heard of Bitcoin? Yes? Heard of Ethereum? Maybe? Heard of Ripple? No? Well, let's try and fix that then. Here is a quick intro to Ripple.

## What is Ripple?

Ripple is a "real time payment settlement network". what does that mean? It is a network on which payment (or value in general) can be transferred between people or entities. It is run by a company, Ripple, Inc., but the software used to run the network is Open Source and anyone can set up a node on the network if they desire. In it's simplest terms, Ripple is just a distributed ledger of transactions. It is a way to record in a provable, immutable way, that a certain transaction happened.

The main problem that Ripple is trying to solve is that of cross-border payment. You may be familiar with SWIFT for international transfers, or SEPA within the Eurozone. If you make a SWIFT payment today it will likely cost you something like £10-15 and take four days for the payment to reach its destination. Ripple can do the same thing at a cost of fractions of a cent and a time of four seconds.

## What is XRP?

XRP is the native currency of Ripple. Confusingly XRP is sometimes also referred to as 'Ripple' as well, as in 'I paid him 100 Ripples'. Ripple the network can work with pretty much any currency you want it to, or even other kinds of value assets. If you are familiar with internet email systems, then you can think of the relationship being a bit like the Ripple network as the SMTP network (and rippled being analogous to Sendmail/Exim/Postfix) and XRP as analogous to RFC-822, the format specification of emails. 

So how does it compare to Bitcoin? With Bitcoin, the general approach is a completely anarchistic system. There is no one entity in control. As there is no trusted party, then transactions are verified by a process of 'proof of work'. This is a process involving a number of untrusted 'miners' to complete a computationally intensive process. Hence the concept of 'mining bitcoin' which involves running highly specialised and efficient processors to try and generate new blocks for the Bitcoin blockchain.

Ripple on the other hand, takes a different approach to validating transactions and simply has a number of designated trusted nodes on the network 'validators' that can form a consensus on whether a transaction is legitimate or not. This requires far less energy to do and can be done in seconds rather than hours. But, it does require a number of 'trusted' validators on the network, and that is a human process of approving who can be trusted.

The idea behind XRP is to be a central currency that is used a bridge between other currencies. At the moment, if you want to make a payment between Brazilian Real and Thai Baht then your bank needs to have an arrangement in place already to do that. This may involve 3rd party liquidity providers or correspondent banks that hold the currency on behalf of the customers banks. With Ripple and XRP, if there is a relationship from Real to XRP and one from XRP to Baht then the network will path find an exchange route for you. This may even involve intermediate currencies, so your payment may actually go BRL -> USD -> EUR ->  THB using XRP as the 'glue' in each step. All of this is done atomically by the network and transparently to the end user. 

The Ripple network can use any currency or asset at all. Anyone can set up to be an 'issuer' of a currency on the network or an asset. In theory I could use Ripple to buy shoes by paying with bananas, so long as there are issuers for each. The network will 'path find' between them.

## Investing in XRP

You can actually invest in XRP itself, and much like many other cryptocurrencies such as Bitcoin or Ethereum it has appreciated significantly in value in the past year. There are many people who think that one of the major financial institutions start using Ripple that the price of XRP is likely to increase dramatically. Commercial use cases are already in production, with the latest being [Amex doing payments to Santander in the UK via Ripple](https://ripple.com/insights/american-express-joins-ripplenet-giving-visibility-and-speed-to-global-commercial-payments/). For some more [great reasons to invest in Ripple there is a great blog post by one of the XRPChat site members 'Hodor'](https://xrphodor.wordpress.com/2017/11/16/top-five-reasons-to-invest-in-xrp/).

XRP is listed on a number of cryptocurrency exchanges such as Gatehub, or Bitstamp. [A full list is on Ripple's website.](https://ripple.com/xrp/buy-xrp/)

## What is 'rippling'

Where did Ripple get it's name from, and what is 'Rippling'. Rippling is the process of passing around a debt obligation from  one place to another. Let's explain this with an analogy I saw by one of the original Ripple founders (<s>I can no longer find the link, so paraphrasing here</s> [link found](https://gendal.me/2014/04/19/ripple-is-hard-to-understand-but-its-worth-making-the-effort-theres-a-deep-insight-at-its-core/)).

Imagine that you and I are in a cafe having lunch. I happen to owe you £10 from last week, but I don't have any cash on me, only my credit card. You, being an ordinary person, don't accept credit card payments. I notice that the cafe happens to sell iTunes vouchers at the counter. I could go and buy a £10 iTunes voucher with my credit card and give that to you. In theory a £10 iTunes voucher is worth the same as a £10 bank note, right? Well maybe. But you happen to be a die-hard Android user, and hate all things Apple. So you don't trust an iTunes voucher and would have no way of spending it anyway. So actually it is worthless to you. 

As it happens, I spot a friend of mine, Debbie, also in the cafe. She happens to (amazing coincidence) be trying to buy a CD for her nephew online for £10, but left her wallet at home with her credit cards in, and only has a crumpled £10 note in her pocket. So I buy the iTunes voucher from the cashier with my credit card, give that to Debbie, she uses it to buy her CD, and she give the £10 banknote to you. I have paid off my debt, you have a picture of the queen with £10 on it in your hand that you trust, and Debbie has managed to buy the CD for her nephew. Everyone is happy. Not only that, but it didn't require you to trust Debbie at all. She had a currency issued by someone you trusted (the Bank of England) and that was all the trust you needed.

In fact, I haven't paid my debt off at all. All I have done is move it. Rather than owe you £10, I now owe my credit card company £10. But the difference is my credit card company has extended me a £1,000 credit limit and is happy for me to borrow £10. You don't want to be owed the money and would rather have cold hard cash in your hands.

This is the process of Rippling. We have moved a debt obligation around, by way of various, in effect, IOUs for Pound Sterling currency. Each of those IOUs (the banknote, the iTunes voucher, the credit card) represent the same currency (GBP) but in different forms and with different perceived value to each person. Ripple the network allows this to happen. Again, instantly, automatically and atomically.


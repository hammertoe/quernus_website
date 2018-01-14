---
layout: post
title: Multi-currency exchange on Ripple, Pathfinding and Bridging with XRP
comments: True
tags: ripple, xrp, bitcoin, blockchain, fx
summary: Ripple has a built in distributed exchange. This is how XRP is used as a bridge currency in payments
---

<p class="message">
 This was originally a <a href="https://twitter.com/HammerToe/status/952583206154457088">Tweet thread I wrote</a>, but I have re-hashed it here for better longevity and discoverability.
</p>

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Thread: OK, let&#39;s try and demonstrate how volatility won&#39;t matter too much when making a payment on Ripple. Unlike, say, Bitcoin you can make payments in any source/destination currency on Ripple. So for example, I can send someone BTC by paying in USD 2/ <a href="https://t.co/0VPA3L1Ed1">https://t.co/0VPA3L1Ed1</a></p>&mdash; Matt Hamilton (@HammerToe) <a href="https://twitter.com/HammerToe/status/952583206154457088?ref_src=twsrc%5Etfw">January 14, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

This week [Ripple and Moneygram announced a partnership](http://ir.moneygram.com/releasedetail.cfm?ReleaseID=1054088) to use Ripple and their XRP digital asset as part of their process for transferring money about.

On Twitter, a number of people have wondered how XRP fits into this process. And with the recent price surges and drops in XRP how that would affect things. Surely if the price of XRP is volatile then that creates risk when doing currency exchanges with it.

Actually, no, it doesn't really. One of the really cool things about Ripple that many people don't realise (or overlook the power of) is that it has a built in decentralised exchange. Given the point of Ripple is to improve cross-border payments, this makes a lot of sense. However some people don't understand how this would work, and how someone like Moneygram would use it in conjunction with XRP.

OK, let's try and demonstrate how volatility won't matter too much when making a payment on Ripple. Unlike, say, Bitcoin you can make payments in any source/destination currency on Ripple. So for example, I can send someone BTC by paying in USD.

Let's look at an actual transaction that does this: 

[70CC6628FB1A03EEAC42E68A0BAA71788C3CD0A93460196B4724301EA59E6599](https://xrpcharts.ripple.com/#/transactions/70CC6628FB1A03EEAC42E68A0BAA71788C3CD0A93460196B4724301EA59E6599) 

this is a transaction on the open, public XRP Ledger (blockchain). It was just randomly picked as the first one I found, and was from 20 minutes ago. It is someone paying 0.22 BTC and funding that with 2,996 USD.

You will notice this is a single transaction on the network. A single atomic unit of work that has happened. Yet it changes 43 nodes in the ledger. If you scroll down you will see a USD/XRP offer node, and a XRP/BTC offer node that were modified.

these are offer nodes on the order book. Someone has said "I have some BTC I'll sell for XRP" and someone has said "I have some XRP to sell for USD". The Ripple matching engine has found these automatically. All the sender did was say "I want to send BTC by paying in USD"

The Ripple matching engine has looked at all the open offers and decided that this is the best 'path'. ie, the most cost efficient way to get USD -> BTC. The reason it was likely cost effective is there were lots of offers open for USD/XRP and XRP/BTC at the time. This is where the utility of XRP comes in. If all other currencies have a pair with XRP, then you can get from any currency to any other currency via XRP. You no longer need to have direct pairings between each and every currency combination.  

The payment transaction 'consumed' a number of those open offers in order to fulfil the requirements of the sender, from cheapest, to more expensive. Hence each offer will likely have a slightly different exchange rate, as they will be offering different rates.

But they key point here is that OVERALL the exchange rate to the end user was a single rate of 13,618 USD/BTC. This transaction was completed in about 3 seconds and cost 0.000015 XRP (0.003 cents).

The point here being that XRP was used a bridge currency between USD and BTC, yet neither the sender nor the recipient held XRP. It was supplied by the market. By the people holding XRP and putting offers on the order books.

I can actually ask Ripple to give me the order book for, say BTC to ETH and it will construct a 'synthetic' order book based on autobridging other orders. e.g. if there is an offer from BTC to XRP and one from XRP to ETH, then Ripple can construct a synthetic offer from BTC to ETH and give me the price for it.

And hence the volatility of XRP itself is not much concern here, as the entire transaction from USD to XRP to BTC is atomic. In fact the sender doesn't know of care what the price of XRP even is. It could be $0.2 or $200. Doesn't matter to them. 

The price of XRP being higher is helpful, as it increases the liquidity on the network. A higher value XRP can convey a higher value of other currencies.

This is why I, personally, am investing in XRP and think it will be a good investment in the long run. I think Ripple will be successful and that a lot of other partnership announcements like this will come out in 2018 and beyond. And, ultimately, supplies of XRP will be needed to make this work. Whilst there is a lot of XRP in circulation, it is actually quite a small amount compared to the $5 trillion that is moved every single day on the foreign exchange markets.
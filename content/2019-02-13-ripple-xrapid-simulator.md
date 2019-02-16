---
layout: post
title: Ripple xRapid Simulator
comments: True
tags: xrp, cryptocurrencies, ripple, banks, fintech
summary: In order to try and get a feel for the potential viability of payments using Ripple's xRapid system, I thought I'd knock up a quick simulator to calculate the actual price of a transfer using xRapid to compare to the current money transfer options
---

So, Ripple have this piece of software called xRapid. The role of xRapid, for those that don't know, is to be an "on demand liquidity sourcing solution". So what does that mean? It means that xRapid uses public liquidity pools -- in this case crypto currency exchanges -- and buys and sells a digital asset (XRP) on demand, to satisfy a payment.

So in order to send a payment from, say Mexico to Thailand, it goes something like this:

1. Customers Mexican Pesos (MXN) are sent by local payment system to a local exchange in Mexico
2. The MXN are sold for XRP on the exchange
3. The XRP are send across the XRP Ledger to a destination exchange in Thailand
4. The XRP are sold for Thai Baht (THB) on the Thai exchange
5. The Thai Baht are sent via local payment system to the destination bank account in Thailand

All of that happens in under a minute, and is fully orchastrated by xRapid. The customer doesn't see any of it. All they know is that their payment has been made and got there in under a minute. As opposed to the 3 days it would likely take using the main alternative, SWIFT.

So this process involves:

- 2 x local payments
- 2 x FX exchanges
- 1 x payment over the XRP Ledger

Some people say "How can that be cheaper than the current system?! You have two FX exchanges in there, with their associated fees and spreads". Recently a customer of Ripple, Mercury FX were telling of the cost savings they made using xRapid to make a payment from the UK to Mexico, and they supposedly made a saving of nearly £80 on a £3,500 transaction:

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">1/2 UK-based Mustard Foods saved £79.17 and 31 hours on the transaction.</p>&mdash; Mercury-fx Ltd (@mercury_fx_ltd) <a href="https://twitter.com/mercury_fx_ltd/status/1085915011636187138?ref_src=twsrc%5Etfw">January 17, 2019</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


To explore this a bit, I wrote a quick and dirty simulator to try and get a feel for the costs involved. The simulator connects to two exchanges and checks the current order books on each one and works out the cost of the two FX transactions using actual real order book data. This means it gives a feel for the size of the orders that xRapid could process at the moment.

The [code of the simulator is on Github](https://github.com/hammertoe/xrapid-sim) so anyone can have a play with it.

Let's have a go shall we and see if the savings claim of Mercury FX stacks up. Firstly, there are not any actual xRapid exchanges (that I know of) in the UK and using GBP. So I'm going to assume that they actually had an EUR account and started the transaction from there. 

Let's assume then that they were making a €4,000 EUR payment to Mexico. We know that Bitstamp is an xRapid-enabled exchange in Europe, and that Bitso is an xRapid-enabled exchange in Mexico.

```text
$ python xrapid-sim.py 4000 bitstamp EUR bitso MXN 
Getting order book for XRP/EUR from Bitstamp
+ Bought 9232.40 XRP @ 0.2653
+ Bought 5842.16 XRP @ 0.2654
Total Bought: 15074.56 XRP
Buy trade fee: 37.69 XRP
Net: 15036.87 XRP

Sending the 15036.87 XRP from Bitstamp to Bitso

Getting order book for XRP/MXN from Bitso
- Sold 1313.89 XRP @ 5.7000
- Sold 4046.21 XRP @ 5.6900
- Sold 9676.77 XRP @ 5.6800
Total dest amount: 85476.17 MXN
Sell trade fee: 555.60 MXN
Net: 84920.57 MXN
```

From the above, you can see that the end result was 84,920 MXN. It required using up the first two levels of orders on the orderbooks at Bitstamp, and used the first three levels of orders on the orderbooks at Bitso. It also calculated the trade fee at both ends of the transaction and deducted that from the resultant amount from the trades.

It assumes that the cost to transfer on the XRP Ledger is negligible (it is thousandths of a cent per payment), and assumes there are no deposit/withdrawal fees at each end. It also doesn't include whatever cut Mercury FX take of the transaction. 

How does that compare? Well, Transferwise will helpfully tell me how their service compares to the banks, so lets see what it would cost with them:

![Transferwise price comparison EUR to MXN](/public/transferwise-eur-mxn.png)

As we can see, Transferwise's prices are pretty good, and at 86,511.88 MXN, you would get about 1.8% better rate with Transferwise. But that said, it would take 5 days from today to get there! It is the 16th Feb now, and it estimates it should arrive by 21st Feb. 

Transferwise gives us the comparison to four other banks. One of those banks Rabobank, is better than our rate above with xRapid. But the other three are worse. If we take the example of BBVA then you would get 83,010.71 MXN. Which is 1,910 MXN less than we would get with xRapid. How much is 1,910 MXN? Approximately £77. 

**Which is very much in line with the £79.17 that Mercury FX claimed their client saved**.

So I'd say it is very feasible that the cost savings are very real and in line with that has been claimed.

For further fun, you can use the xRapid simulator to test what transfers would cost between any exchange supported by the [CCXT library used](https://github.com/ccxt/ccxt).

For example, want to pretend that the Braziliex exchange is xRapid enabled, and you want to send Brazilian Real to Mexico?

```text
$ python xrapid-sim.py 4000 braziliex BRL bitso MXN
Getting order book for XRP/BRL from Braziliex
+ Bought 3508.77 XRP @ 1.1400
Total Bought: 3508.77 XRP
Buy trade fee: 17.54 XRP
Net: 3491.23 XRP

Sending the 3491.23 XRP from Braziliex to Bitso

Getting order book for XRP/MXN from Bitso
- Sold 1249.25 XRP @ 5.7000
- Sold 396.26 XRP @ 5.6800
- Sold 1845.72 XRP @ 5.6700
Total dest amount: 19836.70 MXN
Sell trade fee: 128.94 MXN
Net: 19707.76 MXN
```

Transferwise says they could do it for a better rate resulting in 20,226 MXN. Again, it won't get there for 4 days, until the 20th Feb.

They do give the option of Paypal for cost comparison. Which whilst might be quick, only gives you 17,550 MXN. A whopping 12% lower rate than you would get with xRapid!

![Transferwise price comparison BRL to MXN](/public/transferwise-brl-mxn.png)

And, for even more fun, you can even use a different 'transport' cryptocurrency if you want. Whilst XRP is of course the one we are interested in as it is so cheap and fast to move about, using BTC in examples opens up the chance to play with other exchanges that don't list XRP yet. e.g. want to test sending 4 million Indonesian Rupiah to Mexico, using Bitcoin at the transport?

```text
$ python xrapid-sim.py 4000000 indodax IDR bitso MXN --transport BTC
Getting order book for BTC/IDR from INDODAX
+ Bought 0.03 BTC @ 50990000.0000
+ Bought 0.01 BTC @ 50992000.0000
+ Bought 0.01 BTC @ 50993000.0000
+ Bought 0.01 BTC @ 50995000.0000
+ Bought 0.00 BTC @ 50998000.0000
+ Bought 0.01 BTC @ 51000000.0000
Total Bought: 0.08 BTC
Buy trade fee: 0.00 BTC
Net: 0.08 BTC

Sending the 0.08 BTC from INDODAX to Bitso

Getting order book for BTC/MXN from Bitso
- Sold 0.07 BTC @ 68599.0000
- Sold 0.01 BTC @ 68500.0000
Total dest amount: 5364.03 MXN
Sell trade fee: 34.87 MXN
Net: 5329.16 MXN
```

In this case, Transferwise can't give me a price for this. That is because they don't have IDR -> MXN as a payment route. One of the main aims of xRapid is to remove the need for pre-funding of accounts at each end. This means that more 'exotic' payment routes will be possible without having each bank holding such a vast array of exotic (to them!) currencies.


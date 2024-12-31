# Trading Strategy based on Trading with Siddhant

*Direction, Area and Trigger (DAT Framework) is the core to the strategy*

1. Direction
- Look at 1D(daily chart) to identify the trend(Uptrend or downtrend). 
- If trading in side of trend full qty else half qty

2. Area
- Use supply and demand zones and trendlines.
- Use 1D, 1H and 15m chart for marking the areas.
- Supply and demand zones should have multiple touch points(atleast 2) or should have one big movement to be considered as valid zone.
- For trendline two or more touch points

Tips for Area
1. If zone is broken twice than it is no longer valid.
2. If zone is broken once then wait for it to show that it is still valid by adding one more touch point to the same zone.
3. If trendline is broken and you don't get trade at reversal or retest then delete it.
4. If two areas or trendlines are closer to each other then remove one of them.

3. Trigger
- Candlestick patterns act as triggers
- Two types
    1. Continuation
    - Inside candle 

    2. Reversal
    - pinbar ( hammer (at demand), shooting star (at supply))
    - engulfing ( bullish (at demand), bearish (at supply))
    - star patterns (Morning Star (at demand), Evening Star (at supply))
- Enter at the break of the pattern and keep the SL at high or low of the candlestick when inside of trend if against then place it below the zones or swing.
- Range of candle is also a trigger,

Tips for Trigger
1. It is important to understand the difference of Continuation and Reversal. 
    - If the price is reached the supply zone and if it forms an Inside candle then you will take trade only when the high of the mother candle is taken out, if the low gets taken out then we don't take trade. This is called continuation.
    - Instead if it forms shooting star, then we take trade if the low of the shooting star is taken out, we won't take trade if the high of the shooting star is taken out. This is called Reversal.
2. First trigger is the best trigger try to place your Stop loss there even if you miss the trade and another trigger was formed.
3. It is not necessary that the high or low of the pattern should be taken out in the next candle itself, it may be taken out in the subsequent candles only if it's opposite side should not be taken out.


# Risk Management 
1. Don't try to make your SL smaller purposely keep it in comfortable position.
2. If trading in side of trend full qty else half qty, (Inside of trend 1% of capital, against the trend 0.5% of capital)
3. Max loss per day 2% of your capital
4. can take 3-5 trades per day
5. If the SL is within our capacity then we take the trade otherwise we ignore it.
6. We will use trailing SL, First target 1:1, then trail your SL to cost and book profit and target is 1:2, then trail your SL to 1:1 and book profit and target is 1:3 and finally book the profits at 1:3.
7. I think the above process of trailing SL won't give us enough profits, try 1:1.25 and book full qty. The Reason is it is hard to hit 1:3 and even if we hit it we will won't get +3% we will get +2% and with brokerage it will be +1.7%. But in the new method we will hit 1:1.25 more frequent then 1:3 or 1:2 and we will make +1% (including brokerage). 
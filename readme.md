## 回测指令
`zipline run -f run.py --start [start-date] --end [end-date] -o [output file] --capital-base [starting-capital]`

eg.
`zipline run -f run.py --start 2017-1-1 --end 2018-1-1 -o dma.pickleclear --capital-base 100000`


## Context object 解释
1. Orders: 所有的历史订单
2. Open orders: 这一交易周期下的订单


## output file 中数据项解释

1. Capital used: 这一期花了多少钱
2. Ending cash: portfolio 里面还有多少钱可以用
3. Ending value: 这周期完后仓位里有多少钱
4. Portfolio value: 总金额
5. position: 仓位
6. orders: 这周期买/卖的
7. Algorithm period return: 策略周期收益

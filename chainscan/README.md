
```


all_pairs --- 


```


```
apps:
    [desktop]
            |
            /templates
                - [desktop.html, ]
            /models
                - [Desktop]
            /views
                - [get_pairs]
    [user] _
          |
          /templates
            -[user.html, pairs.html]
          /models
            -[User]

    [blockchains]
                |
                /templates
                    - [dekstop.html, bsc.html, AURORA.html]
                /models
                    - [BscTransaction,  Aurora]
                    - [Pair, BSCPair, Deals]
                        -Pair{blockChain, factoryAddress, pairAddress, pairSymbol, token0, token1}
    
```
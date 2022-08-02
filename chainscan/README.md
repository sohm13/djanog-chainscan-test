
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
                        - PairTransaction{pair=ForengeyKey:Pair, reserveToken0, reserveToken1, amount0In, amount1In, amount0Out, amount1Out, maker}
    [bsc]
        |
        /templates
            - [desktop.html, transactions]
        /models
            - [Transcation, TranscationReceipt]
    

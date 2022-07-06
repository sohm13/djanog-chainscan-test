models:
[user] - [FitlerLog]
            |
        [transaction]


templates:
[user.html] - [pairs.html] - [add-pair]-


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
                    - [Bsc, Aurora]
    


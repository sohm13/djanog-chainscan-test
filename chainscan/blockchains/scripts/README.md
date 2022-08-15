## events_inpsect_app
    - events_inpsect package - give data from blockchain 


---------------
**module dependencies:**

```
package:
____________________________
blockchain_scan -->-- [events, schemas]
events -->-- [schemas, decode]
web3_provider -->-- [config]
contract_calls -->-- [abi]
helper -->-- [config, schemas,web3_provider, contract_calls, utils]
utils -->-- [schemas]

____________________________

example_app -->-- [blockchain_scan, web3_provider, helper, utils]
```



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
____________________________

app -->-- [blockchain_scan, web3_provider]
app_contract -->-- [contract_calls, web3_provider]
```
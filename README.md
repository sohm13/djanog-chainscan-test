
```
Смысл, собираем данные из блокченов(пример https://bscscan.com/),
собираем траназкции где есть сделки(обмены токенов),
собираем результаты обменов в бд
```
```
импользуем services.events_inspect_app обновляем дб;
    - management/commands/add_pairs -> to models.BaseEthPair
    - management/commands/update_db_async -> to models.BaseBlock, models.BaseEthSyncEvent

services.events_inspect_app.events_inspect.config - настройки какие данные собирать
```

```
views:
    BscListView from models.BaseEthPair
    AuroraListView from models.BaseEthPair
    bsc_pair_detail form models.BaseEthSyncEvent 
    aurora_pair_detail form models.BaseEthSyncEvent 
```

  ### чтобы тестового запустить 
  ```
  pip install -r requirements.txt
  ### ongoing loop
  python run_app_script.py
  ### ongoing loop
  python run_server.py #
  ```


 
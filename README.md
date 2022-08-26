
Тема; собирать и анализировать данные из блокчейнов типа bsc, eth
Цель;
``` 
    [OK] научиться собирать и обрабатывать нужные данные с блокчейна
    [OK] Забписвать их в бд и анализировать
    [OK] Сделать визуальное отображения данных на сайти
    [OK] Запустить сайт на серваке
```
Использовал;
```
    web3 - для работы с блокченами
    pandas - для анализа данных
    django - для сайта
    sqlite - как бд
```
Что дальше;
```
 Использовать postrges db
 Оптимизировать запросы в bd
 Оптимизировать изображения данных на страници
 Оптимизировать обновления данных онлайн

```


Памятка;
```
импользуем services.events_inspect_app обновляем дб;
    - management/commands/add_pairs -> to models.BaseEthPair
    - management/commands/update_db_async -> to models.BaseBlock, models.BaseEthSyncEvent

services.events_inspect_app.events_inspect.config - настройки какие данные собирать
```

  ### быстрый запуск
  ```
  pip install -r requirements.txt
  ### ongoing loop
  python run_app_script.py
  ### ongoing loop
  python run_server.py #
  ```


 
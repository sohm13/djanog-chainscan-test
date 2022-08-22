import os
from concurrent.futures import ThreadPoolExecutor 


os.system("python ./chainscan/manage.py makemigrations")
os.system("python ./chainscan/manage.py migrate")

os.system('python ./chainscan/manage.py add_pairs')
os.system('python ./chainscan/manage.py update_new_pairs')
os.system('python ./chainscan/manage.py update_db_loop')


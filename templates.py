import os
from pathlib import Path
import logging

# Set up logging format correctly
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

list_of_files = [
    'resources/MBSD-chatbot.ipynb',
    'src/helper.py',
    'src/__init__.py',
    '.env',
    'requirements.txt',
    'setup.py',
    'main.py',
    'store_index.py',
    'static/style.css',
    'static/script.js',
    'templates/index.html',
]

for file_path in list_of_files:

    file_path = Path(file_path)
    filedir, filename = os.path.split(file_path)

    if filedir != '':
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory created: {filedir} for the file {filename}")

    # Use file_path for size check, not filename
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
        logging.info(f"Creating file: {file_path}")
    else:
        logging.info(f"File already exists: {file_path}")

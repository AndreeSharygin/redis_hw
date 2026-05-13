import logging

# Настройка логирования
logging.basicConfig(filename='notify.log', level=logging.INFO)

def write_log(article_id: int):
    logging.info(f"Article {article_id} created")
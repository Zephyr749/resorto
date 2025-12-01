import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
    filemode='a',
    filename='modules/common/logs.txt'
)

def get_logger(name):
    return logging.getLogger(name)
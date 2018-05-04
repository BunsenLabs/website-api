import logging
logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def named_logger(name:str = "main") -> logging.Logger:
  logger = logging.getLogger(name=name)
  logger.setLevel(logging.INFO)
  return logger

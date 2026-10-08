import logging

logging_level = logging.INFO
logging_filename  = "run.log"
logging_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging_datefmt = '%Y-%m-%D %H:%M:%S'
console_format = '%(asctime)s : %(levelname)s : %(message)s'

logging.basicConfig(level=logging_level, \
                    format=logging_format, \
                    datefmt=logging_datefmt, \
                    filename=logging_filename, \
                    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging_level)
formatter = logging.Formatter(console_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

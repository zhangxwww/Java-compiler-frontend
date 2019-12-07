import sys
import logging

from lexical import lexer
from syntax import parser

logging.basicConfig(
    level=logging.DEBUG,
    filename='parse.log',
    filemode='w',
    format='%(filename)10s:%(lineno)4d:%(message)s'
)
log = logging.getLogger()

if __name__ == '__main__':
    filename = sys.argv[1]
    s = open(filename).read()
    root = parser.parse(s, lexer=lexer, debug=log)
    print(root)

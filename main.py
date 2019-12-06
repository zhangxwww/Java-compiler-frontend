import sys
from lexical import lexer

if __name__ == '__main__':
    filename = sys.argv[1]
    lexer.input(open(filename).read())
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

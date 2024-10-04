import re
import string
import sys


def is_number(s):
    return (re.fullmatch('[-|+]?[0-9]+', s) or
            re.fullmatch('[-|+]?[0-9]+.[0-9]+', s) or
            re.fullmatch('[-|+]?[0-9].[0-9]*[e|E][-|+][0-9]+', s))


def is_kword(word):
    return re.fullmatch("[_a-zA-Z][_a-zA-Z0-9]*", word)


def lexer(file0):
    state = "H"
    file = open(file0, "r")
    # 0 ключевые слова 1 разделители 2 числа 3 идентификаторы 4 равно
    table = [[], ['(', ')', ';', '=', '<', '>'], [], []]
    c = file.read(1)
    while c != "":
        if state == "H":
            if c in " \n\r\t":
                c = file.read(1)
                continue
            elif c == ":":
                state = "ASGN"
            elif c == "_" or c in string.ascii_letters:
                state = "ID"
            elif c in "-+." or c in string.digits:
                state = "NM"
            else:
                state = "DLM"
        elif state == "NM":
            num = c
            while True:
                c = file.read(1)
                if c in string.digits or c in "eE.-+":
                    num += c
                else:
                    break
            if is_number(num):
                print(2, len(table[2]))
                table[2].append(num)
                state = "H"
            else:
                state = "ERR"
        elif state == "ASGN":
            if file.read(1) == "=":
                print(5, 0)
                c = file.read(1)
                state = "H"
            else:
                state = "ERR"
        elif state == "DLM":
            if c in "();<>=":
                state = "H"
                print(1, table[1].index(c))
                c = file.read(1)
            else:
                state = "ERR"
        elif state == "ID":
            word = c
            while True:
                c = file.read(1)
                if c == "_" or c in string.ascii_letters or c in string.digits:
                    word += c
                else:
                    break
            if is_kword(word):
                state = "H"
                if word in table[3]:
                    print(3, table[3].index(word))
                else:
                    print(3, len(table[3]))
                    table[3].append(word)

            else:
                state = "ERR"
        elif state == "ERR":
            raise Exception(state + ": " + c)
    print(table)
    return table


if __name__ == '__main__':
    try:
        lexer('prac3 (lexer)/prog.txt')
    except Exception as e:
        print(e)
    # print(is_number("-1.101e-23"))

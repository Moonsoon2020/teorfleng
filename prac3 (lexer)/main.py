import re
import string


def is_number(s):
    """Проверяет, является ли строка числом в различных форматах."""
    s = s.lower()
    if re.fullmatch(r'[-+]?[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?', s):
        return 3  
    elif re.fullmatch(r'[01]+b', s):
        return 4  
    elif re.fullmatch(r'[0-7]+o', s):
        return 5  
    elif re.fullmatch(r'[0-9a-fA-F]+h', s):
        return 6  
    elif re.fullmatch(r'[0-9]+', s):
        return 2
    return 0  


key_words = ["for", "do", "mult", "div", "and", "or"]


def is_kword(word):
    """Проверяет, является ли слово ключевым словом."""
    return word in key_words


def lexer(file0):
    """
    Лексер, анализирующий текстовый файл, распознающий числа, идентификаторы,
    ключевые слова и разделители.
    """
    state = "H"  
    file = open(file0, "r")
    table = [key_words, ['=', '<>', '<=', '<', '>', '>=', '(', ')', ';', '+', "-", "!"], [], []]
    c = file.read(1)  

    while c != "":  
        if state == "H":
            if c in " \n\r\t":  
                c = file.read(1)
                continue
            elif c == ":":  
                state = "ASGN"
            elif c == "_" or c in string.ascii_letters:  # Идентификатор
                state = "ID"
            elif c in string.digits:  # Число
                state = "NM"
            else:  # Разделители
                state = "DLM"
            continue

        elif state == "NM":  
            num = c
            while True:
                c = file.read(1)
                if c in string.digits or c in "abcdABCDFfHheE.-+":
                    num += c
                else:
                    break
            num_type = is_number(num)
            if num_type:  
                print(2, len(table[2]))  
                table[2].append(num)
                state = "H"
            else:
                state = "ERR"

        elif state == "ASGN":  
            if file.read(1) == "=":
                print(5, 0)  
                state = "H"
            else:
                state = "ERR"

        elif state == "DLM":  
            if c in table[1]:
                print(1, table[1].index(c))  
            state = "H"

        elif state == "ID":  
            word = c
            while True:
                c = file.read(1)
                if c == "_" or c in string.ascii_letters or c in string.digits:
                    word += c
                else:
                    break
            state = "H"
            if not is_kword(word):  
                if word in table[3]:
                    print(3, table[3].index(word))  
                else:
                    print(3, len(table[3]))  
                    table[3].append(word)
            else:
                print(0, table[0].index(word))  

        elif state == "ERR":  
            raise Exception(f"Ошибка в состоянии {state}: {c}")

        c = file.read(1)  

    print(table)  
    return table


if __name__ == '__main__':
    try:
        lexer('prac3 (lexer)/prog.txt')  
    except Exception as e:
        print(e)
# + - or mult div and !

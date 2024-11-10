import re
import string


def is_number(s):
    """Проверяет, является ли строка числом в различных форматах."""
    s = s.lower()
    if re.fullmatch(r'[0-9]*\.[0-9]+(e[-+][0-9]+)?', s):
        return 1
    if re.fullmatch(r'[0-9]+e[+-][0-9]+', s):
        return 2
    elif re.fullmatch(r'[01]+b', s):
        return 3
    elif re.fullmatch(r'[0-7]+o', s):
        return 4
    elif re.fullmatch(r'[0-9a-fA-F]+h', s):
        return 5
    elif re.fullmatch(r'[0-9]+d', s):
        return 6
    return 0


key_words = [
    "or", "and", "not", "program", "var", "begin", "end", "integer", "real", "boolean", "as", "if", "else", "then",
    "for", "to", "do", "while", "read", "write", "true", "false"]


def is_kword(word):
    """Проверяет, является ли слово ключевым словом."""
    return word in key_words


def lexer(file0):
    """
    Лексер, анализирующий текстовый файл, распознающий числа, идентификаторы,
    ключевые слова и разделители.
    """
    result = []
    state = "H"
    file = open(file0)
    table = [key_words,
             ['=', '<>', '<=', '<', '>', '>=', '*', '/', '+', "-", "{", "}", ";", ",", "[", "]", "(", ")", ":", ","],
             [], []]
    c = file.read(1)

    while c != "":
        if state == "H":
            if c in " \n\r\t":
                c = file.read(1)
                continue
            elif c in string.ascii_letters:  # Идентификатор
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
                if (c in string.digits or c in "abcdABCDFfHheEoO.-+") and c != "":
                    num += c
                else:
                    break
            num_type = is_number(num)
            if num_type:
                result.append([2, len(table[2])])
                table[2].append(num)
                state = "H"
            else:
                state = "ERR"
            continue
        elif state == "DLM":
            text = c
            c = file.read(1)
            text += c
            if text in table[1]:
                result.append([1, table[1].index(text)])
                c = file.read(1)
                state = "H"
                continue
            elif text[0] in table[1]:
                if text[0] == "{":
                    c = file.read(1)
                    while c != "}":
                        c = file.read(1)
                    c = file.read(1)
                    state = "H"
                    continue
                else:
                    result.append([1, table[1].index(text[0])])
                    state = "H"
                    continue
            else:
                state = "ERR"
        elif state == "ID":
            word = c
            while True:
                c = file.read(1)
                if (c in string.ascii_letters or c in string.digits) and c != "":
                    word += c
                else:
                    break
            state = "H"
            if not is_kword(word):
                if word in table[3]:
                    result.append([3, table[3].index(word)])
                else:
                    result.append([3, len(table[3])])
                    table[3].append(word)
            else:
                result.append([0, table[0].index(word)])
            continue
        elif state == "ERR":
            raise Exception(1)

        c = file.read(1)
    if state == "ERR":
        raise Exception(0)
    return table, result


if __name__ == '__main__':
    try:
        lexer('kurs/prog.txt')
    except Exception as e:
        print(e)

import re
import string
from os import write


def is_number(s):
    """Проверяет, является ли строка числом в различных форматах."""
    s = s.lower()
    if re.fullmatch(r'[0-9]*\.[0-9]+(e[-+][0-9]+)?', s):
        return 3
    if re.fullmatch(r'[0-9]+e[+-][0-9]+', s):
        return 2
    elif re.fullmatch(r'[01]+b', s):
        return 4
    elif re.fullmatch(r'[0-7]+o', s):
        return 5
    elif re.fullmatch(r'[0-9a-fA-F]+h', s):
        return 6
    elif re.fullmatch(r'[0-9]+d', s):
        return 2
    return 0


key_words = [
    "or", "and", "not", "program", "var", "begin", "end", "integer", "real", "boolean", "as", "if", "else", "then",
    "for", "to", "do", "while", "read", "write"]


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
    file = open(file0, "r")
    table = [key_words,
             ['=', '<>', '<=', '<', '>', '>=', '*', '/', '+', "-", "{", "}", ";", ",", "[", "]", "(", ")", ":", ","],
             [], []]
    c = file.read(1)

    while c != "":
        if state == "H":
            if c in " \n\r\t":
                c = file.read(1)
                continue
            elif c == "_" or c in string.ascii_letters:  # Идентификатор
                state = "ID"
            elif c in string.digits + ".":  # Число
                state = "NM"
            else:  # Разделители
                state = "DLM"
            continue

        elif state == "NM":
            num = c
            while True:
                c = file.read(1)
                if c in string.digits or c in "abcdABCDFfHheEoO.-+":
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
                if c == "_" or c in string.ascii_letters or c in string.digits:
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
            raise Exception(f"Ошибка в состоянии {state}: {c}")

        c = file.read(1)
    if state == "ERR":
        raise Exception(f"Ошибка в состоянии {state}: {c}")
    return table, result


# def remove_comments(tokens, table):
#     result = []
#     flag = False
#     for token in tokens:
#         if token[0] == 1 and token[1] == table[1].index("}") and flag:
#             flag = False
#             continue
#         if token[0] == 1 and token[1] == table[1].index("{"):
#             flag = True
#             continue
#         if not flag:
#             result.append(token)
#     return result
# def desc_enum(tokens, table):
#     if tokens[0][0] ==

def desc(tokens, table):
    tokens.pop(0)
    if tokens[0][0] == 3:
        tokens.pop(0)
        if tokens[0][0] == 1 and tokens[0][1] == table[1].index(","):
            desc(tokens, table)
        elif tokens[0][0] == 1 and tokens[0][1] == table[1].index(":"):
            tokens.pop(0)
            if tokens[0][0] == 0 and (tokens[0][1] == table[0].index("integer")
                                      or tokens[0][1] == table[0].index("real")
                                      or tokens[0][1] == table[0].index("boolean")):
                tokens.pop(0)
                return
            raise Exception()
        else:
            raise Exception()
    else:
        raise Exception()


def if_(tokens, table):
    pass


def for_(tokens, table):
    pass


def while_(tokens, table):
    pass


def pr(tokens, table):
    pass


def read_(tokens, table):
    pass


def write_(tokens, table):
    pass


def operations(tokens, table):
    token = tokens.pop(0)
    if token[0] == 1 and token[1] == table[1].index("["):
        operations(tokens, table)
    elif token[0] == 1 and token[1] == table[1].index("]"):
        operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("if"):
        if_(tokens, table)
        # operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("for"):
        for_(tokens, table)
        # operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("while"):
        while_(tokens, table)
        # operations(tokens, table)
    elif token[0] == 3:
        pr(tokens, table)
        # operations(tokens, table)
    elif token[0] == 1 and token[1] == table[1].index(";"):
        operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("read"):
        read_(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("write"):
        write_(tokens, table)
    else:
        raise Exception()


def syntax(tokens, table):
    # tokens = remove_comments(tokens, table)
    token = tokens.pop(0)
    while token[0] == 0 and token[1] == table[0].index("program"):
        token = tokens[0]
        if token[0] == 0 and token[1] == table[0].index("var"):
            desc(tokens, table)
            token = tokens.pop(0)
            if token[0] == 0 and token[1] == table[0].index("begin"):
                tokens.pop(0)
                while True:
                    if len(tokens) == 0:
                        raise Exception()
                    elif tokens[0][0] == 0 and tokens[0][1] == table[0].index("end"):
                        break
                    operations(tokens, table)
            print()
        else:
            raise Exception()


if __name__ == '__main__':
    try:
        var = lexer('prac3 (lexer)/prog.txt')
        print(*var, sep='\n')
        print(syntax(var[1], var[0]))
    except Exception as e:
        print(e)

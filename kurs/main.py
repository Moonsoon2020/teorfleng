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
            elif c in string.ascii_letters:  # Идентификатор
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
                if (c == "_" or c in string.ascii_letters or c in string.digits) and c != "":
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
            raise Exception(f"Ошибка в состоянии {state}: {c}", 1)

        c = file.read(1)
    if state == "ERR":
        raise Exception(f"Ошибка в состоянии {state}: {c}", 1)
    return table, result


var = []


def parse_declaration(tokens, table):
    """Парсинг объявления переменной."""
    tokens.pop(0)
    if tokens[0][0] == 0 and (tokens[0][1] == table[0].index("integer")
                              or tokens[0][1] == table[0].index("real")
                              or tokens[0][1] == table[0].index("boolean")):
        tokens.pop(0)
        while tokens[0][0] == 3:
            token = tokens.pop(0)
            var.append(token[1])
            if tokens[0][0] == 1 and tokens[0][1] == table[1].index(","):
                tokens.pop(0)
                continue
            else:
                break
        if len(var) < 1:
            raise Exception(3)
    else:
        raise Exception(4)


def parse_mult(tokens, table):
    """Парсинг члена операнда."""
    flag = [table[0].index("false"), table[0].index("true")]
    token = tokens.pop(0)
    if token[0] == 0 and token[1] in flag:
        return
    if token[0] == 1 and token[1] == table[1].index("("):
        parse_expression(tokens, table)
        if tokens[0][0] == 1 and tokens[0][1] == table[1].index(")"):
            tokens.pop(0)
            return
        else:
            raise Exception(5)
    if token[0] == 3 and token[1] in var:
        return
    if token[0] == 2:
        return
    if token[0] == 0 and token[1] == table[0].index("not"):
        parse_mult(tokens, table)
        return
    raise Exception(6)


def parse_slg(tokens, table):
    parse_mult(tokens, table)
    if ((tokens[0][0] == 1 and (tokens[0][1] == table[1].index("*") or tokens[0][1] == table[1].index("/")))
            or (tokens[0][0] == 0 and (tokens[0][1] == table[0].index("and")))):
        tokens.pop(0)
        parse_mult(tokens, table)


def parse_operand(tokens, table):
    parse_slg(tokens, table)
    if ((tokens[0][0] == 1 and (tokens[0][1] == table[1].index("+") or tokens[0][1] == table[1].index("-")))
            or (tokens[0][0] == 0 and (tokens[0][1] == table[0].index("or")))):
        tokens.pop(0)
        parse_slg(tokens, table)


def parse_expression(tokens, table):
    """Парсинг выражения."""
    parse_operand(tokens, table)
    if tokens[0][0] == 1 and tokens[0][1] in [table[1].index(op) for op in ["=", "<>", ">", "<", ">=", "<="]]:
        tokens.pop(0)
        parse_expression(tokens, table)


def parse_if(tokens, table):
    """Парсинг конструкции if."""
    parse_expression(tokens, table)
    if tokens[0][0] == 0 and tokens[0][1] == table[0].index("then"):
        tokens.pop(0)
        parse_operation(tokens, table)
        if tokens[0][0] == 0 and tokens[0][1] == table[0].index("else"):
            tokens.pop(0)
            parse_operation(tokens, table)
    else:
        raise Exception(7)  # Ошибка if-then


def parse_for(tokens, table):
    if tokens[0][0] != 3:
        raise Exception(8)
    tokens.pop(0)
    parse_eq(tokens, table)
    if tokens[0][0] == 0 and tokens[0][1] == table[0].index("to"):
        tokens.pop(0)
        parse_expression(tokens, table)
        if tokens[0][0] == 0 and tokens[0][1] == table[0].index("do"):
            tokens.pop(0)
            parse_operation(tokens, table)
        else:
            raise Exception(9)
    else:
        raise Exception(10)


def parse_while(tokens, table):
    parse_expression(tokens, table)
    if tokens[0][0] == 0 and tokens[0][1] == table[0].index("do"):
        tokens.pop(0)
        parse_operation(tokens, table)


def parse_eq(tokens, table):
    token = tokens.pop(0)
    if token[0] == 0 and token[1] == table[0].index("as"):
        parse_expression(tokens, table)
    else:
        raise Exception(11)


def parse_read(tokens, table):
    opentoken = tokens.pop(0)
    if opentoken[0] == 1 and opentoken[1] == table[1].index("("):
        ind_token = tokens.pop(0)
        if ind_token[0] == 3:
            while tokens[0][0] == 1 and tokens[0][1] == table[1].index(","):
                tokens.pop(0)
                if tokens[0][0] == 3:
                    tokens.pop(0)
                else:
                    raise Exception(12)
            if tokens[0][0] == 1 and tokens[0][1] == table[1].index(")"):
                tokens.pop(0)
            else:
                raise Exception(13)
        else:
            raise Exception(14)
    else:
        raise Exception(15)


def parse_write(tokens, table):
    if not (tokens[0][0] == 1 and tokens[0][1] == table[1].index("(")):
        raise Exception(16)
    tokens.pop(0)
    parse_expression(tokens, table)
    while tokens[0][0] == 1 and tokens[0][1] == table[1].index(","):
        tokens.pop(0)
        parse_expression(tokens, table)
    if not (tokens[0][0] == 1 and tokens[0][1] == table[1].index(")")):
        raise Exception(17)
    tokens.pop(0)


def composite_operations(tokens, table):
    token = tokens.pop(0)
    if token[0] == 1 and token[1] == table[1].index("["):
        composite_operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("if"):
        parse_if(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("for"):
        parse_for(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("while"):
        parse_while(tokens, table)
    elif token[0] == 3:
        parse_eq(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("read"):
        parse_read(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("write"):
        parse_write(tokens, table)
    if tokens[0][0] == 1 and tokens[0][1] == table[1].index("]"):
        tokens.pop(0)
        return
    if tokens[0][0] == 1 and tokens[0][1] == table[1].index(":"):
        tokens.pop(0)
        composite_operations(tokens, table)
    else:
        raise Exception(18)

def parse_operation(tokens, table):
    token = tokens.pop(0)
    if token[0] == 1 and token[1] == table[1].index("["):
        composite_operations(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("if"):
        parse_if(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("for"):
        parse_for(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("while"):
        parse_while(tokens, table)
    elif token[0] == 3 and token[1] in var:
        parse_eq(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("read"):
        parse_read(tokens, table)
    elif token[0] == 0 and token[1] == table[0].index("write"):
        parse_write(tokens, table)
    else:
        raise Exception(19)

def parse_operations(tokens, table):
    parse_operation(tokens, table)
    if tokens[0][0] == 1 and tokens[0][1] == table[1].index(";"):
        tokens.pop(0)
        parse_operations(tokens, table)


def syntax(tokens, table):
    """Основная синтаксическая проверка программы."""
    token = tokens.pop(0)
    while token[0] == 0 and token[1] == table[0].index("program"):
        token = tokens[0]
        if token[0] == 0 and token[1] == table[0].index("var"):
            parse_declaration(tokens, table)
            token = tokens.pop(0)
            if token[0] == 0 and token[1] == table[0].index("begin"):
                parse_operations(tokens, table)
                if tokens[0][0] == 0 and tokens[0][1] == table[0].index("end"):
                    tokens.pop(0)

        else:
            raise Exception(21)  # Ошибка в синтаксисе после program
    if len(tokens) != 0:
        raise Exception(22)  # Ошибка неиспользованных токенов


if __name__ == '__main__':
    try:
        tokens_and_table = lexer('kurs/prog.txt')
        print(*tokens_and_table, sep='\n')
        syntax(tokens_and_table[1], tokens_and_table[0])
        print("Ошибки не обнаружены")
    except Exception as e:
        print(f"{str(e)} err")

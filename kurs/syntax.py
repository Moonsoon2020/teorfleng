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
            if token[1] in var:
                raise Exception(2)
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
    if token[0] == 0 and token[1] == table[0].index("program"):
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
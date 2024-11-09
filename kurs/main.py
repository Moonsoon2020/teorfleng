import sys

from lexer import lexer
from syntax import syntax

if __name__ == '__main__':
    try:
        filename = "kurs/prog.txt"
        for i, line in enumerate(open(filename)):
            print(str(i)+":", line, end="")
        print()
        tokens_and_table = lexer(filename)
        # print(*tokens_and_table, sep='\n')
        syntax(tokens_and_table[1], tokens_and_table[0])
        print("Ошибки не обнаружены")
    except Exception as e:
        print(f"Получена ошибка. Код ошибки: {str(e)} ")

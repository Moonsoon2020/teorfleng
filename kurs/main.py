from lexer import lexer
from syntax import syntax

if __name__ == '__main__':
    try:
        for i, line in enumerate(open("kurs/prog.txt")):
            print(str(i)+":", line, end="")
        print()
        tokens_and_table = lexer('kurs/prog.txt')
        # print(*tokens_and_table, sep='\n')
        syntax(tokens_and_table[1], tokens_and_table[0])
        print("Ошибки не обнаружены")
    except Exception as e:
        print(f"Получена ошибка. Код ошибки: {str(e)} ")

op = {"(": 1, "+": 2, "-": 2, "*": 3, "/": 3}


def rpn(text):
    stack = []
    exit = ""
    flag = False
    for symbol in text:
        if not stack and symbol in "+-*/":
            flag = False
            stack.append(symbol)
        elif stack and symbol in "+-*/":
            flag = False
            if op[symbol] > op[stack[-1]]:
                stack.append(symbol)
            else:
                while op[symbol] <= op[stack[-1]]:
                    exit += stack.pop() + " "
                    if not stack:
                        break
                stack.append(symbol)
        elif symbol == "(":
            flag = False
            stack.append(symbol)
        elif symbol == ")":
            flag = False
            while stack[-1] != "(":
                exit += stack.pop() + " "
            stack.pop()
        else:
            if flag == True:
                exit = exit[:-1] + symbol + " "
            else:
                exit += symbol + " "
            flag = True
    while stack:
        exit += stack.pop() + " "
    return exit


def calcrpn(text):
    stack = []
    for symbol in text.split(" "):
        if not (symbol in op):
            stack.append(symbol)
        else:
            b = int(stack.pop())
            a = int(stack.pop())
            if symbol == "+":
                stack.append(a + b)
            elif symbol == "-":
                stack.append(a - b)
            elif symbol == "*":
                stack.append(a * b)
            elif symbol == "/":
                stack.append(a / b)
    stack.pop()
    return stack.pop()


print("1+4-4/2+(12*8)/6")
print("Обр. польск. нот.:", rpn("1+4-4/2+(12*8)/6"))
print(calcrpn(rpn("1+4-4/2+(12*8)/6")))

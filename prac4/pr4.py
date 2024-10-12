def main(info: str):
    bibl = {}
    quic = []
    new_bibl = {}
    operators = set()
    for line in info.splitlines():
        note1, operator, note2 = line.split()
        operators.add(operator)
        if note1 not in bibl:
            bibl[note1] = {operator: note2}
        elif operator not in bibl[note1]:
            bibl[note1][operator] = note2
        else:
            bibl[note1][operator] = ''.join(sorted(note2 + bibl[note1][operator]))
    first_key = sorted(bibl.keys())[0]
    new_bibl[first_key] = bibl[first_key]
    quic.extend(bibl[first_key].values())
    while len(quic) > 0:
        key = quic.pop(0)
        new_bibl[key] = {}
        keys = []
        for i in key:
            if i not in bibl:
                continue
            keys.extend(bibl[i].values())
            for j in bibl[i].values():
                if j not in new_bibl.keys():
                    quic.append(j)
        for element in keys:
            if element not in bibl:
                continue
            for operator in operators:
                if operator not in new_bibl[key].keys():
                    new_bibl[key][operator] = ""
                new_bibl[key][operator] += bibl[element][operator]
    print("\n".join(
        ["Поле " + str(key) + " связано с (ключ, узел) " + " ".join(map(str, new_bibl[key].items())) for key in
         new_bibl.keys()]))


import unittest


class Test(unittest.TestCase):
    def test(self):
        result = main("""0 a 1
        0 b 1
        1 b 2
        0 b 2
        1 a 1""")
        assert result == ""

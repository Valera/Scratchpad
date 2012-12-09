print("fact =", [x for x in [[1]] if (list(map(lambda elem: x.append(x[-1] * elem), range(2, int(input("n = ")) + 1))) or True)][0][-1])


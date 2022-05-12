def Row_dominance(tmp_minterm):
    tmp_minterm.sort(key = len)
    for i in range(len(tmp_minterm) - 1):
        count = 0
        row = i + 1
        pos = 0
        for j in range(len(tmp_minterm) - 1 - i):
            for k in range(len(tmp_minterm[i])):
                if tmp_minterm[i][pos] in tmp_minterm[row]:
                    count += 1
                    pos += 1

            if count == len(tmp_minterm[i]):
                del tmp_minterm[i][:]
                break

            row += 1
            pos = 0
            count = 0

    while 1:
        if [] in tmp_minterm:
            tmp_minterm.remove([])
            continue
        break

    print("Row_dominance :", tmp_minterm)
    return tmp_minterm    # row_dominance후에 남은 row들

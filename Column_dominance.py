def Column_dominance(tmp_minterm):
    check = []
    for i in range(len(tmp_minterm)):
        for j in tmp_minterm[i]:
            if j not in check:
                check.append(j)
    check.sort(key = int)
    col_minterm = [[0]*(len(tmp_minterm)+1) for row in range(len(check))]

    for i in range(len(check)):   #2차 배열의 시작에 check의 요소들을 적어준다.
        col_minterm[i][0] = check[i]

    for i in range(len(tmp_minterm)):       # 해당 minterm을 가지는 pi체크
        for j in range(len(tmp_minterm[i])):
            for k in check:
                if tmp_minterm[i][j] == k:
                    col_minterm[check.index(k)][i+1] = 1
                    break

    col_minterm.sort(key = lambda x : x.count(1))
    print(col_minterm)
    for i in range(len(col_minterm) - 1):
        if col_minterm[i] == []:
            continue
        compare_row = 1
        loop = True
        while (loop):
            count = 0
            if i+compare_row == len(col_minterm):
                break
            if col_minterm[i+compare_row] == []:
                compare_row += 1
                continue
            for j in range(len(col_minterm[i]) - 1):
                if ((col_minterm[i][j+1] == 1) and (col_minterm[i+compare_row][j+1] == 1)):
                    count += 1
                if count == col_minterm[i].count(1):
                    loop = False
                    del col_minterm[i+compare_row][:]
                    break
            compare_row += 1
            if i+compare_row == len(col_minterm):
                break
    while 1:
        if [] in col_minterm:
            col_minterm.remove([])
            continue
        break

    check.clear()   #배열 재사용
    for i in range(len(col_minterm[0])-1):  #배열에 남은 pi 갯수만큼 빈 배열 추가
        check.append([])

    for i in range(len(col_minterm)):   #col_minterm돌면서 1인 것을 check에 추가.
        for j in range(len(col_minterm[i])- 1):   #j는 pi의 번호
            if col_minterm[i][j+1] == 1:
                check[j].append(col_minterm[i][0])

    while 1:
        if [] in check:
            check.remove([])
            continue
        break

    print("Column_dominance :", check)

    return check   #Column_dominance 후에 정리된 minterm을 가진 pi


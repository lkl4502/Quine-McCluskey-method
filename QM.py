from string import ascii_uppercase

def Finding_minterm(result, binary):  # 재귀함수 구현
    tmp = binary.find('-')  # binary에 '-'가 있으면 해당 인덱스 반환
    if tmp == -1:  # binary에 '-'가 없으면 binary가 minterm이므로 바로 추가
        result.append(binary)
        return
    s1 = binary[:tmp] + '0' + binary[tmp + 1:]  # binary의 '-' 부분을 0으로 바꿈.
    s2 = binary[:tmp] + '1' + binary[tmp + 1:]  # binary의 '-' 부분을 1로 바꿈.
    if s1.find('-') == -1:  # s1에 더이상 '-'가 없으면 result에 append
        result.append(s1)
    else:  # '-'가 더 있다면 다시 한번 함수 호출
        Finding_minterm(result, s1)
    if s2.find('-') == -1:
        result.append(s2)
    else:
        Finding_minterm(result, s2)


def Finding_EPI(answer):
    EPI = []  # EPI가 들어갈 빈 배열 생성
    if len(answer) == 1:
        EPI.append(answer[0])
        return EPI

    result = [[] for row in range(len(answer))]  # pi 갯수에 맞게 2차원 배열 생성
    for i in range(len(answer)):
        Finding_minterm(result[i], answer[i])  # 각 pi에 해당하는 minterm 구하기.

    for i in range(len(result)):
        for j in range(len(result[i])):
            count = 0  # 다른 pi에서 cover하는 minterm인지 확인하는 변수
            if i == 0:
                compare_row = 1
            else:
                compare_row = 0
            compare_col = 0
            while (count == 0):  # count가 0 일때만 반복 count가 1이상이면 이미 cover됐다는 의미라서 더 이상의 반복 무의미
                if result[i][j] == result[compare_row][compare_col]:
                    count += 1
                else:
                    compare_col += 1  # 반복하면서 비교하는 과정에서 같지 않다면 col += 1
                    if compare_col == len(result[compare_row]):  # 비교하는 pi의 마지막 minterm을 끝내면 row += 1 col = 0
                        compare_row += 1
                        compare_col = 0
                    if compare_row == i:  # 만약 비교하는 pi의 row가 i와 같다면 row += 1
                        compare_row += 1
                    if compare_row == len(result):  # row가 result의 길이와 같으면 비교는 끝
                        break

            if count == 0:  # 반복이 끝났음에도 count 가 0이면 EPI이다.
                EPI.append(answer[i])
                break  # 해당 pi는 EPI임으로 다음 PI로 넘어간다.
    return EPI


def Finding_PI(input_count, array, answer):
    result = []
    zerolist = []
    for i in range(len(array)):  # combined 됐는지 확인하는 list
        zerolist.append([])
        for j in range(len(array[i])):
            zerolist[i].append(0)

    for i in range(len(array) - 1):  # 마지막 배열은 이미 전 단계에서 확인되기때문에 반보을 한 번 적게
        binary_set = []
        A_pos = B_pos = 0
        for j in range(len(array[i]) * len(array[i + 1])):
            # array[i]와 array[i+1]안에 있는 요소를 각각 매칭시켜야 하기 때문에 반복회수는 요소의 갯수를 서로 곱한 값
            if B_pos == len(array[i + 1]):  # 기준은 array[i]이기 때문에 B_pos다 돌면 A_pos + 1
                B_pos = 0
                A_pos += 1
            count = 0
            binary_tmp = array[i][A_pos]
            for k in range(input_count):  # input의 수는 bit수와 동일하다
                if array[i][A_pos][k] != array[i + 1][B_pos][k]:
                    count += 1
                    binary_tmp = array[i][A_pos][:k] + '2' + array[i][A_pos][k + 1:]  # 출력값 정렬을 위해 '2'
            if count == 1:  # count가 1이면 hamming distane가 1이라는 의미
                if binary_tmp in binary_set:  # 만약 이미 있다면 그냥 지나가고 combined만 올려줌
                    pass
                else:
                    binary_set.append(binary_tmp)  # 없으면 추가
                zerolist[i][A_pos] += 1
                zerolist[i + 1][B_pos] += 1
            B_pos += 1

        result.append([])
        result[i] = binary_set
    zero_count = 0
    zerolist_len = 0
    for i in range(len(zerolist)):  # combined되지 않은 것을 찾아 answer에 추가
        zerolist_len += len(zerolist[i])
        for j in range(len(zerolist[i])):
            if zerolist[i][j] == 0:
                zero_count += 1
                answer.append(array[i][j])
    if zero_count == zerolist_len:
        result = []
    return result

def Remove_EPI_minterm(EPI, answer):
    if "EPI" in answer:
        tmp = answer[:len(answer) - len(EPI)]
        del EPI[0]
        for i in tmp:
            for j in EPI:
                if i == j:
                    tmp.remove(i)
    else:
        tmp = answer

    tmp_minterm = [[] for row in range(len(tmp))]
    for i in range(len(tmp)):
        Finding_minterm(tmp_minterm[i], tmp[i])

    EPI_minterm = [[] for row in range(len(EPI))]
    for i in range(len(EPI)):
        Finding_minterm(EPI_minterm[i], EPI[i])

    for i in range(len(EPI_minterm)):
        for j in range(len(EPI_minterm[i])):
            for k in range(len(tmp_minterm)):
                for l in range(len(tmp_minterm[k])):
                    if EPI_minterm[i][j] == tmp_minterm[k][l]:
                        del tmp_minterm[k][l]
                        break
    while 1:
        if [] in tmp_minterm:
            tmp_minterm.remove([])
            continue
        break

    return tmp_minterm

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

def change_form(remove_minterm, input_count):
    result = []
    for i in range(len(remove_minterm)):
        if len(remove_minterm[i]) == 1:
            result.append(remove_minterm[i][0])
            continue
        s = remove_minterm[i][0]
        for j in range(len(remove_minterm[i])-1):
            for k in range(input_count):
                if remove_minterm[i][0][k] != remove_minterm[i][j+1][k]:
                    s = s[:k] + '-' + s[k+1:]
        result.append(s)
    return result

def optimization_form(input_count, EPI, second_EPI, remove_minterm):
    alphabet_list = list(ascii_uppercase)
    alphabet_list = alphabet_list[:input_count]
    result = []

    for t in EPI,second_EPI,remove_minterm:
        for i in range(len(t)):
            s = ''.join(alphabet_list)
            count = 0
            for j in range(len(s)):
                if (t[i][j] == '0'):
                    s = s[:j+count+1] + '\'' + s[j+count + 1:]
                    count += 1
                elif t[i][j] == '-':
                    s = s[:j + count] + s[j+count+1:]
                    count -= 1
            result.append(s)

    return result

def Petrick_method(remove_minterm):
    result = []
    for i in range(len(remove_minterm)):
        for j in range(len(remove_minterm[i])):
            for k in range(len(remove_minterm)-i-1):
                if remove_minterm[i][j] in remove_minterm[i+k+1]:
                    result.append(remove_minterm[i])
                    result.append(remove_minterm[i+k+1])
    return result

def solution(minterm):
    answer = []
    input_count = minterm[0]
    minterm_count = minterm[1]

    tmp = [[] for row in range(input_count + 1)]  # 초기 배열은 input_count + 1개 만큼 생성 빈 리스트 생성, 비트수 + 1

    for i in range(2, 2 + minterm_count):
        binary = str(format(minterm[i], 'b').rjust(input_count, '0'))  # minterm을 2진법으로 변환
        count = 0
        for j in range(len(binary)):
            if binary[j] == '1':  # 2진법으로 변환했을 때 들어가는 1의 갯수
                count += 1
        tmp[count].append(binary)  # 1의 갯수별로 리스트를 다르게

    while (tmp):
        tmp = Finding_PI(input_count, tmp, answer)

    answer.sort(key=int)  # key값으로 int를 줘서 크기로 인식하여 정렬, reverse는 default값으로 오름차순
    for i in range(len(answer)):
        for j in range(len(answer[i])):
            if answer[i][j] == '2':
                answer[i] = answer[i][:j] + '-' + answer[i][j + 1:]

    print("PI :", answer)  #PI 출력

    # EPI 구해서 answer에 더하고 출력
    EPI = Finding_EPI(answer)
    EPI.insert(0, "EPI")
    answer.extend(EPI)
    print("PI + EPI :", answer)

    remove_minterm = Remove_EPI_minterm(EPI, answer)
    if remove_minterm == []:
        result = optimization_form(input_count, EPI, [], [])
        print("F =", end=' ')
        for i in range(len(result) - 1):
            print("{} + ".format(result[i]), end='')
        print(result[-1])
        return result

    condition = True
    second_EPi_list = []
    while condition:   # EPI가 더 이상 없을때까지 반복
        remove_minterm = Column_dominance(remove_minterm)   #[minterm]끼리 묶어서 반환
        remove_minterm = Row_dominance(remove_minterm)  # row_dominance후에 남은 row
        tmp = change_form(remove_minterm, input_count)

        second_EPI = Finding_EPI(tmp)
        second_EPi_list.extend(second_EPI)
        print("second_EPI : {}".format(second_EPI))
        remove_minterm = change_form(remove_minterm, input_count)
        remove_minterm = Remove_EPI_minterm(second_EPI, remove_minterm)
        if (second_EPI == [] or remove_minterm == []): condition = False


    if (len(remove_minterm) == 0):
        result = optimization_form(input_count, EPI, second_EPi_list, remove_minterm)   #최적화 폼으로 변환
        print("F =", end=' ')
        for i in range(len(result) - 1):
            print("{} + ".format(result[i]), end='')
        print(result[-1])
    else:
        print("Petrick")
        remove_minterm = Petrick_method(remove_minterm)
        remove_minterm = change_form(remove_minterm, input_count)
        result = optimization_form(input_count, EPI, second_EPi_list, remove_minterm)

        print("F =", end=' ')
        for i in range(len(result) - len(remove_minterm)):
            print("{} + ".format(result[i]), end='')
        plus = 0
        for i in range(len(result)-len(remove_minterm), len(result)):
            if i+plus == len(result): break
            print("({} + {})".format(result[i+plus], result[i+1+plus]), end='')
            plus += 1
        return result

    return answer

# solution([4, 13, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
# solution([4, 11, 0, 2, 5, 6, 7, 8, 10, 12, 13, 14, 15])
# solution(([3, 6, 0, 1, 2, 5, 6, 7]))
# solution([4, 9, 1, 2, 3, 5, 7, 9, 10, 11, 13])
# solution([4, 11, 1, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15])
# solution([4, 9, 1, 2, 3, 7, 9, 10, 11, 13, 15])
# solution([4, 10, 0, 1, 2, 5, 6, 7, 8, 9, 10, 14])
# solution([4, 8, 1, 2, 3, 4, 5, 7, 9, 15])
# solution([4, 11, 0, 1, 2, 3, 5, 7, 8, 10, 12, 13, 15])
# solution([3, 5, 0, 1, 2, 5, 7])

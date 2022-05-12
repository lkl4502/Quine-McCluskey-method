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

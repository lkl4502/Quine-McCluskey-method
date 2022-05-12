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


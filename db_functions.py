from datetime import datetime
import link_functions
import pickle
import time

# 메인 db 이름 형식
# db_{학년 기수}.pkl (학년 기수를 나타내는 변수는 generation, gen)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 비활성화 여부} {int 삭제 여부} {int 추천수(미사용)} {int 비추천수(미사용)}
# 마지막 index는 [ {index}, 'not_a_video', ' ', {다음에 재생될 영상의 index}, 0, 1, 1, 0, 0 ]

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 비활성화 여부, 삭제 여부가 기록됨
#   비활성화할 경우 노래가 재생되지는 않지만 비활성화됐다는 사실을 알 수 있음
#   삭제할 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

def getData(gen : int, ban=False):
    """db에서 데이터 호출

    Args:
        gen (int): generation
        ban (bool, optional): is ban DB. Defaults to False.

    Returns:
        int:
            0: got data successfully
            1: got wrong data(not a list)
    """
    
    if ban:
        path = f"./db/ban_{gen}.pkl"
    else:
        path = f"./db/db_{gen}.pkl"
    
    with open(path, "rb") as fr:
        arr = pickle.load(fr)
    
    # db 데이터 받은거 return
    if type(arr) == list:
        return arr
    else: # 리스트가 아니면 초기화하고 return
        with open(path, "rb") as fr:
            if ban:
                pickle.dump(arr := [0], fr)
            else:
                pickle.dump(arr := [[0, 'not_a_video', ' ', 0, 0, 1, 1, 0, 0]], fr)
        
        return arr
    
def setData(gen : int, data : list, ban=False):
    """db 데이터 갱신
    
    Args:
        gen (int): generation
        data (anything): updated db data
        ban (bool, optional): is ban DB. Defaults to False.

    Returns:
        int: 0
    """
    
    # 경로 설정
    if ban:
        path = f"./db/ban_{gen}.pkl"
    else:
        path = f"./db/db_{gen}.pkl"
    
    # db 데이터 갱신
    with open(path, "rb") as fr:
        pickle.dump(data, fr)
    
    return 0

def setNextPlaylist(gen : int, i : int):
    """db_{gen}.pkl[-1][3] (다음에 재생할 영상의 index)를 i로 바꿈 

    Args:
        gen (int): generation
        i (int): playlist index number of video to play next
    """
    arr = getData(gen)
    arr[-1][3] = i
    setData(gen, arr)

def dbAppend(gen : int, code : str):
    """db에 영상 추가

    Args:
        gen (int): generation
        code (str): youtube video code

    Returns:
        int: 
            0: success
            1: runtime error
            2: duplicated
            3: banned
            4: timeout
    """
    
    try:
        arr = getData(gen)
        
        # 시간 검사
        lenth, title = link_functions.getLengthAndTitle(code)
        if lenth > 600: # 10분 넘어가는 영상 거름
            return 4
        
        # 차단 여부 검사
        if ban(code, isBan=False) == 2:
            return 3
        
        # 중복 검사
        st = arr[-1][3]
        ed = arr[-1][0]
        isDuplicated = False
        for i in range(st, ed):
            if arr[i][1] == code:
                isDuplicated = True
                break
            else:
                continue
        
        if isDuplicated:
            return 2
        
        # (검사를 통과하면) db에 추가
        ld = arr.pop()
        while arr[ld[0]][3] == 1:
            ld[0] += 1
        arr.append([len(arr), code, title, lenth, (time.time()//1), 0, 0])
        arr.append(ld)
        setData(gen, arr)
        
        return 0
    except:
        return 1
    
def ban(gen : int, code : str, isBan=True):
    """ban_{gen}.pkl에 유튜브 영상 코드 추가

    Args:
        gen (int): generation
        code (str): youtube video code
        b (bool, optional): actual ban or not. Defaults to True.

    Returns:
        int:
            0: success
            1: runtime error
            2: duplicated
    """
    
    try:
        # db 데이터 불러오기
        banTree = getData(gen, ban=True)
        
        # 중복검사
        l = len(banTree)
        if len(banTree) > 1:
            i = 1
            while True:
                if i >= l:
                    break
                elif banTree[i] == 0:
                    break
                elif banTree[i] == code: # 중복된 경우
                    return 2
                else:
                    i *= 2
                    if code > banTree[i]:
                        i += 1
                    continue
        else:
            banTree = [0, code]
            flag = False
        
        if isBan: # b=False이면 밴 안함
            for _ in range(l, i+1):
                banTree.append(0)
            banTree[i] = code

        return 0
    except:
        return 1

def deactivate(gen : int, i : int):
    """db_{gen}.pkl에서 i번 인덱스의 비활성화 여부를 1로 바꿈

    Args:
        gen (int): generation
        i (int): index number

    Returns:
        int:
            0: success
            1: runtime error
    """
    try:
        # db 데이터 불러오기
        arr = getData(gen)
        
        # db 데이터 바꾸기
        arr[i][5] = 1
        setData(gen, arr)
        
        return 0
    except:
        return 1

def delete(gen : int, i : int):
    """db_{gen}.pkl에서 i번 인덱스의 영상을 삭제 여부를 1로 바꿈

    Args:
        gen (int): generation
        i (int): index number

    Returns:
        int:
            0: success
            1: runtime error
    """
    try:
        # db 데이터 불러오기
        arr = getData(gen)
        
        # db 데이터 바꾸기
        arr[i][6] = 1
        setData(gen, arr)
        
        return 0
    except:
        return 1

if __name__ == "__main__":
    pass
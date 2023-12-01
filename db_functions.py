from datetime import datetime
import link_functions
import pickle
import time

# 메인 db 이름 형식
# db_{학년 기수}.pkl (학년 기수를 나타내는 변수는 generation, gen)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 다운로드 여부(deactivate)} {int 삭제 여부(deleted)} {int 추천수(미사용)} {int 비추천수(미사용)}

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 다운로드 여부, 삭제 여부가 기록됨
#   삭제할 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

def getData(gen : int, ban=False):
    """db 데이터 호출

    Args:
        gen (int): generation
        ban (bool, optional): is it ban_{gen}.pkl. Defaults to False.

    Returns:
        list: DB data
    """
    
    if ban:
        path = f"./db/ban_{gen}.pkl"
    else:
        path = f"./db/db_{gen}.pkl"
    
    try:
        with open(path, "rb") as fr:
            arr = pickle.load(fr)
    except:
        arr = 0
    
    # db 데이터 받은거 return
    if type(arr) == list:
        return arr
    else: # 리스트가 아니면 초기화하고 return
        with open(path, "wb") as fw:
            if ban:
                pickle.dump(arr := [0], fw)
            else:
                pickle.dump(arr := [[0, 'not_a_video', ' ', 0, 0, 1, 1, 0, 0]], fw)
        
        return arr

def getDataWithoutDeleted(gen : int):
    """db에서 삭제되지 않은 데이터 호출

    Args:
        gen (int): generation

    Returns:
        list: DB data without deleted index
    """

    arr = getData(gen)
    
    # db 데이터 받은거 arr[n][6](삭제 여부)=0인거만 newarr에 넣음
    newarr = []
    st = arr[-1][3]
    ed = arr[-1][0]
    for i in range(st, ed):
        if arr[i][6] == 0:
            newarr.append(arr[i])
        
    return newarr

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
    with open(path, "wb") as fw:
        pickle.dump(data, fw)
    
    return 0

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
        k = ban(gen, code, isBan=False)
        if k == 2:
            return 3
        elif k == 1: # ban 함수에서 오류 발생
            return 1
        
        # 중복 검사
        isDuplicated = False
        l = len(arr)
        for i in range(l):
            if (arr[i][1] == code) and (arr[i][5] == 0) and (arr[i][6] == 0):
                isDuplicated = True
                break
            else:
                continue
        
        if isDuplicated:
            return 2
        
        # (검사를 통과하면) db에 추가
        arr.append([len(arr), code, title, lenth, int(time.time()//1), 0, 0, 0, 0])
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
        banDict = getData(gen, ban=True)
        
        # 중복검사
        if code in banDict:
            return 2
        
        # db 업데이트
        if isBan:
            banDict[code] = 1
            setData(gen, banDict, ban=True)
        
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
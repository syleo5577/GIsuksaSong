from datetime import datetime
import link_functions
import pickle
import time

# 메인 db 이름 형식
# db_{학년 기수}.txt (학년 기수를 나타내는 변수는 generation, gen)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 비활성화 여부} {int 삭제 여부} {int 추천수(미사용)} {int 비추천수(미사용)}
# 마지막 index는 [ {index}, 'not_a_video', ' ', {마지막으로 재생된 영상의 index}, 0, 1, 1, 0, 0 ]

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 비활성화 여부, 삭제 여부가 기록됨
#   비활성화할 경우 노래가 재생되지는 않지만 비활성화됐다는 사실을 알 수 있음
#   삭제할 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

# 기타 사항:

def getData(gen, ban=False):
    """db에서 데이터 가져옴

    Args:
        gen (int): generation
        ban (bool, optional): is ban DB. Defaults to False.

    Returns:
        int: 0
    """
    
    if ban:
        path = f"./db/ban_{gen}.py"
    else:
        path = f"./db/db_{gen}.pkl"
    
    with open(path, "rb") as fr:
        arr : list = pickle.load(fr)
    
    if type(arr) == list:
        return arr
    else:
        with open(path, "rb") as fr:
            pickle.dump([], fr)
        return []
    
def updateData(gen, data, ban=False):
    """db에 데이터 갱신함

    Args:
        gen (int): generation
        data (anything): updated db data
        ban (bool, optional): is ban DB. Defaults to False.

    Returns:
        int: 0
    """
    
    if ban:
        path = f"./db/ban_{gen}.pkl"
    else:
        path = f"./db/db_{gen}.pkl"
    
    with open(path, "rb") as fr:
        pickle.dump(data, fr)
    
    return 0

def dbAppend(gen, code):
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
            return 3
        
        
        # 차단 여부 검사
        if ban(code, b=False) == 2:
            return 3
        
        # 나중에 여기에 중복 검사 추가 예정
        
        # (검사를 통과하면) db에 추가
        ld = arr.pop()
        ld[0] += 1
        arr.append([len(arr), code, title, lenth, (time.time()//1), 0, 0])
        arr.append(ld)
        updateData(gen, arr)
        
        return 0
    except:
        return 1

    
def ban(gen, code, b=True):
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
        banList = getData(gen, ban=True)
        
        # 중복검사
        for i in range(len(banList)):
            if banList[i] == code:
                return 2
        
        banList.append(code)
        if b: # b=True면 밴, False면 밴 안함
            updateData(gen, banList, ban=True)

        return 0
    except:
        return 1

def deactivate(gen, i):
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
        updateData(gen, arr)
        
        return 0
    except:
        return 1

def delete(gen, i):
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
        updateData(gen, arr)
        
        return 0
    except:
        return 1

if __name__ == "__main__":
    pass
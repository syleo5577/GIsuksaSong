from datetime import datetime
import link_functions
import pickle
import time

# 메인 db 이름 형식
# db_{학년 기수}.txt (학년 기수를 나타내는 변수는 generation, gen)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 비활성화 여부} {int 삭제 여부}

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 비활성화 여부, 삭제 여부가 기록됨
#   비활성화할 경우 노래가 재생되지는 않지만 비활성화됐다는 사실을 알 수 있음
#   삭제될 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

# 기타 사항:

def makeNewFile(path, p=True):
    """만약 path의 경로에 파일이 없으면 빈 리스트가 들어있는 pkl 파일 만듦, p=False면 빈 파일 만듦

    Args:
        path (str): 파일 경로
        p (bool): pickle 파일인지 아닌지 고름

    Returns:
        int: 0
    """
    try:
        f = open(path, "rb")
        f.close
    except FileExistsError: # 만약 db 파일이 없으면 새 파일 만듦
        if pickle:
            with open(path, "wb") as fw:
                pickle.dump([], fw)
        else:
            f = open(path, "w")
            f.close()
    
    return 0

def dbAppend(gen, code):
    """db에 영상 추가

    Args:
        gen (int): 기수(期數)
        code (str): 유튜브 영상 코드

    Returns:
        int: 0: 추가 성공, 1: 중복, 2: 시간 초과, 3: 차단됨, 4: 실패(오류)
    """
    
    try:
        path = f"./db/db_{gen}.pkl"
        makeNewFile(path)
        
        # db 데이터 불러오기
        with open(path,"rb") as fr:
            lst : list = pickle.load(fr)
        
        # 나중에 여기에 중복 검사 추가 예정
        
        # 시간 검사
        lenth, title = link_functions.getLengthAndTitle(code)
        if lenth > 600: # 10분 넘어가는 영상 거름
            return 2
        
        # 차단 여부 검사
        if ban(code, b=False) == 1:
            return 3
        
        # (검사를 통과하면) db에 추가
        lst.append([len(lst), code, title, lenth, (time.time()//1), 0, 0])
        return 0
        
    except:
        return 4

    
def ban(code, b=True):
    """banned_list.txt에 유튜브 코드 영상 추가

    Args:
        code (str): 유튜브 영상 코드
        b (bool): 실제 밴 여부(기본: True)

    Returns:
        int: 0이면 append 성공, 1이면 중복, 2면 실패(오류)
    """
    
    try:
        # db 데이터 불러오기
        with open("db/banned_list.txt", "r") as f:
            banList = f.readlines()
        
        # 중복검사
        for i in range(len(banList)):
            if banList[i].strip() == code:
                return 1
        
        if b: # b=True면 밴함, False면 밴 안함
            with open("db/banned_list.txt", "a") as f:
                f.write(code + "\n")

        return 0
    except:
        return 2

def delete(gen, i):
    """db_{gen}.pkl에서 i번 인덱스의 영상을 삭제 여부를 1로 바꿈

    Args:
        gen (int): 기수(期數)
        i (int): index number

    Returns:
        int: 0; 성공, 1: 실패(오류)
    """
    try:
        # db 데이터 불러오기
        path = f"./db/db_{gen}.pkl"
        makeNewFile(path)
        with open(path, "rb") as fr:
            lst : list = pickle.load(fr)
        
        # db 데이터 바꾸기
        lst[i][6] = 1
        
        return 0
    except:
        return 1

def deactivate(gen, i):
    """db_{gen}.pkl에서 i번 인덱스의 비활성화 여부를 1로 바꿈

    Args:
        gen (int): 기수(期數)
        i (int): index number

    Returns:
        _type_: 0: 성공, 1: 실패(오류)
    """
    try:
        # db 데이터 불러오기
        path = f"./db/db_{gen}.pkl"
        makeNewFile(path)
        with open(path, "rb") as fr:
            lst : list = pickle.load(fr)
        
        # db 데이터 바꾸기
        lst[i][5] = 1
        
        return 0
    except:
        return 1

def callData():
    pass

if __name__ == "__main__":
    pass
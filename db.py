from datetime import datetime
import link_functinos
import pickle
import time

# 메인 db 이름 형식
# db_{학년 기수}.pkl (학년 기수를 나타내는 변수는 generation)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 비활성화 여부} {int 삭제 여부}

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 비활성화 여부, 삭제 여부가 기록됨
#   비활성화할 경우 노래가 재생되지는 않지만 비활성화됐다는 사실을 알 수 있음
#   삭제될 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

# 기타 사항:

def dbAppend(code, generation):
    """db에 영상 추가

    Args:
        code (str): 유튜브 영상 코드
        generation (int): 기수(期數)

    Returns:
        int: 0: 추가 성공, 1: 중복, 2: 시간 초과, 3: 밴, 4: 실패(오류)
    """
    
    try:
        f = f"./db/db_{generation}.pkl"
        
        try:
            with open(f,"rb") as fr:
                lst : list = pickle.load(fr)
        except FileExistsError: # 만약 db 파일이 없으면 새 파일 만듦
            file = open(f, "w")
            file.close
            with open(f, "rb") as fr:
                lst : list = pickle.load(fr)
        
        # 나중에 여기에 중복 검사 추가 예정
        
        # 시간 검사
        lenth, title = link_functinos.getLengthAndTitle(code)
        if lenth > 600: # 10분 넘어가는 영상 거름
            return 2
        
        # 밴 여부 검사
        with open("./db/banned_list.pkl","rb") as fr:
            banList : list = pickle.loads(fr)
        for i in range(len(banList)):
            if banList[i] == code:
                return 3
        
        # (검사를 통과하면) db에 추가
        lst.append([len(lst), code, title, lenth, int(time.time()), 0, 0])
        return 0
        
    except:
        return 4

    
def ban(code):
    """banned_list.pkl에 유튜브 영상 추가

    Args:
        code (str): 유튜브 영상 코드

    Returns:
        int: 0이면 append 성공, 1이면 중복, 2면 실패(오류발생)
    """
    
    try:
        with open("./db/banned_list.pkl","rb") as fr:
            banList : list = pickle.loads(fr)
        
        for i in range(len(banList)):
            if banList[i] == code:
                return 1
        
        banList.append(code)
        
        with open("./db/banned_list.pkl", "wb") as fw:
            pickle.dump(banList, fw)

        return 0
    except:
        return 2

def delete(i):
    pass

def deactivate(i):
    pass

def callData():
    pass

if __name__ == "__main__":
    pass
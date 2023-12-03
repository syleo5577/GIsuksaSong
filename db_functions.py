import link_functions
import moviepy.editor as mp
import os
import pickle
from pytube import YouTube
import time

# 메인 db 이름 형식
# db_{학년 기수}.pkl (학년 기수를 나타내는 변수는 generation, gen)

# 메인 db 데이터 형식
# {index} {str 영상 코드} {str 영상 제목} {int 영상 길이} {int 등록 (유닉스) 시간} {int 다운로드 여부(deactivate)} {int 삭제 여부(deleted)} {int 추천수(미사용)} {int 비추천수(미사용)}

# 기본적인 기획:
#   db에는 영상 코드, 제목, 길이, 등록한 시간, 다운로드 여부, 삭제 여부가 기록됨
#   삭제할 경우 db에만 기록이 남으며 웹사이트에서는 확인할 수 없음

def getData(gen : int):
    """db 데이터 호출

    Args:
        gen (int): generation

    Returns:
        list: DB data
    """
    
    path = f"./db/db_{gen}.pkl"
    with open(path, "rb") as fr:
        arr : list[list] = pickle.load(fr)
    
    # db 데이터 받은거 return
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
    l = len(arr)
    for i in range(l):
        if arr[i][5] == 0 and arr[i][6] == 0:
            newarr.append(arr[i])
        
    return newarr

def setData(gen : int, data : list):
    """db 데이터 갱신
    
    Args:
        gen (int): generation
        data (anything): updated db data

    Returns:
        int: 0
    """
    
    # 경로 설정
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
        str: 작동 성공/실패 여부. 등록 성공시 영상 정보도 함께 보냄.
    """
    
    try:
        arr = getData(gen)
        
        # 시간 검사
        lenth, title = link_functions.getLengthAndTitle(code)
        if lenth > 600: # 10분 넘어가는 영상 거름
            return "timeout", 4
        
        # 차단 여부 검사
        with open(f"db/ban_{gen}.pkl", "rb") as fr:
            banDict = pickle.load(fr)
        if code in banDict:
            return "banned", 3
        
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
            return "duplicated", 2
        
        # (검사를 통과하면) db에 추가
        arr.append([len(arr), code, title, lenth, int(time.time()//1), 0, 0, 0, 0])
        setData(gen, arr)
        
        return "success", [len(arr), code, title, lenth, int(time.time()//1), 0, 0, 0, 0]
    except:
        return "runtime error", 1

def ban(gen : int, code : str):
    """ban_{gen}.pkl에 유튜브 영상 코드 추가

    Args:
        gen (int): generation
        code (str): youtube video code

    Returns:
        int:
            0: success
            1: runtime error
            2: duplicated
    """
    
    try:
        # db 데이터 불러오기
        path = f"db/ban_{gen}.pkl"
        with open(path, "rb") as fr:
            banDict = pickle.load(fr)
        
        # 중복검사
        if code in banDict:
            return 2
        
        # db 업데이트
        with open(path, "wb") as fw:
            pickle.dump(banDict, fw)
        
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

def downloadVideo(code : str):
    """유튜브의 code 영상 다운로드. 이미 있으면 다운로드 안함

    Args:
        gen (int): generation
        index (int): index number of video to download

    Returns:
        str: dir path of downloaded file, if fail return 'error'
    """
    
    try:
        # 파일 존재 여부 확인
        mp4_file = f"db/videos/{code}.mp4"
        mp3_file = f"db/audio/{code}.mp3"
        if os.path.isfile(mp3_file):
            return mp3_file
    
        # 유튜브 영상 다운로드
        url = f"https://youtube.com/watch?v={code}"
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path=f'db/video', filename=code)

        # 다운로드한 영상을 mp3로 변환
        clip = mp.AudioFileClip(mp4_file)
        clip.write_audiofile(mp3_file)

        # 변환 후 mp4 파일 삭제
        clip.close()
        os.remove(mp4_file)
        
        return mp3_file
    except:
        return "runtime error"

def deleteVideo(gen : int, index : int):
    """**DO NOT USE**
    db/videos에서 파일 지움. index는 db_gen.pkl에서의 인덱스

    Args:
        gen (int): generation
        index (int): index number of video to delete

    Returns:
        int:
            0: success
            1: runtime error
    """
    
    try:
        arr = getData(gen)
        title = arr[index][2]
        path = f"db/videos/{title}.mp3"
        
        os.remove(path)
        
        return 0
    except:
        return 1

if __name__ == "__main__":
    # setData(0, [[0, 'gX9m-rCtSqc', '【Lyric Video】結束バンド「忘れてやらない」／ TVアニメ「ぼっち・ざ・ろっく！」第12話劇中曲', 218, 1198508400, 0, 0, 0, 0]])
    arr = getData(0)
    print(arr)
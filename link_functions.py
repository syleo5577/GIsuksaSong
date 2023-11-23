from googleapiclient.discovery import build
import re

def addHTTPS(url : str):
    """입력받은 문자열에 https:// 없으면 넣어줌

    Args:
        url (str): 입력받은 문자열

    Returns:
        str, 'https://'가 추가된 URL
    """
    
    https = re.compile("https{0, 1}://")
    
    if not https.match(url):
        return "https://" + url
    else:
        return url

def getYouTubeVideoID(url : str):
    """입력받은 URL이 'https://www.youtube.com/watch?v='로 시작하는지 확인 + 글자수 확인
    즉, 유튜브 영상의 링크를 입력으로 받아야 1 출력
    (예: https://www.youtube.com을 입력받으면 0 출력) 
    ! 이 함수는 입력받은 문자열이 URL인지 아닌지 검사하지 않음
    
    Args:
        url (str): 검사할 문자열

    Returns:
        int: 유튜브 영상이면 유튜브 영상 코드, 아니면 None을 리턴
    """
    
    ytRegex = re.compile(r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(shorts/|watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    if regexMatch := ytRegex.match(url):
        return regexMatch.group(6)
    else:
        return None

def getLengthAndTitle(code : str):
    """유튜브 영상 코드 넣으면 영상 시간, 제목 반환함

    Args:
        code (str): 유튜브 영상 코드

    Returns:
        int, str: 영상 길이, 영상 제목
    """
    
    f = open("./youtubeAPIkey.txt", "r")
    api_key = f.readline().strip()
    f.close()   
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    response1 = youtube.videos().list(
        part='contentDetails', 
        id=code
    ).execute()
    response2 = youtube.videos().list(
        part='snippet',
        id=code
    ).execute()
    
    length = response1['items'][0]['contentDetails']['duration']
    title = response2['items'][0]['snippet']['title']

    return strTimeToInt(length), title

def strTimeToInt(length : int):
    """유튜브 API에서 받은 시간 형식(PT{hh}H{mm}M{ss}S)을 초단위로 바꿔줌

    Args:
        length (str): 유튜브 영상의 길이(유튜브 API가 출력하는 형식)

    Returns:
        int: 영상의 길이
    """
    
    i = len(length) - 2
    j = i + 1
    cnt = 0
    time = 0
    while i > 0:
        if not ('0' <= length[i] <= '9'):
            time += int(length[i+1:j]) * (60 ** (0 if length[j] == "S" else (1 if length[j] == "M" else 2))) 
            cnt += 1
            j = i
        i -= 1
    
    return time

if __name__ == "__main__":
    url = addHTTPS(input())
    code = getYouTubeVideoID(url)
    if code:
        print("code:", code)
        print(getLengthAndTitle(code))
    else:
        print("NOT YOUTUBE VIDEO")
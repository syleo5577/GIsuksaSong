import os
import re
from googleapiclient.discovery import build

def add_https(url : str):
    """입력받은 문자열에 https:// 없으면 넣어줌

    Args:
        url (str): 입력받은 문자열

    Returns:
        str, 'https://'가 추가된 URL
    """
    
    https = re.compile("https{0,1}://")
    
    if not https.match(url):
        return "https://" + url
    else:
        return url

def get_youtube_video_id(url : str):
    """입력받은 URL에서 유튜브 영상 코드 추출
    
    Args:
        url (str): 검사할 문자열

    Returns:
        str | None: 유튜브 영상이면 유튜브 영상 코드, 아니면 None을 리턴
    """
    
    yt_regex = re.compile(r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(shorts/|watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    if regex_match := yt_regex.match(url):
        return regex_match.group(6)
    else:
        return None

def get_length_and_title(code : str):
    """유튜브 영상 코드 넣으면 영상 시간, 제목 반환함

    Args:
        code (str): 유튜브 영상 코드

    Returns:
        int, str: 영상 길이, 영상 제목
    """
    
    api_key = os.environ.get('YOUTUBE_API_KEY')
    
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

    return str_time_to_int(length), title

def str_time_to_int(length : int):
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
    url = add_https(input())
    code = get_youtube_video_id(url)
    if code:
        print("code:", code)
        print(get_length_and_title(code))
    else:
        print("NOT YOUTUBE VIDEO")
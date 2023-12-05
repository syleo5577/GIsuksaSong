let currentURL = new URL(window.location.href);
let searchParams = new URLSearchParams(currentURL.search);
let generation = searchParams.get("gen");

var playlistLength = 0;

/**
 * 플레이리스트 채우는 함수.
 * @param {string} lowerText 윗부분 텍스트(영상 제목)
 * @param {string} upperText 아랫부분 텍스트(영상 등록 일시)
 * @param {string} code 영상 코드
 * @param {int} indexInDB db에서의 인덱스
 * @param {int} [isStrikthrough=0] 취소선 여부
 */
async function playlistAppend(upperText, lowerText, code, indexInDB, isStrikthrough=0) {

    //make item to append

    // itemContainer
    let itemContainer = document.createElement('div');
    itemContainer.classList.add('playlist-item');
    itemContainer.classList.add('item-flex-container');
    
    
    
    // thumbnailContainer
    let thumbnailContainer = document.createElement('div');
    thumbnailContainer.classList.add('thumbnail-container');
    
    // thumbnail
    let thumbnail = new Image();
    thumbnail.src = `https://i.ytimg.com/vi/${code}/default.jpg`; // 썸네일 이미지 링크
    thumbnailContainer.appendChild(thumbnail);
    

    // textContainer
    let textContainer = document.createElement('div');
    textContainer.classList.add('text-container');
    
    // upperTexteliment
    let upperTextElement = document.createElement('p');
    upperTextElement.classList.add('upper-text-eliment');
    upperTextElement.appendChild(document.createTextNode(upperText));
    if (isStrikthrough == 1) {
        upperTextElement.style.textDecoration = 'line-through';
    }
    textContainer.appendChild(upperTextElement);

    // lowerTexteliment
    let lowerTextElement = document.createElement('p');
    lowerTextElement.classList.add('lower-text-eliment');
    lowerTextElement.appendChild(document.createTextNode(lowerText));
    textContainer.appendChild(lowerTextElement);
    
    
    // buttonContainer
    let buttonsContainer = document.createElement('div');
    buttonsContainer.classList.add('buttons-container');
    
    // buttonsUl
    let buttonsUl = document.createElement('ul');
    buttonsUl.classList.add('buttons-ul');

    // buttonsLi
    let buttonsLi = document.createElement('li');
    buttonsLi.classList.add('buttons-li');

    // buttons
    // let nameOfTextNodes = ['다운로드', '비활성화', '삭제', '차단'];
    // let nameOfCssClassAndId = ['download', 'deactivate', 'delete', 'ban'];
    let nameOfTextNodes = ['다운로드', '삭제', '차단'];
    let kindOfButton = ['download', 'delete', 'ban'];
    for (var i = 0; i < 3; i++){
        let button = document.createElement('button');
        button.classList.add('round-button');
        button.classList.add('button-' + kindOfButton[i]);
        button.id = 'button.' + kindOfButton[i] + '.' + playlistLength + '.' + indexInDB + '.' + code;
        button.appendChild(document.createTextNode(nameOfTextNodes[i]));

        button.addEventListener('click', async function() {
            buttonsInteraction(this.id);
        });

        buttonsLi.appendChild(button);
        buttonsUl.appendChild(buttonsLi);
    }

    buttonsContainer.appendChild(buttonsUl);
    
    
    // 총합
    itemContainer.appendChild(thumbnailContainer);
    itemContainer.appendChild(textContainer);
    itemContainer.appendChild(buttonsContainer);
    
    let liEliment = document.createElement('li');
    liEliment.appendChild(itemContainer);

    let playlist = document.getElementById('playlist');
    playlist.appendChild(liEliment);
    
    return 0;
}

/**
 * 
 * @returns gotten data or 'error'
 */
async function getData() {
    try {
        let response = await fetch(`/list/data?gen=${generation}`, { method: 'GET' });
        let data = await response.json();
        // console.log(playlistArr);
        return data.arr;
    } catch (error) {
        console.error('Error:', error);
        return 'error'
    }

}

/**
 * 유튜브 영상 mp3 다운로드
 * @param {str} buttonId 클릭한 버튼의 Id
 * @returns 성공/실패 여부
 */
async function getVideo(buttonId) {
    let button = document.getElementById(buttonId);
    button.innerHTML = '다운로드 중...';
    button.style.backgroundColor = 'gray';
    try {
        let kindOfButton, indexInJS, indexInDB, code;
        [dummy, kindOfButton, indexInJS, indexInDB, code] = buttonId.split('.');

        let response = await fetch(`/list/download?gen=${generation}&index=${indexInDB}&code=${code}`, { method: 'GET' });
        console.log(response);

        if (!response.ok) {
            console.error('Server response was not ok.', response);
            return 'server error';
        }
        
        
        let blob = await response.blob();
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = code + '.mp3';
        a.click();

        if (response.headers.get('result') == 'success') {
            async function changePtagStyle() {
                let playlist = document.getElementById('playlist');
                pElement = playlist.children[indexInJS].children[0].children[1].children[0];
                pElement.style.textDecoration = 'line-through';
            }

            await changePtagStyle();
        }


        async function changeStyle() {
            button.innerHTML = '다운로드';
            button.style.backgroundColor = '#4CAF50';
        }

        await changeStyle();

        return 'success';
    } catch (error) {
        console.error('Error:', error);
        
        async function changeStyle() {
            button.innerHTML = '다운로드';
            button.style.backgroundColor = '#4CAF50';
        }
        
        await changeStyle();
        
        return 'catch error';
    }
    
}

/**
 * 영상을 db/프론트에서 지우기
 * @param {str} buttonId 클릭한 버튼의 Id
 * @returns 성공/실패 여부
 */
async function deleteItem(buttonId) {
    
    try {
        let kindOfButton, indexInJS, indexInDB, code;
        [dummy, kindOfButton, indexInJS, indexInDB, code] = buttonId.split('.');
        // console.log(buttonId);
        let response = await fetch(`/list/delete?gen=${generation}&index=${indexInDB}&code=${code}`, { method: 'GET' });
        
        if  (!response.ok) {
            console.error('Server response was not ok.', response);
            return 'server error';
        }
        
        let data = await response.json();
        
        if (data.result == 'success') {
            let playlist = document.getElementById('playlist');
            let divElement = document.createElement('div');
            playlist.replaceChild(divElement, playlist.children[indexInJS]);
        }

        return data.result;
    } catch (error) {
        console.error('Error:', error);
        return 'catch error';
    }
}

/**
 * 영상을 db/프론트에서 삭제하고 차단하기
 * @param {str} buttonId 클릭한 버튼의 Id
 * @returns 성공/실패 여부
 */
async function banItem(buttonId) {
    let kindOfButton, indexInJS, indexInDB, code;
    [dummy, kindOfButton, indexInJS, indexInDB, code] = buttonId.split('.');
    console.log(buttonId);

    try {
        let response = await fetch(`/list/ban?gen=${generation}&index=${indexInDB}&code=${code}`, { method: 'GET' });
        
        if  (!response.ok) {
            console.error('Server response was not ok.', response);
            
            return 'server error';
        }
        
        let data = await response.json();
        
        if (data.result == 'success') {
            let playlist = document.getElementById('playlist');
            let divElement = document.createElement('div');
            playlist.replaceChild(divElement, playlist.children[indexInJS]);
        }

        return data.result;
    } catch (error) {
        console.error('Error:', error);
        return 'catch error';
    }
}

/**
 * input에 입력한 링크 서버로 보냄
 * @param {Event} e 
 * @returns json 또는 'error'
 */
async function postLink(e) {
    let inputValue = document.getElementById('linkInput').value;
    if (e.keyCode == 13){
        e.preventDefault();
        
        try {
            const response = await fetch(`/list?gen=${generation}`, {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: inputValue})
            });
    
            if (!response.ok) {
                console.error('Server response was not ok.', response);
            
                return 'server error';
            }
    
            const jsonData = await response.json();
            console.log(jsonData);


            res = jsonData.result;
            if (jsonData.result == 'success') {
                window.alert('정상적으로 등록되었습니다.');
                playlistAppend(jsonData.title, Unix_timestamp(jsonData.unixtime), jsonData.code, jsonData.index);

                let input = document.querySelector('#linkInput');
                input.value = '';
            } else if (res == 'timeout') {
                window.alert('영상이 너무 깁니다.')
            } else if (res == 'banned') {
                window.alert('차단된 동영상입니다.')
            } else if (res == 'duplicated') {
                window.alert('이미 등록된 동영상입니다.')
            } else if (res == 'not video') {
                window.alert('유튜브 동영상 링크가 아닙니다.')
            } else if (res == 'runtime error'){
                window.alert('런타임 에러')
            } else {
                window.alert('오류가 발생했습니다. (뭔가 비정상적인 일이 발생함)')
            }

            return jsonData;
        } catch (error) {
            console.error('Error:', error);
            return 'catch error';
        }
    }
}


/**
 * 유닉스 시간을 사람이 알아볼 수 있게 바꿔줌
 * @param {float | int} t 
 * @returns yyyy-mm-dd hh:mm:ss
 */
function Unix_timestamp(t){
    const date = new Date(t*1000);

    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();

    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")} ${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

/**
 * 최초 로드시 리스트 채우기
 * @returns 0
 */
async function fillList() {
    let playlistArr = await getData();
    let playlistArrLength = playlistArr.length;

    for (let i = 0; i < playlistArrLength; i++) {
        let index = playlistArr[i][0];
        let code = playlistArr[i][1];
        let title = playlistArr[i][2];
        let uploadTime = playlistArr[i][4];
        let isDeactivated = playlistArr[i][5];
        playlistAppend(title, Unix_timestamp(uploadTime), code, index, isStrikthrough=isDeactivated);
        playlistLength++;
    }

    return 0
}

/**
 * 버튼 눌렀을 때 호출하는 함수
 * @param {str} thisId 클릭한 버튼의 Id
 * @returns 0
 */
async function buttonsInteraction(thisId) {
    let kindOfButton, indexInDB, code;
    [dummy, kindOfButton, indexInJS, indexInDB, code] = thisId.split('.');

    if (kindOfButton == 'download') {
        var res = await getVideo(thisId);
    } else if (kindOfButton == 'delete') {
        var res = await deleteItem(thisId);
    } else if (kindOfButton == 'ban') {
        var res = await banItem(thisId);
    } else {
        window.alert("오류발생");
    }

    window.alert(res);

    return 0;
}

document.addEventListener('DOMContentLoaded', async function () {
    playlistLength = 0;
    fillList();
});
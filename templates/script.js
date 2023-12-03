let currentURL = new URL(window.location.href);
let searchParams = new URLSearchParams(currentURL.search);
let generation = searchParams.get("gen");



/**
 * 플레이리스트 채우는 함수. int는 db에서의 인덱스 말하는거임.
 * @param {string} lowerText 
 * @param {string} upperText 
 * @param {string} imageUrl 
 * @param {int} index 
 */
function addItemToList(upperText, lowerText, imageUrl, index) {
    // itemContainer
    let itemContainer = document.createElement('div');
    itemContainer.classList.add('playlist-item');
    itemContainer.classList.add('item-flex-container');
    
    
    
    // thumbnailContainer
    let thumbnailContainer = document.createElement('div');
    thumbnailContainer.classList.add('thumbnail-container');
    
    // thumbnail
    let thumbnail = new Image();
    thumbnail.src = imageUrl; // 이미지 경로를 실제 이미지 경로로 대체
    thumbnailContainer.appendChild(thumbnail);
    

    // textContainer
    let textContainer = document.createElement('div');
    textContainer.classList.add('text-container');
    
    // upperTexteliment
    let upperTextElement = document.createElement('p');
    upperTextElement.classList.add('upper-text-eliment');
    upperTextElement.appendChild(document.createTextNode(upperText));
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
    textNodeArr = ['좋아요', '싫어요', 3, 4];
    for (var i = 0; i < 2; i++){
        let button = document.createElement('button');
        button.classList.add('round-button');
        button.classList.add('button' + (i+1));
        button.id = 'button' + (i+1) + '-' + index;
        button.appendChild(document.createTextNode(textNodeArr[i]));

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
 * @returns array[array[int, str, str, int * 6]]
 */
async function getData() {
    let playlistArr;

    try {
        let response = await fetch(`/list/data?gen=${generation}`, { method: 'GET' });
        let data = await response.json();
        playlistArr = data.arr;
    } catch (error) {
        console.error('Error:', error);
    }

    console.log(playlistArr);
    return playlistArr;
}

async function postLink(e) {
    let input = document.getElementById('linkInput');
    let inputValue = input.value;
    if (e.keyCode == 13){
        e.preventDefault();
        
        try {
            const response = await fetch('/list?gen=0', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: inputValue})
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const jsonData = await response.json();
            console.log(jsonData);

            input = null;
            fillList
            
            return jsonData;
        } catch (error) {
            console.error('Error:', error);
        }
    }
}


/**
 * 
 * @param {float | int} t 
 * @returns yyyy-mm-
 */
function Unix_timestamp(t){
    const date = new Date(t*1000);

    // 원하는 날짜 및 시간 형식으로 변환하기
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();

    return `${year}-${String(month).padStart(2, "0")}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * 
 * @returns 0
 */
async function fillList(){
    let playlistArr = await getData();
    let playlistLength = playlistArr.length;
    for (let i = 0; i < playlistLength; i++) {
        let index, code, title, videoLength, uploadTime, isDeactivated, isDeleted, likes, dislikes;
        [index, code, title, videoLength, uploadTime, isDeactivated, isDeleted, likes, dislikes] = playlistArr[i];
        addItemToList(title, Unix_timestamp(uploadTime), `https://i.ytimg.com/vi/${code}/hq720.jpg`, index);
    }

    return 0
}

document.addEventListener('DOMContentLoaded', async function () {
    fillList();
});
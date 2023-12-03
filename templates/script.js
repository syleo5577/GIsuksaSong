let currentURL = new URL(window.location.href);
let searchParams = new URLSearchParams(currentURL.search);
let generation = searchParams.get("gen");



/**
 * 플레이리스트 채우는 함수. int는 
 * @param {string} lowerText 윗부분 텍스트(영상 제목)
 * @param {string} upperText 아랫부분 텍스트(영상 등록 일시)
 * @param {string} code 영상 코드
 * @param {int} index db에서의 인덱스
 * @param {int} [isStrikthrough=false] 취소선 여부
 */
function addItemToList(upperText, lowerText, code, index, isStrikthrough=0) {
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
    if (isStrikthrough == 1) {
        lowerTextElement.style.textDecoration = 'line-through';
    }
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
    let nameOfCssClassAndId = ['download', 'delete', 'ban'];
    for (var i = 0; i < 3; i++){
        let button = document.createElement('button');
        button.classList.add('round-button');
        button.classList.add('button-' + nameOfCssClassAndId[i]);
        button.id = 'button.' + nameOfCssClassAndId[i] + '.' + index + '.' + code;
        button.appendChild(document.createTextNode(nameOfTextNodes[i]));

        button.addEventListener('click', function() {
            // console.log(this.id + ' 클릭됨');
            var dummy;
            let kindOfButton, dbIndexOfButton, codeOfButton;
            [dummy, kindOfButton, dbIndexOfButton, codeOfButton] = this.id.split('.');

            if (kindOfButton == 'download') {
                var res = getVideo(dbIndexOfButton, codeOfButton);
                if (res == 1) {
                    window.alert('다운로드 실패')
                }
            // } else if (kindOfButton == 'deactivate') {
            //     var res = deactivateItem(dbIndexOfButton);
            //     if (res == 1) {
            //         window.alert('비활성화 실패')
            //     }
            } else if (kindOfButton == 'delete') {
                var res = deleteItem(dbIndexOfButton);
                if (res == 1) {
                    window.alert('삭제 실패')
                }
            } else if (kindOfButton == 'ban') {
                var res = banItem(dbIndexOfButton, codeOfButton);
                if (res == 1) {
                    window.alert('차단 실패')
                }
                if (res == 2) {
                    window.alert('이미 차단되었습니다')
                }
            } else {
                window.alert("오류발생")
            }
            
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

async function getVideo(index, code) {
    try {
        let response = await fetch(`/list/download?gen=${generation}&index=${index}&code=${code}`, { method: 'GET' });

        if (!response.ok) {
            console.error('Server response was not ok.', response);

            return 1;
        }

        let blob = await response.blob();
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = code + '.mp3';
        a.click()
    } catch (error) {
        console.error('Error:', error);

        return 1;
    }

    return 0;
}

async function deactivateItem(index) {
    try {
        let response = await fetch(`/list/deactivate?gen=${generation}&index=${index}`, { method: 'GET' });
        
        if (!response.ok) {
            console.error('Server response was not ok.', response);
            return 1;
        }

        let data = await response.json();

        if (data.result == 'success') {
            return 0;
        } else {
            return 1;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteItem(index) {
    try {
        let response = await fetch(`/list/delete?gen=${generation}&index=${index}`, { method: 'GET' });
        // console.log(response);

        if (!response.ok) {
            console.error('Server response was not ok.', response);

            return 1;
        }

        let data = await response.json();

        if (data.result == 'success') {
            return 0;
        } else {
            return 1;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function banItem(index, code) {
    var res = deleteItem(index);
    if (res == 1) {
        return 1;
    }

    let response;
    try {
        response = await fetch(`/list/ban?gen=${generation}&index=${index}&code=${code}`, { method: 'GET' });
        
        if  (!response.ok) {
            console.error('Server response was not ok.', response);
            
            return 1;
        }
        
        let data = await response.json();

        if (data.result == 'success') {
            return 0;
        } else if (data.result == 'duplicated') {
            return 2;
        } else {
            return 1;
        }
    } catch (error) {
        console.error('Error:', error);

        return 1;
    }
}

/**
 * input에 입력한 링크 서버로 보냄
 * @param {Event} e 
 * @returns json
 */
async function postLink(e) {
    let inputValue = document.getElementById('linkInput').value;
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

            let result = jsonData.result;
            if (result = "success") {
                window.alert("정상적으로 등록되었습니다.");
                addItemToList(jsonData.title, Unix_timestamp(jsonData.unixtime), jsonData.code, jsonData.index)

                let input = document.querySelector('#linkInput');
                input.value = '';
            }

            
            return jsonData;
        } catch (error) {
            console.error('Error:', error);
        }
    }
}


/**
 * 유닉스 시간 바꿔줌
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
 * 리스트 채우기
 * @returns 0
 */
async function fillList() {
    let playlistArr = await getData();
    let playlistLength = playlistArr.length;

    for (let i = 0; i < playlistLength; i++) {
        let index, code, title, videoLength, uploadTime, isDeactivated, isDeleted, likes, dislikes;
        [index, code, title, videoLength, uploadTime, isDeactivated, isDeleted, likes, dislikes] = playlistArr[i];
        addItemToList(title, Unix_timestamp(uploadTime), code, index, isStrikthrough=isDeactivated);
    }

    return 0
}

async function resetList() {
    let ulElement = document.querySelector('#playlist');
    ulElement.innerHTML = '';

    return 0;
}

document.addEventListener('DOMContentLoaded', async function () {
    fillList();
});
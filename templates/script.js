let player;
let currentSongIndex = 0;
let isAdmin = false;


function onYouTubeIframeAPIReady() {
    player = new YT.Player('videoPlayer', {
        height: '315',
        width: '560',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
        playNextSong();
    }
}

function getVideoTitle(videoId, callback) {
    const apiKey = 'YOUR_API_KEY'; // Replace with your own API key
    const apiUrl = `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&key=${apiKey}&part=snippet`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data && data.items && data.items.length > 0) {
                const title = data.items[0].snippet.title;
                callback(title);
            } else {
                callback('Unknown Title');
            }
        })
        .catch(error => console.error('Error:', error));
}

let playlist = [];

function addSong() {
    const youtubeLink = document.getElementById('youtubeLink').value;
    const videoId = getVideoIdFromLink(youtubeLink);
    if (videoId) {
        getVideoTitle(videoId, (title) => {
            playlist.push({ videoId, title });
            document.getElementById('youtubeLink').value = '';
            
            if (playlist.length === 1) { 
                currentSongIndex = 0;     
                playNextSong();           
            }

            displayPlaylist();
        });
    }
}




function displayPlaylist() {
    const playlistContainer = document.getElementById('playlist');
    playlistContainer.innerHTML = '';

    playlist.forEach((song, index) => {
        const li = document.createElement('li');
        
        const img = document.createElement('img');
        img.src = `https://img.youtube.com/vi/${song.videoId}/default.jpg`; // Get the thumbnail image URL
        img.alt = `Thumbnail for Music No.${index + 1}`;
        img.classList.add('thumbnail');
        li.appendChild(img);
        
        const musicInfo = document.createElement('div');
        musicInfo.classList.add('music-info');
        
        const span = document.createElement('span');
        span.textContent = `Music No.${index + 1}`; // Display music name as "Music No.X"
        musicInfo.appendChild(span);
        
        const buttonsContainer = document.createElement('div');
        buttonsContainer.classList.add('buttons-container'); // Add class for styling
        
        // Add "Play" button
        const playButton = document.createElement('button');
        playButton.className = 'play-button';
        playButton.textContent = 'Play';
        playButton.onclick = () => playSong(index);
        buttonsContainer.appendChild(playButton);
        
        // Add "Delete" button
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-button';
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteSong(index);
        buttonsContainer.appendChild(deleteButton);
        
        musicInfo.appendChild(buttonsContainer);
        
        li.appendChild(musicInfo);

        playlistContainer.appendChild(li);
    });
}

// ... (The rest of your existing code)



function playNextSong() {
    const videoPlayerContainer = document.getElementById('videoPlayer');
    if (currentSongIndex < playlist.length) { 
        const videoId = playlist[currentSongIndex].videoId;
        player.loadVideoById({ videoId, suggestedQuality: 'large', loop: false });
        player.playVideo();
        currentSongIndex++; 
        displayPlaylist();
    } else if(playlist.length > 0){
        currentSongIndex=0;
        playNextSong();
    } else{
        videoPlayerContainer.innerHTML='';
    }
}

function playSong(index) {
    const videoPlayerContainer = document.getElementById('videoPlayer');
    const videoId = playlist[index].videoId;
    player.loadVideoById({ videoId, suggestedQuality: 'large', loop: false });
    player.playVideo();
    displayPlaylist();
}

function deleteSong(index) {
    const videoPlayerContainer = document.getElementById('videoPlayer');
    const videoElement = videoPlayerContainer.querySelector('iframe');
    if (videoElement) {
        videoElement.remove(); 
        player.stopVideo(); 
    }
    playlist.splice(index, 1);
    displayPlaylist();
}

function deleteBatch() {
    const videoPlayerContainer = document.getElementById('videoPlayer');
    const videoElement = videoPlayerContainer.querySelector('iframe');
    if (videoElement) {
        videoElement.remove(); 
        player.stopVideo(); 
    }
    playlist = [];
    displayPlaylist();
}






if (evnet.keyCode == 13) {
    document.getElementById('input').addEventListener('submit', function(e) {
        e.preventDefault(); // 폼의 기본 제출 동작을 방지합니다.
    
        var inputValue = document.getElementById('myInput').value; // 입력 값을 가져옵니다.
    
        // 여기에서 서버로 데이터를 전송하는 코드를 작성합니다.
        fetch('/main', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({url: inputValue}),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => console.error('Error:', error));
    });
}
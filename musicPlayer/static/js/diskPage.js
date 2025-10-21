let current = 0;
let playing = false;
let mysound;
let source;
let progressBar;
let onProgChange = false;
let musics = [];



function set_ListOfMusics(mlist) {
  musics = mlist;
}

function startMusic() {
  console.log("funcionando");
console.log("musics:", musics);
console.log("current:", current);

  mysound = document.getElementById('myplay');
  source = document.getElementById('audioSource');
  progressBar = document.getElementById('rangeProgr');
  const soundImg = document.getElementById('coverImg');

  source.src = musics[0].fileUrl;
  soundImg.src = musics[0].coverURL;
  mysound.load();
  mysound.play();
  playing = true;

  changeColorMusic();
  changeArtistTitle();
  updateTime();

  mysound.addEventListener('ended', () => {
    if (current < musics.length - 1) {
      current++;
      source.src = musics[current].fileUrl;
      document.getElementById('coverImg').src = musics[current].coverURL;
      mysound.load();
      mysound.play();
    }

    changeColorMusic();
    changeArtistTitle();
    updateTime();

    if (current === musics.length - 1) {
      const mylink = document.getElementById("lim_" + current.toString());
      if (mylink) mylink.style.color = "blue";
    }
  });

  mysound.addEventListener('timeupdate', () => {
    if (!onProgChange) {
      const per = (mysound.currentTime / mysound.duration) * 100;
      progressBar.value = per;
      updateTime();
    }
  });

  progressBar.addEventListener('mousedown', () => onProgChange = true);
  progressBar.addEventListener('mouseup', () => {
    mysound.currentTime = (progressBar.value * mysound.duration) / 100;
    onProgChange = false;
    updateTime();
  });

  progressBar.addEventListener('touchstart', () => onProgChange = true);
  progressBar.addEventListener('touchend', () => {
    mysound.currentTime = (progressBar.value * mysound.duration) / 100;
    onProgChange = false;
    updateTime();
  });
}

function changeMusic(newSound) {
  current = musics.findIndex(m => m.fileUrl === newSound);
  if (current === -1) return;

  source.src = newSound;
  document.getElementById('coverImg').src = musics[current].coverURL;
  mysound.load();
  mysound.play();

  changeColorMusic();
  changeArtistTitle();
  updateTime();
}

function changeArtistTitle() {
  const artist = document.getElementById("artista");
  const titulo = document.getElementById("titulo");

  if (musics[current].Tags) {
    artist.innerHTML = musics[current].Tags.TPE1 || "unknown";
    titulo.innerHTML = musics[current].Tags.TIT2 || musics[current].fileName;
  } else {
    artist.innerHTML = "unknown";
    titulo.innerHTML = musics[current].fileName;
  }
}

function changeColorMusic() {
  for (let i = 0; i < musics.length; i++) {
    const mylink = document.getElementById("lim_" + i.toString());
    if (mylink) {
      mylink.style.color = (i === current) ? "red" : "blue";
    }
  }
}

function onPlay() {
  if (!playing) {
    mysound.play();
    playing = true;
    document.getElementById("playbutton").innerHTML = 'pause';
  } else {
    mysound.pause();
    playing = false;
    document.getElementById("playbutton").innerHTML = 'play_arrow';
  }
  updateTime();
}

function skip_next() {
  current = (current + 1) % musics.length;
  source.src = musics[current].fileUrl;
  document.getElementById('coverImg').src = musics[current].coverURL;
  mysound.load();
  mysound.play();

  changeColorMusic();
  changeArtistTitle();
  updateTime();
}

function skip_previous() {
  current = (current === 0) ? musics.length - 1 : current - 1;
  source.src = musics[current].fileUrl;
  document.getElementById('coverImg').src = musics[current].coverURL;
  mysound.load();
  mysound.play();

  changeColorMusic();
  changeArtistTitle();
  updateTime();
}

function updateTime() {
  document.getElementById("ctime").innerHTML = sec2minString(mysound.currentTime);
  document.getElementById("totalTime").innerHTML = sec2minString(mysound.duration);
}

function sec2minString(mytime) {
  const minutes = Math.floor(mytime / 60);
  let seconds = Math.round(mytime % 60);
  seconds = seconds < 10 ? '0' + seconds : seconds.toString();
  return `${minutes}:${seconds}`;
}

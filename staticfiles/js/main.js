var icons = document.getElementsByClassName('icon-nav')

for(var i=0; i<icons.length; i++){
    icons[i].addEventListener('click', ()=>{
        var current = document.getElementsByClassName('active');
        current[0].className = current[0].className.replace(' active', '');
        this.className += ' active';
    })
}
const navButton = document.getElementById('nav-menu-button');
const container = document.querySelector('.container');

navButton.addEventListener('click', ()=> {
    container.classList.toggle('nav-open');
})
const sideMenu = document.querySelector('aside');
const menuButton = document.querySelector('#burger-button');
const closeButton = document.querySelector('#close-button');



// Show sidebar
menuButton.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

// Close sidebar
closeButton.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});


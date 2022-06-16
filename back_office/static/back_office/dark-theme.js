let darkTheme = localStorage.getItem('darkTheme');
const darkThemeToggler = document.querySelector('.theme-toggler');

//check if dark mode is enabled
// if it's enabled, turn it off
//if it's disabled, turn it on

const enableDarkTheme = () => {
    // 1. add the class darkmode to the body
    document.body.classList.add('dark-theme');
    darkThemeToggler.querySelector('span:nth-child(1)').classList.remove('active');
    darkThemeToggler.querySelector('span:nth-child(2)').classList.add('active');
    // 2. update darkMode in the localStorage
    localStorage.setItem('darkTheme', 'enabled');
};

const desableDarkTheme = () => {
    // 1. remove the class darkmode to the body
    document.body.classList.remove('dark-theme');
    darkThemeToggler.querySelector('span:nth-child(1)').classList.add('active');
    darkThemeToggler.querySelector('span:nth-child(2)').classList.remove('active');
    // 2. update darkMode in the localStorage
    localStorage.setItem('darkTheme', null);
};

if (darkTheme === 'enabled') {
    enableDarkTheme();
}

darkThemeToggler.addEventListener('click', () => {
    darkTheme = localStorage.getItem('darkTheme')
    if (darkTheme !== 'enabled') {
        enableDarkTheme();
        console.log(darkTheme)
    } else {
        desableDarkTheme();
        console.log(darkTheme)
    }
});
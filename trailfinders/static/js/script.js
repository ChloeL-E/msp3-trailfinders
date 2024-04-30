/**
 * Function taken from SheCodes and adapted to project
 * Function to hide navbar when scrolling down and show 
 * navbar when scrolling up
 */

document.addEventListener("DOMContentLoaded", function () {
    let prevScrollPos = window.pageYOffset;

    window.addEventListener('scroll', function () {
        const currentScrollPos = window.pageYOffset;

        if (prevScrollPos > currentScrollPos) {
            document.querySelector('.navbar').classList.add('show');
        } else {
            document.querySelector('.navbar').classList.remove('show');
            document.querySelector('.navbar').classList.add('hide')
        }

        prevScrollPos = currentScrollPos;
    });
});

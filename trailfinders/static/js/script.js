/**
 * Function taken from SheCodes and adapted to project
 * Function to add an event listener to wait for DOM load
 * Then to hide navbar when scrolling down and show 
 * navbar when scrolling up
 * Use version ES6
 */

document.addEventListener("DOMContentLoaded", function () {
    let prevScrollPos = window.pageYOffset;

    window.addEventListener('scroll', function () {
        const currentScrollPos = window.pageYOffset;

        if (prevScrollPos > currentScrollPos) {
            document.querySelector('.navbar').classList.add('show');
        } else {
            document.querySelector('.navbar').classList.remove('show');
            document.querySelector('.navbar').classList.add('hide');
        }

        prevScrollPos = currentScrollPos;
    });
});

/**
 *  Dynamic year display-CodexWorld
 *  Gets the element by id and inserts the current year
 */
const year = document.querySelector('#get-year').innerHTML = new Date().getFullYear();



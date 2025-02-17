// Smooth scrolling for anchor links
document.querySelectorAll('nav ul li a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default anchor behavior
        const targetId = this.getAttribute('href').substring(1); // Get the target section ID
        const targetSection = document.getElementById(targetId); // Find the target section
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' }); // Smooth scroll
        }
    });
});

// Form validation for the login form
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent form submission

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // Basic validation
        if (!username || !password) {
            alert('Please fill in both username and password.');
            return;
        }

        // Simulate a successful login (replace with actual backend logic)
        alert(`Welcome back, ${username}!`);
        loginForm.reset(); // Clear the form
    });
}

// Responsive navigation menu for smaller screens
const nav = document.querySelector('nav ul');
const toggleButton = document.createElement('button');
toggleButton.innerHTML = '&#9776;'; // Hamburger icon
toggleButton.classList.add('nav-toggle');
document.querySelector('header').appendChild(toggleButton);

toggleButton.addEventListener('click', function () {
    nav.classList.toggle('active'); // Toggle the 'active' class for the navigation menu
});

// Close the navigation menu when a link is clicked (for mobile)
document.querySelectorAll('nav ul li a').forEach(link => {
    link.addEventListener('click', () => {
        if (nav.classList.contains('active')) {
            nav.classList.remove('active'); // Close the menu
        }
    });
});

// Dynamic background color change for sections on scroll
window.addEventListener('scroll', function () {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
            section.style.backgroundColor = 'rgba(31, 31, 31, 0.98)'; // Highlight the active section
        } else {
            section.style.backgroundColor = 'rgba(31, 31, 31, 0.95)'; // Reset to default
        }
    });
});

// Add a "Back to Top" button
const backToTopButton = document.createElement('button');
backToTopButton.innerHTML = '↑';
backToTopButton.classList.add('back-to-top');
document.body.appendChild(backToTopButton);


// Smooth scroll to the top when the button is clicked
backToTopButton.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Add hover effects to buttons dynamically
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.05)';
        this.style.transition = 'transform 0.3s ease';
    });

    button.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1)';
    });
});
// Smooth scroll for all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href'))
        .scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Simple fade-in animation
window.addEventListener('scroll', function() {
    let sections = document.querySelectorAll("section");
    sections.forEach(section => {
        let position = section.getBoundingClientRect().top;
        let screenPosition = window.innerHeight / 1.3;
        if (position < screenPosition) {
            section.style.opacity = "1";
            section.style.transform = "translateY(0px)";
        }
    });
});

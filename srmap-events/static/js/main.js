document.addEventListener("DOMContentLoaded", function() {
    // Dark mode toggle
    const toggleBtn = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;
    
    // Check localStorage for preferred theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlElement.setAttribute('data-bs-theme', savedTheme);
        updateIcon(savedTheme);
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            let currentTheme = htmlElement.getAttribute('data-bs-theme');
            let newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (!toggleBtn) return;
        if (theme === 'dark') {
            toggleBtn.innerHTML = '<i class="fa-solid fa-sun text-warning"></i>';
        } else {
            toggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    }

    // Form Validation logic (Bootstrap)
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    });
});

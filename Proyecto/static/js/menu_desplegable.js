document.addEventListener('DOMContentLoaded', function () {
    let dropdownBtns = document.querySelectorAll('.dropdown-btn');
    dropdownBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            let dropdownContent = this.nextElementSibling;
            let arrow = this.querySelector('.arrow');

            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
            arrow.innerHTML = arrow.innerHTML === '&#9660;' ? '&#9650;' : '&#9660;';
        });
    });

    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.menu-toggle');

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
    });

    const toggleBtn1 = document.querySelector('.menu-toggle-head');
    
    toggleBtn1.addEventListener('click', function () {
        sidebar.classList.remove('collapsed');
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const profileBtn = document.querySelector('.profile-btn');
    const dropdownContent = document.querySelector('.dropdown-profile-content');

    profileBtn.addEventListener('click', function () {
        dropdownContent.classList.toggle('show');
    });

    window.addEventListener('click', function (e) {
        if (!profileBtn.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });
});


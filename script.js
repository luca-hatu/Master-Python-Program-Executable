const downloadButton = document.querySelector('.download-button');

downloadButton.addEventListener('mouseenter', () => {
    downloadButton.style.animation = 'bounce 0.5s ease';
});

downloadButton.addEventListener('mouseleave', () => {
    downloadButton.style.animation = '';
});

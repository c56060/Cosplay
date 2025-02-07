document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const gallery = document.getElementById('gallery');
    const items = gallery.getElementsByClassName('image-item');

    function searchImages() {
        const searchTerm = searchInput.value.toLowerCase();
        items.forEach(item => {
            item.style.display = 'none';
        });
        const rowBreaks = gallery.getElementsByClassName('row-break');

        items.forEach((item, index) => {
            const captionName = item.getElementsByClassName('caption-name')[0].textContent.toLowerCase();
            const captionNumber = item.getElementsByClassName('caption-number')[0].textContent.toLowerCase();
            if (captionName.includes(searchTerm) || captionNumber.includes(searchTerm)) {
                item.style.display = 'inline-block';
                if ((index + 1) % 4 === 0) {
                    rowBreaks[Math.floor(index / 4)].style.display = 'block';
                }
            }
        });
    }

    function showAllImages() {
        items.forEach(item => {
            item.style.display = 'inline-block';
        });
        rowBreaks.forEach(breakElement => {
            breakElement.style.display = 'block';
        });
    }

    searchInput.addEventListener('input', searchImages);
});

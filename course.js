    function filterItems() {
        const searchInput = document.getElementById('search-bar').value.toLowerCase();
        const cards = document.querySelectorAll('.card');

        // Filter cards
        cards.forEach(card => {
            const cardName = card.getAttribute('data-name').toLowerCase();
            if (cardName.includes(searchInput)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

function showAvailableMoves(position) {
    request('/api/availableMoves', 'POST', { position: position })
        .done((data) => {
            render(data);
        });
};
document.getElementById('noteForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    fetch('/api/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({title, content})
    })
        .then(response => response.json())
        .then(data => {
            const notesContainer = document.getElementById('notesContainer');
            const noteElement = document.createElement('div');
            noteElement.className = 'note';
            noteElement.innerHTML = `<h2>${data.title}</h2><p>${data.content}</p>`;
            notesContainer.appendChild(noteElement);
            document.getElementById('noteForm').reset();
        })
        .catch(error => console.error('Error:', error));
});
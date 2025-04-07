document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = new FormData();
    let fileInput = document.getElementById('imageUpload');
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `<p>Kết quả: ${data.message}</p>`;
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<p>Lỗi: ${error}</p>`;
    });
});
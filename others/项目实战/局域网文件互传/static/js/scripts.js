document.addEventListener('DOMContentLoaded', function() {
    const fileForm = document.getElementById('file-form');
    const textForm = document.getElementById('text-form');

    fileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('upload-result').textContent = data.success ? '文件上传成功' : '文件上传失败';
            if (data.success) {
                updateFileList();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('upload-result').textContent = '文件上传失败';
        });
    });

    textForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_text', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('upload-result').textContent = data.success ? '文本上传成功' : '文本上传失败';
            if (data.success) {
                updateFileList();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('upload-result').textContent = '文本上传失败';
        });
    });
});

function updateFileList() {
    fetch('/get_files')
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('file-list');
            const noFiles = document.getElementById('no-files');
            fileList.innerHTML = '';
            noFiles.style.display = 'none';

            data.forEach(file => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `/uploads/${encodeURIComponent(file.name)}`;
                link.textContent = file.name;
                const sizeText = document.createElement('span');
                sizeText.textContent = ` - 大小: ${file.size} bytes`;
                const timeText = document.createElement('span');
                timeText.textContent = ` - 上传时间: ${file.upload_time}`;
                const deleteButton = document.createElement('button');
                deleteButton.textContent = '删除';
                deleteButton.onclick = function() { deleteFile(file.name); };

                listItem.appendChild(link);
                listItem.appendChild(sizeText);
                listItem.appendChild(timeText);
                listItem.appendChild(deleteButton);
                fileList.appendChild(listItem);
            });

            if (data.length === 0) {
                noFiles.style.display = 'block';
            }
        });
}

function deleteFile(filename) {
    if (confirm("确定要删除此文件吗？")) {
        fetch(`/delete/${encodeURIComponent(filename)}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                alert('删除成功');
                updateFileList();
            } else {
                alert('删除失败');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
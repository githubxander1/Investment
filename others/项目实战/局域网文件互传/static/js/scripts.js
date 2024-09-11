document.addEventListener('DOMContentLoaded', function() {
//监听 DOM 加载完成事件，确保 DOM 完全加载后再执行后续代码。
    const fileForm = document.getElementById('file-form');
    const textForm = document.getElementById('text-form');

//监听文件上传表单的提交事件
    fileForm.addEventListener('submit', function(event) {
        event.preventDefault();//阻止默认的表单提交行为:阻止这种自动刷新或跳转行为；保留用户输入；显示验证错误信息
        const formData = new FormData(this);//创建 FormData 对象，用于收集表单数据
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        })//发起 POST 请求，将表单数据发送到服务器
        .then(response => response.json())//将响应转换为 JSON 格式
        .then(data => {
            document.getElementById('upload-result').textContent = data.success ? '文件上传成功' : '文件上传失败';
            if (data.success) {
                updateFileList();
            }//如果上传成功，则更新文件列表
        })//处理成功响应
        .catch(error => {
            console.error('Error:', error);//处理错误
            document.getElementById('upload-result').textContent = '文件上传失败';//更新上传结果的显示。
        });//
    });//监听文件上传表单的提交事件

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

//更新文件列表
function updateFileList() {
    fetch('/get_files')
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('file-list');
            const noFiles = document.getElementById('no-files');
            fileList.innerHTML = '';//清空列表
            noFiles.style.display = 'none';

            data.forEach(file => { //遍历文件列表，创建每个文件的列表项。
                const listItem = document.createElement('li');//创建列表项

                const link = document.createElement('a');//创建链接
                link.href = `/uploads/${encodeURIComponent(file.name)}`;//设置链接的 href 属性链接地址
                link.textContent = file.name;//设置链接的文本内容

                const sizeText = document.createElement('span');//创建大小文本
                sizeText.textContent = ` - 大小: ${file.size} bytes`;

                const timeText = document.createElement('span');//创建上传时间文本。
                timeText.textContent = ` - 上传时间: ${file.upload_time}`;

                const deleteButton = document.createElement('button');//创建删除按钮
                deleteButton.textContent = '删除';
                deleteButton.onclick = function() { deleteFile(file.name); };//绑定删除按钮的点击事件

                const copyButton = document.createElement('button');
                copyButton.textContent = '复制';
                copyButton.onclick = function() {
                    navigator.clipboard.writeText(file.content)//复制文件内容到剪贴板
                           .then(() => { //成功复制后弹出提示框显示“已复制文本内容”。
                               alert('已复制文本内容');
                           })
                           .catch(error => { //如果复制失败，则显示“复制失败，请重试”
                               console.error('复制失败:', error);
                               alert('复制失败，请重试');
                           });
               };

                if (file.type == 'text/plain') {
                    const contentSpan = document.createElement('span');
                    contentSpan.textContent = `\n${file.content}`;//创建文本内容
//                    contentSpan.textContent = file.content.substring(0, 200);
                    contentSpan.style.whiteSpace = 'nowrap';//禁止换行
                    contentSpan.style.overflow = 'hidden';
                    contentSpan.style.textOverflow = 'ellipsis';
                    contentSpan.style.maxWidth = '200px';//限制最大宽度

                    listItem.appendChild(contentSpan);
                } else {
                    listItem.appendChild(link);
                }

//                listItem.appendChild(link);//将链接、大小文本、上传时间文本和删除按钮添加到列表项中
                listItem.appendChild(sizeText);
                listItem.appendChild(timeText);
                if (file.type == 'text/plain') {
                    listItem.appendChild(copyButton);
                }
                listItem.appendChild(deleteButton);
                fileList.appendChild(listItem);//将列表项添加到文件列表中
            });

            if (data.length === 0) {
                noFiles.style.display = 'block';
            }//如果没有文件，则显示提示信息
        });
}

function deleteFile(filename) {
    if (confirm("确定要删除此文件吗？")) {
        fetch(`/delete/${encodeURIComponent(filename)}`, { method: 'DELETE' })//发起 DELETE 请求，删除指定文件
        .then(response => {
            if (response.ok) {
                alert('删除成功');
                updateFileList();
            } else {
                alert('删除失败');
            }
        })
        .catch(error => console.error('Error:', error));//处理错误
    }
}
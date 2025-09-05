document.addEventListener('DOMContentLoaded', function() {
    // 加载项目列表
    loadProjects();
    // 加载链接列表
    loadLinks();
});

// 添加项目
function addItem() {
    const name = document.getElementById('item-name').value;
    const description = document.getElementById('item-description').value;

    if (!name || !description) {
        alert('请输入项目名称和描述');
        return;
    }

    fetch('/api/projects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, description })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('项目添加成功');
            document.getElementById('item-name').value = '';
            document.getElementById('item-description').value = '';
            loadProjects(); // 重新加载项目列表
        } else {
            alert('项目添加失败: ' + data.message);
        }
    })
    .catch(error => {
        console.error('添加项目时出错:', error);
        alert('添加项目时出错');
    });
}

// 加载项目列表
function loadProjects() {
    fetch('/api/projects')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const select = document.getElementById('project-filter');
            // 清空现有选项（保留第一个"所有项目"选项）
            while (select.options.length > 1) {
                select.remove(1);
            }
            // 添加新项目选项
            data.projects.forEach(project => {
                const option = document.createElement('option');
                option.value = project.id;
                option.textContent = project.name;
                select.appendChild(option);
            });
        } else {
            console.error('加载项目失败:', data.message);
        }
    })
    .catch(error => {
        console.error('加载项目时出错:', error);
    });
}

// 加载链接列表
function loadLinks(projectId = '', linkId = '') {
    let url = '/api/referer-links';
    const params = [];

    if (projectId) {
        params.push(`project_id=${projectId}`);
    }
    if (linkId) {
        params.push(`id=${linkId}`);
    }

    if (params.length > 0) {
        url += '?' + params.join('&');
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const linksList = document.getElementById('referer-links');
            linksList.innerHTML = '';

            if (data.links.length === 0) {
                linksList.innerHTML = '<li>没有找到链接</li>';
                return;
            }

            data.links.forEach(link => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="link-info">
                        <h3>${link.name}</h3>
                        <p><strong>ID:</strong> ${link.id}</p>
                        <p><strong>项目:</strong> ${link.project_name}</p>
                        <p><strong>URL:</strong> <a href=
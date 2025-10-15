// 删除链接 - 全局作用域函数
function deleteLink(linkId) {
    console.log('========= deleteLink函数开始执行 =========');
    console.log('[' + new Date().toISOString() + '] deleteLink函数被调用，ID:', linkId, '，类型:', typeof linkId);
    if (typeof linkId === 'undefined' || linkId === null || linkId === '') {
        console.error('[' + new Date().toISOString() + '] 链接ID无效:', linkId);
        alert('链接ID无效，请刷新页面重试');
        return;
    }
    console.log('[' + new Date().toISOString() + '] 链接ID验证通过，准备显示确认对话框');
    if (confirm('确定要删除这个链接吗？')) {
        console.log('[' + new Date().toISOString() + '] 用户确认删除操作');
        const url = `/api/referer-links/admin/${linkId}`;
        console.log('[' + new Date().toISOString() + '] 准备发送DELETE请求到:', url);
        // 测试用: 输出完整URL
        console.log('[' + new Date().toISOString() + '] 完整URL:', window.location.origin + url);
        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'  // 确保包含cookie等凭证
        })
            .then(response => {
                console.log('[' + new Date().toISOString() + '] 收到删除请求响应，状态码:', response.status);
                if (response.status === 404) {
                    console.error('[' + new Date().toISOString() + '] 未找到该链接，可能已被删除');
                    throw new Error('未找到该链接，可能已被删除');
                } else if (response.status === 403) {
                    console.error('[' + new Date().toISOString() + '] 没有权限删除该链接');
                    throw new Error('没有权限删除该链接');
                } else if (!response.ok) {
                    console.error('[' + new Date().toISOString() + '] HTTP错误! 状态码:', response.status);
                    throw new Error(`HTTP错误! 状态码: ${response.status}`);
                }
                console.log('[' + new Date().toISOString() + '] 响应状态正常，准备处理响应数据');
                // 检查响应是否为空
                const contentType = response.headers.get('content-type');
                console.log('[' + new Date().toISOString() + '] 响应内容类型:', contentType);
                if (contentType && contentType.includes('application/json')) {
                    console.log('[' + new Date().toISOString() + '] 响应为JSON格式，准备解析');
                    return response.json();
                } else {
                    console.log('[' + new Date().toISOString() + '] 响应非JSON格式，返回默认成功对象');
                    return { success: true };
                }
            })
            .then(data => {
                console.log('[' + new Date().toISOString() + '] 成功解析响应数据:', data);
                if (data.success) {
                    console.log('[' + new Date().toISOString() + '] 删除操作成功，准备重新加载链接列表');
                    loadLinks();
                    alert('删除成功');
                } else {
                    console.error('[' + new Date().toISOString() + '] 删除操作失败:', data.error);
                    alert('删除失败: ' + data.error);
                }
            })
            .catch(error => {
                console.error('[' + new Date().toISOString() + '] 删除链接失败:', error);
                alert('删除链接失败，请重试: ' + error.message);
            });
    console.log('========= deleteLink函数执行结束 =========');
    }
}

// 加载链接列表
function loadLinks() {
    fetch('/api/referer-links')
        .then(response => response.json())
        .then(data => {
            const linksList = document.getElementById('links-list');
            linksList.innerHTML = '';
            console.log('加载的链接数据:', data);

            if (data.referer_links && data.referer_links.length > 0) {
                data.referer_links.forEach(link => {
                    const linkItem = document.createElement('div');
                    linkItem.className = 'link-item';
                    // 直接在HTML中添加onclick属性
                    linkItem.innerHTML = `
                        <div class="link-info">
                            <h3>${link.project}</h3>
                            <p>${link.url}</p>
                            <p>${link.description || ''}</p>
                        </div>
                        <div class="link-actions">
                            <button class="btn-edit" data-id="${link.id}">编辑</button>
                            <button class="btn-delete" onclick="deleteLink('${link.id}')">删除</button>
                        </div>
                    `;
                    linksList.appendChild(linkItem);
                    console.log('创建链接项，ID:', link.id);
                });

                // 移除了之前的事件监听代码，现在使用内联onclick属性
                console.log('链接项创建完成，共', data.referer_links.length, '个链接');
            } else {
                linksList.innerHTML = '<p>暂无链接数据</p>';
            }
        })
        .catch(error => {
            console.error('加载链接失败:', error);
            alert('加载链接失败，请重试');
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // 等待links-list元素加载完成后再绑定事件
    setTimeout(function() {
        const linksList = document.getElementById('links-list');
        console.log('links-list元素:', linksList);

        if (linksList) {
            // 直接绑定到links-list元素
            linksList.addEventListener('click', function(e) {
                console.log('links-list内点击事件被触发，目标元素:', e.target);
                console.log('目标元素class:', e.target.className);

                if (e.target.classList.contains('btn-edit')) {
                    console.log('编辑按钮被点击');
                    const linkId = e.target.getAttribute('data-id');
                    editLink(linkId);
                }
            });
        } else {
            console.error('未找到links-list元素');
        }
    }, 100); // 延迟100毫秒确保元素已加载

    // 初始化页面
    loadLinks();

    // 表单提交事件
    document.getElementById('link-form').addEventListener('submit', function(e) {
        e.preventDefault();
        saveLink();
    });

    // 取消编辑按钮事件
    document.getElementById('cancel-edit').addEventListener('click', function() {
        resetForm();
    });

    // 保存链接（添加或更新）
    function saveLink() {
        console.log('========= saveLink函数开始执行 =========');
        const linkId = document.getElementById('link-id').value;
        const project = document.getElementById('link-project').value;
        const url = document.getElementById('link-url').value;
        const description = document.getElementById('link-description').value;

        // 验证表单数据
        if (!project || !url) {
            alert('项目和URL不能为空');
            return;
        }

        const linkData = {
            project: project,
            url: url,
            description: description
        };

        let method = 'POST';
        let apiUrl = '/api/referer-links/admin';
        
        if (linkId) {
            method = 'PUT';
            // 保持使用相同的URL，但在请求体中包含id
            linkData.id = linkId;
        }

        console.log('保存链接，方法:', method, '，URL:', apiUrl);
        console.log('链接数据:', linkData);

        console.log('[' + new Date().toISOString() + '] 保存链接，方法:', method, '，URL:', apiUrl);
        console.log('[' + new Date().toISOString() + '] 链接数据:', linkData);

        fetch(apiUrl, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',  // 确保包含cookie等凭证
            body: JSON.stringify(linkData)
        })
            .then(response => {
                console.log('[' + new Date().toISOString() + '] 保存链接响应状态:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态码: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('[' + new Date().toISOString() + '] 保存链接响应数据:', data);
                if (data.success) {
                    loadLinks();
                    resetForm();
                    alert('保存成功');
                } else {
                    alert('保存失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(error => {
                console.error('[' + new Date().toISOString() + '] 保存链接失败:', error);
                alert('保存链接失败: ' + error.message);
            });
    }

    // 编辑链接
    function editLink(linkId) {
        console.log('========= editLink函数开始执行 =========');
        console.log('编辑链接ID:', linkId);
        // 使用管理员接口获取链接详情
        fetch(`/api/referer-links/admin/${linkId}`)
            .then(response => {
                console.log('获取链接详情响应状态:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态码: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('获取链接详情成功:', data);
                const link = data.referer_links.find(l => l.id === linkId);
                if (link) {
                    document.getElementById('link-id').value = link.id;
                    document.getElementById('link-project').value = link.project;
                    document.getElementById('link-url').value = link.url;
                    document.getElementById('link-description').value = link.description || '';
                    document.getElementById('form-title').textContent = '编辑链接';
                    document.getElementById('cancel-edit').style.display = 'inline-block';
                }
            })
            .catch(error => {
                console.error('获取链接详情失败:', error);
                alert('获取链接详情失败，请重试');
            });
    }

    // 重置表单
    function resetForm() {
        document.getElementById('link-id').value = '';
        document.getElementById('link-project').value = '';
        document.getElementById('link-url').value = '';
        document.getElementById('link-description').value = '';
        document.getElementById('form-title').textContent = '添加新链接';
        document.getElementById('cancel-edit').style.display = 'none';
    }
});
export function logError(error) {
  console.error('An error occurred:', error);
  // 假设我们有一个API端点来记录错误
  fetch('/api/log-error', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ error: error.message })
  }).catch(err => console.error('Failed to log error:', err));
}
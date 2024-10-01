# utils/sync.py
import os
import hashlib
import rclone

def get_file_hash(file_path):
    """计算文件的哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_local_files_and_hashes(local_dir):
    """获取本地目录中的所有文件及其哈希值"""
    files_and_hashes = {}
    for root, _, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            files_and_hashes[file_path] = file_hash
    return files_and_hashes

def get_remote_files_and_hashes(remote_dir):
    """获取远程目录中的所有文件及其哈希值（假设使用 rclone）"""
    output = rclone.run_command(["rclone", "lsjson", remote_dir])
    files_and_hashes = {}
    for line in output.splitlines():
        file_info = json.loads(line)
        if 'Name' in file_info and 'Hashes' in file_info:
            file_path = os.path.join(remote_dir, file_info['Name'])
            file_hash = file_info['Hashes'].get('MD5')
            if file_hash:
                files_and_hashes[file_path] = file_hash
    return files_and_hashes

def sync_files(local_dir, remote_dir):
    local_files = get_local_files_and_hashes(local_dir)
    remote_files = get_remote_files_and_hashes(remote_dir)

    for local_file, local_hash in local_files.items():
        remote_file = local_file.replace(local_dir, remote_dir)
        remote_hash = remote_files.get(remote_file)

        if not remote_hash or local_hash != remote_hash:
            print(f"Syncing {local_file} to {remote_file}")
            rclone.run_command(["rclone", "copy", local_file, remote_file])

    for remote_file, _ in remote_files.items():
        local_file = remote_file.replace(remote_dir, local_dir)
        if local_file not in local_files:
            print(f"Deleting {remote_file} from remote")
            rclone.run_command(["rclone", "delete", remote_file])

if __name__ == "__main__":
    local_dir = "/path/to/local/data"
    remote_dir = "remote:backup/notes"
    sync_files(local_dir, remote_dir)
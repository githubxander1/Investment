# utils/sync_oss.py
import hashlib
import os

from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials.provider import StaticCredentialProvider
from aliyunsdkcore.client import AcsClient
from aliyunsdkoss.request.v20190517 import ListObjectsRequest

access_key_id = 'your_access_key_id'
access_key_secret = 'your_access_key_secret'
bucket_name = 'your_bucket_name'
endpoint = 'your_endpoint'

credentials = StaticCredentialProvider(AccessKeyCredential(access_key_id, access_key_secret))
client = AcsClient(region_id='your_region', credential_provider=credentials)


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


def get_remote_files_and_hashes(bucket_name, prefix=''):
    """获取远程目录中的所有文件及其哈希值"""
    files_and_hashes = {}
    request = ListObjectsRequest.ListObjectsRequest()
    request.set_BucketName(bucket_name)
    request.set_Prefix(prefix)

    response = client.do_action_with_exception(request)
    objects = response.get('Contents')

    for obj in objects:
        key = obj.get('Key')
        etag = obj.get('ETag').strip('"')
        files_and_hashes[key] = etag

    return files_and_hashes


def sync_files(local_dir, bucket_name, prefix=''):
    local_files = get_local_files_and_hashes(local_dir)
    remote_files = get_remote_files_and_hashes(bucket_name, prefix)

    for local_file, local_hash in local_files.items():
        remote_key = os.path.relpath(local_file, local_dir)
        remote_key = os.path.join(prefix, remote_key).replace('\\', '/')

        remote_hash = remote_files.get(remote_key)

        if not remote_hash or local_hash != remote_hash:
            print(f"Syncing {local_file} to {remote_key}")
            with open(local_file, 'rb') as file_data:
                client.put_object(bucket_name, remote_key, file_data)

    for remote_key, _ in remote_files.items():
        local_file = os.path.join(local_dir, remote_key[len(prefix) + 1:])
        if local_file not in local_files:
            print(f"Deleting {remote_key} from remote")
            client.delete_object(bucket_name, remote_key)


if __name__ == "__main__":
    local_dir = "/path/to/local/testdata"
    bucket_name = 'your_bucket_name'
    prefix = 'notes'
    sync_files(local_dir, bucket_name, prefix)
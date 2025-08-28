import argparse
import requests
import json
import os
from pathlib import Path

class DRDRClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        
    def upload_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
            
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(
                f'{self.base_url}/upload',
                files=files,
                headers=self.headers
            )
            
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Upload failed: {response.text}")
            
    def get_file_info(self, file_id):
        response = requests.get(
            f'{self.base_url}/files/{file_id}',
            headers=self.headers
        )
        return response.json()

def main():
    parser = argparse.ArgumentParser(description='DRDR Cloud System CLI Client')
    parser.add_argument('--url', default='http://localhost:8080', help='DRDR service URL')
    parser.add_argument('--api-key', help='API key for authentication')
    
    subparsers = parser.add_subparsers(dest='command')
    
    upload_parser = subparsers.add_parser('upload', help='Upload a file')
    upload_parser.add_argument('--file', required=True, help='File to upload')
    
    info_parser = subparsers.add_parser('info', help='Get file information')
    info_parser.add_argument('--file-id', required=True, help='File ID to query')
    
    args = parser.parse_args()
    
    client = DRDRClient(args.url, args.api_key)
    
    try:
        if args.command == 'upload':
            result = client.upload_file(args.file)
            print(f"Upload successful: {json.dumps(result, indent=2)}")
        elif args.command == 'info':
            result = client.get_file_info(args.file_id)
            print(f"File info: {json.dumps(result, indent=2)}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

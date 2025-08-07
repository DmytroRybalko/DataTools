import argparse
import time
from aux_functions import get_file_names, download_files_sync

def main():
    parser = argparse.ArgumentParser(description="Download files from logger device.")
    parser.add_argument('--ip', type=str, required=True, help='Logger IP address, e.g. http://192.168.0.102')
    parser.add_argument('--save_dir', type=str, default='data', help='Directory to save downloaded files')
    args = parser.parse_args()

    print(f"Connecting to logger at {args.ip}...")
    files2download = get_file_names(args.ip)
    print(f"Found {len(files2download)} files to download.")

    start_time = time.time()
    download_files_sync(args.ip, files2download, args.save_dir)
    elapsed = time.time() - start_time
    print(f"Total time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()

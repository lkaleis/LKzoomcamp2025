import os
import urllib.request
import gzip
import shutil
import time
from google.cloud import storage

# Initialize the Google Cloud Storage client
CREDENTIALS_FILE =  "/home/lpop22/LKzoomcamp2025/01-docker-terraform/1_terraform_gcp/terrademo/keys/my-creds.json"  
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

# Base URL for FHV data (2019)
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv"
YEAR = 2019
MONTHS = [f"{i:02d}" for i in range(1, 13)]  # Loop through all 12 months
DOWNLOAD_DIR = "."  # Directory to store downloaded files

# Google Cloud Bucket name
BUCKET_NAME = "lindakaleis-kestra"  
CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB chunk size for uploading

bucket = client.bucket(BUCKET_NAME)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_file(month):
    """Download the FHV data file for the specified month."""
    month_str = f"{month:02d}"  # Format the month as 2 digits (e.g., 01, 02, ..., 12)
    file_name = f"fhv_tripdata_2019-{month_str}.csv.gz"
    url = f"{BASE_URL}/{file_name}"
    gz_path = os.path.join(DOWNLOAD_DIR, file_name)

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, gz_path)
        print(f"Downloaded: {gz_path}")
        return gz_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def extract_gz(gz_path):
    """Extract .csv.gz file to .csv"""
    if gz_path is None:
        return None

    csv_path = gz_path.replace(".csv.gz", ".csv")
    
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            with open(csv_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Extracted: {csv_path}")
        return csv_path
    except Exception as e:
        print(f"Failed to extract {gz_path}: {e}")
        return None

def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)

def upload_to_gcs(file_path, max_retries=3):
    """Upload the extracted CSV file to GCS"""
    if file_path is None:
        return

    blob_name = f"raw/{os.path.basename(file_path)}"
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE  # Set chunk size for upload

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
            time.sleep(5)  # Wait before retrying

    print(f"Giving up on {file_path} after {max_retries} attempts.")

def process_monthly_files():
    """Download, extract, and upload FHV data files for each month."""
    for month in range(1, 13):  # Loop through months 1 to 12
        # Step 1: Download the .csv.gz file
        gz_file = download_file(month)

        # Step 2: Extract the .csv.gz file
        csv_file = extract_gz(gz_file)

        # Step 3: Upload the extracted CSV file to GCS
        upload_to_gcs(csv_file)

    print("Processing complete!")

if __name__ == "__main__":
    process_monthly_files()

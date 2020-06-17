import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("0.0.0.0", 9876))

def exit():
    import sys
    sys.exit(0)

def send_to_gcs():
    from google.cloud import storage
    from google.oauth2 import service_account
    import glob

    cred = service_account.Credentials.from_service_account_file('service-account-bq.json')
    # client = bigquery.Client(project='kss-home', credentials=cred)
    # table = client.get_table(client.dataset('flights').table('ctnl'))
    bucket_name = 'home-monitor-kss-home'
    bucket = storage.Client(project='kss-home', credentials=cred).get_bucket(bucket_name)
    
    glob.glob("")
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

# TODO: Write from socket to file with date
# Every X minutes send all files to GCS
# Log last timestamp uploaded


while True:
    try:
        data, addr = server_socket.recvfrom(1024)
        print("Data "+data.decode('utf-8'))
        print("Addr "+str(addr))
    except:
        pass

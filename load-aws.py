# This file is for loading images to AWS
# Images originally scraped from Epicurious
# Importantly, my local machine is set up with AWS CLI
# to be authenticated; this script will not work for you
# without that piece.

import boto3
import os, sys
print("Libraries imported successfully.")

images_dir = './raw-data/Food Images/'
s3_bucket = 'sage-recipe-images'
failures = []


# Connect to S3 bucket
try:
    client = boto3.client('s3', region_name = 'us-west-1')
    print("Client successfully established.")
except Exception as e:
    print("Connection to client failed with the following error:")
    print(e)
    sys.exit()


# Loop over files in Food Images directory, and load to S3 bucket
for f in os.scandir(images_dir):
    if f.is_file():
        try:
            client.upload_file(images_dir + f.name,
                                s3_bucket,
                                f.name)
            print("Uploaded:", f.name)
        except Exception as e:
            print("Some exception was encountered when uploading file:", f.name)
            print("Exception encountered:\n" + e)
            failures.append(f.name)
            input("Press enter to continue")


# Write out any failures or lack thereof to notepad        
if len(failures) == 0:
    failures.append("No failures")

with open('failures_06222022.txt', 'w') as file:
    for fail in failures:
        file.writelines([fail])
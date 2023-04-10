import face_recognition
import pickle
import os
import csv
import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3', aws_access_key_id='AKIA3TWA32MBZWZY54HE', aws_secret_access_key='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', region_name='us-east-1')
UNKNOWN_PERSON = "Unknown"
TABLE_NAME = "student_table_two"
header = ["name", "major", "year"]
output_bucket = "output-video-hsh"

temp_dir = "/tmp/"


"""
    This function deletes file from disk of app instance.
"""
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def identify_person(face_encoding, known_encodings):
    encodings = known_encodings['encoding']
    names = known_encodings["name"]
    counter = 0
    for encoding in encodings:
        result = face_recognition.compare_faces([face_encoding], encoding)
        if result[0] == True:
            return names[counter]
        counter = counter + 1
    return "Unknown"

def query_db(person_name):
    dynamo_db = boto3.resource("dynamodb")

    response = dynamo_db.Table(TABLE_NAME).get_item(
        Key = {
            'name' : person_name
        }
    )
    #print("Dynamo db response ", response['Item'])
    major, year = response['Item']['major'], response['Item']['year']
    return [person_name, major, year]

def write_results_s3(data, fileName):
    path = "/tmp/" + fileName + ".csv"
    with open(path, 'w', newline='') as output_file:
        csv_write = csv.writer(output_file)
        csv_write.writerow(header)
        csv_write.writerow(data)
    
    print("Uploading data to s3 bucket for image ", fileName)
    s3.upload_file(path, output_bucket, fileName + ".csv");
    
    print("Removing " + path);
    remove_file(path);

def generate_id(frame_number):
    frame_id = "";
    temp = frame_number
    digit_cnt = 1
    while(digit_cnt<=3):
        frame_id = str(int(temp%10)) + frame_id
        digit_cnt = digit_cnt + 1
        temp = temp/10

    return frame_id;

def face_recognition_handler(event, context):

    known_encodings = open_encoding("encoding")

    bucket = event['Records'][0]['s3']['bucket']['name']
    video_file_name = event['Records'][0]['s3']['object']['key']

    print(video_file_name)

    video_file_path = temp_dir + video_file_name
    with open(video_file_path, 'wb') as data:
        s3.download_fileobj(bucket, video_file_name, data)

    video_file_without_format = video_file_name.split(".")[0]
    os.system("ffmpeg -i " + video_file_path + " -r 1 " + temp_dir + video_file_without_format + "-%3d.jpeg")

    names_image = set()
    frame_number = 1
    while True:

        frame_id = generate_id(frame_number)        
        frame_path = temp_dir + video_file_without_format + "-" + frame_id + ".jpeg"; 

        if os.path.exists(frame_path)==False:
            break

        frame = face_recognition.load_image_file(frame_path)
        face_encodings = face_recognition.face_encodings(frame)

        for encoding in face_encodings:
            person_name = identify_person(encoding, known_encodings)
            print("Printing  person name ", person_name)
            names_image.add(person_name)

        print("Removing " + frame_path);
        remove_file(frame_path);

        frame_number = frame_number + 1

    print("Removing " + video_file_path);
    remove_file(video_file_path)
    if(len(names_image)>=1):
        person_name = list(names_image)[0];

    results = query_db(str(person_name))
    write_results_s3(results, video_file_without_format)




    

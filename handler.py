import face_recognition
import pickle
import os
import boto3


s3 = boto3.client('s3', aws_access_key_id='AKIA3TWA32MBVPBDLKU2', aws_secret_access_key='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', region_name='us-east-1')


# Function to read the 'encoding' file
def open_encoding(filename):
	global data;
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	print(data);
	return data

def identify_person(face_encoding):
    encodings = data['encoding']
    names = data["name"]
    counter = 0
    for encoding in encodings:
        result = face_recognition.compare_faces([face_encoding], encoding)
        if result[0] == True:
            return names[counter];
        counter = counter + 1
    return "Unknown"

def face_recognition_handler(event, context):

    open_encoding("encoding");

    bucket = event['Records'][0]['s3']['bucket']['name']
    video_file_name = event['Records'][0]['s3']['object']['key'];

    print(video_file_name);

    video_file_path = "/tmp/" + video_file_name;
    with open(video_file_path, 'wb') as data:
        s3.download_fileobj(bucket, video_file_name, data)

    video_file_without_format = video_file_name.split(".")[0];
    path = "/tmp/";
    os.system("ffmpeg -i " + video_file_path + " -r 1 " + path + video_file_without_format + "-%3d.jpeg");

    names_image = set();
    i = 1
    while(i<=100):
        
        file_id = "";
        digits = i;
        j = 1;
        while(j<=3):
            req = int(digits%10);
            file_id = str(req) + file_id
            j = j + 1;
            digits = digits/10;
        

        # print(file_id);
        # print(video_file_without_format);
        file_name = "/tmp/" + video_file_without_format + "-" + file_id + ".jpeg"; 

        if os.path.exists(file_name)==False:
            break;

        trump_image = face_recognition.load_image_file(file_name)
        face_encodings = face_recognition.face_encodings(trump_image);

        for encoding in face_encodings:
            person_name = identify_person(encoding);
            names_image.add(person_name);
    
        i = i + 1;


    for each in names_image:
        print(each);



    

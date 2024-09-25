# Video Processing
Developed a website that allows users to upload videos, which will be processed in the background. After processing and extracting subtitles from the video.

## Setup Instructions
**1. Clone the Repository**

    git clone https://github.com/Amal-Krishnanps/Video_process.git
    
    cd video_processing

**2. Create a Virtual Environment**
   
     python -m venv venv
   
 **3. Activate the Virtual Environment**
 
      On Windows:
      venv\Scripts\activate
     
      On macOS/Linux:
      source venv/bin/activate
   
**4. Install Dependencies**

      pip install -r requirements.txt

**5. Apply Migrations**

     python manage.py migrate

**6. Create Superuser**

     python manage.py createsuperuser

**7. Run the Development Server**

     python manage.py runserver

Visit http://127.0.0.1:8000/ to view the API.

### API Endpoints
   
 **Upload Video**
  
  Method: POST
  URL: /upload/
  Payload: Provide video details in the request body including video file you want to process

**List All Videos**

  Method: GET
  URL: ''

**Retrieve Video Details**

  Method: GET
  URL: /videos/{video_id}/

**Search Phrases**

  Method: GET
  URL: /search/
  Payload: Provide keyword you want to search in the request body

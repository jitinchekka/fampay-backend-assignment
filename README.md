# FamPay Backend Assignment

### Problem Statement
To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

### Frontend
The frontend for this project is available at [FamPay Assignment Frontend](https://github.com/jitinchekka/youtube-latest-videos-frontend)
![Landing Page](https://raw.githubusercontent.com/jitinchekka/youtube-latest-videos-frontend/refs/heads/main/screenshots/Screenshot1.png?token=GHSAT0AAAAAACQZFCHKZT4LQGC7XYAGQCL2Z3IDBQQ)
![Search Results](https://raw.githubusercontent.com/jitinchekka/youtube-latest-videos-frontend/refs/heads/main/screenshots/Screenshot4.png?token=GHSAT0AAAAAACQZFCHKZSRYTAKPMFQTXNBGZ3IDCCA)
### API Endpoints
- `/docs` - Swagger UI for the API

- `/ping` - GET - Health check endpoint
Sample request:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/ping' \
  -H 'accept: application/json'
```

Response:
```
{
  "message": "pong"
}
```

- `/videos/` - GET - Get all videos
Sample request:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/videos?page_size=10' \
  -H 'accept: application/json'
```


Response:

    {
    "videos": [
        {
        "video_id": "ncVm8jlHJ80",
        "title": "What AGI Really Is? #ai #openai #agi",
        "id": 4954,
        "thumbnails": "https://i.ytimg.com/vi/ncVm8jlHJ80/hqdefault.jpg",
        "description": "",
        "published_at": "2024-12-22T11:09:08"
        },
        {
        "video_id": "KZL0-_Q7XOU",
        "title": "【12 Days of OpenAIを徹底解説】GPTs研究会モーニングライブ12月22日",
        "id": 5055,
        "thumbnails": "https://i.ytimg.com/vi/KZL0-_Q7XOU/hqdefault.jpg",
        "description": "【12 Days of OpenAIを徹底解説】GPTs研究会モーニングライブ12月22日 「12 Days of OpenAI」は、ChatGPTの公開2周年を ...",
        "published_at": "2024-12-22T10:47:48"
        },

        ....

        {
        "video_id": "AHfsI1J88K4",
        "title": "🚨OpenAI wprowadza przełomowy model &quot;o3&quot;, który jest na poziomie doktoranckim #openai #chatgpt",
        "id": 5005,
        "thumbnails": "https://i.ytimg.com/vi/AHfsI1J88K4/hqdefault.jpg",
        "description": "OpenAI zaprezentowało swój najnowszy model sztucznej inteligencji o nazwie o3, który stanowi znaczący krok naprzód w .",
        "published_at": "2024-12-22T10:27:21"
        },
    ],
    "next_cursor": 4058
    }

- `/search/` - GET - Search videos by title
Sample request:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/search?query=Sora&page_size=10' \
  -H 'accept: application/json'
```

Response
```
{
  "videos": [
    {
      "video_id": "QXd4D7cqfQo",
      "title": "Openai Sora vs Google veo 2 #openai #shorts",
      "id": 4704,
      "thumbnails": "https://i.ytimg.com/vi/QXd4D7cqfQo/hqdefault.jpg",
      "description": "",
      "published_at": "2024-12-22T07:37:36"
    },
    {
      "video_id": "5ff0QnzmDAU",
      "title": "Indian model drinking vine #youtube #shorts #ai  #aigenerated #openai #sora",
      "id": 4063,
      "thumbnails": "https://i.ytimg.com/vi/5ff0QnzmDAU/hqdefault.jpg",
      "description": "Indian model drinking vine. generated with @OpenAI 's Sora.",
      "published_at": "2024-12-22T06:38:16"
    },

   ...

    {
      "video_id": "3oV4mOiz-Z8",
      "title": "AI in Content Creation  OpenAI has just introduced Sora #AINews",
      "id": 4159,
      "thumbnails": "https://i.ytimg.com/vi/3oV4mOiz-Z8/hqdefault.jpg",
      "description": "OpenAI's Sora Makes Videos Visualize Your Ideas: Turn your creative thoughts into stunning videos with just a few words.",
      "published_at": "2024-12-22T01:57:30"
    }
  ],
  "next_cursor": 4159
}
```


### Setup
- Clone the repository
```
git clone https://github.com/jitinchekka/fampay-backend-assignment.git
```
- Create a `.env` file in the root directory and fill the values similar to `.env.example`
- Create a virtual environment
```
python3 -m venv venv
```
- Install the dependencies
```
pip install -r requirements.txt
```
- change the directory
```
cd src
```
- Start the server
```
uvicorn main:app --reload
```

OR

- Run the docker container
```
docker-compose up
```
- The server will be running at `http://127.0.0.1:8000`

### Tech Stack
- FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
It generates interactive API documentation using Swagger UI and it is one of the fastest python frameworks available.

- Redis

Redis is an open-source, in-memory data structure store and has been used to cache the most recently fetched videos from the `/videos` endpoint. It is also used for storing the timestamp of the last video fetched from the YouTube API.

- SQLite

SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. It is used to store the video data fetched from the YouTube API.

It makes a lot of sense to use a relational database for this project as the data is highly structured and the relationships between the data are well defined. SQLite is used as it is easy to set up, development is fast and it is lightweight and deployable with the application.

- Docker

Docker is used to containerize the application and Redis server. It makes it easy to deploy the application and its dependencies in a consistent environment.

- Pagination

The `/videos` and `/search` endpoints support cursor pagination. The `page_size` query parameter can be used to specify the number of videos to be fetched in a single request. The response will contain a `next_cursor` field which can be used to fetch the next set of videos.

### Swagger UI Demo
1. All Endpoints
![All Endpoints](/screenshots/Screenshot1.png)
2. Ping Endpoint
![Ping Endpoint](/screenshots/Screenshot3.png)
3. Videos Endpoint
![Videos Endpoint](/screenshots/Screenshot4.png)
4. Search Endpoint
![Search Endpoint](/screenshots/Screenshot5.png)

### Live demo of logs
![Logs](/screenshots/Screenshot2.png)
A scheduler is running every 10 seconds to fetch the latest videos from the YouTube API and store them in the SQLite database. The logs show the videos fetched from the YouTube API and the videos stored in the SQLite database.
This is implemented using the APScheduler library.

### Author
------------------
*[jitinchekka2@gmail.com](mailto:jitinchekka2@gmail.com) - For any queries or feedback*

*[http://linkedin.com/in/jitinchekka/](http://linkedin.com/in/jitinchekka/)*

Get in Touch
-------------
* Email: mailto:jitinchekka2@gmail.com
* LinkedIn: https://www.linkedin.com/in/jitin-krishna-chekka/
* GitHub: http://github.com/jitinchekka/
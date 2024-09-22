## This is a posts searcher service that allows you to find posts by arbitrary text queries, utilizing Elasticsearch mechanics

## Features:

### 1. Search posts by arbitrary text queries
### 2. Delete post by id

## How to use the project:
### 1. git clone github.com/kirilldarealcaucasian/Elasticsearch-document-searcher
### 2. Create .env file in common/config folder and put the data below in there
```env
  LOG_LEVEL=DEBUG
  ELASTIC_HOST=elasticsearch
  ELASTIC_PORT=9200
  ELASTIC_POSTS_INDEX_NAME=posts_index
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_SERVER=db
  DB_PORT=5432
  DB_NAME=posts_db
```
### 3. cd project
### 4. docker-compose up --build
### 5. Follow to http://127.0.0.1:8000/docs#/ to see endpoints.
### When the project is started, connection to elasticsearch, creation and filling of tables, creation of index and filling the index will happen automatically. 

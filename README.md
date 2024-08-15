<h1 align="center"><img src="https://imgur.com/DeQ6HEq.png" width="128"><br>EchoSphere</h1>

**EchoSphere** is a forum system, featuring a RESTful API built with FastAPI and SQLAlchemy ORM, using SQLite as the database, and a client-side interface developed with React and Material-UI.

## Features

- User authentication
- Users can read, create and comment on topics and message other users
- Administrators can create categories, manage users, topics, categories and different types of access to categories
- Upvoting/Downvoting replies and setting best reply
- Pagination options for categories and topics and filtering for messages from a specific user
- Dark mode and light mode support

## Used Technologies

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy ORM**: The Python SQL toolkit and Object-Relational Mapper that gives application developers the full power and flexibility of SQL.
- **SQLite**: A C library that provides a lightweight disk-based database that doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language.
- **React**: A JavaScript library for building user interfaces.

## Installation
1. Clone the repository:
    
    ```git clone```

2. Install the requirements:

    ```pip install -r requirements.txt```

    ```npm install```

3. Run the client-side and server-side applications in a split terminal:

    ```cd backend``` ->  ```uvicorn main:app```

    ```cd frontend``` ->  ```npm start```

## API Documentation

### Authentication
- `POST /auth`
Endpoint for user registration and login
- `POST /auth/token`
Endpoint for token generation

### Categories
- `POST /categories`
Endpoint for category creation.

- `GET /categories`
Endpoint for retrieving a list of all categories with pagination, filtering, and sorting options.

- `GET /categories/{category_id}`
Endpoint for retrieving information about a specific category and topics related to it.

- `PUT /categories/{category_id}/visibility`
Endpoint for changing the visibility of a category to public or private.

- `PUT /categories/{category_id}/users/{user_id}/read-access`
Endpoint for giving a user read access to a specific private category.

- `PUT /categories/{category_id}/users/{user_id}/write-access`
Endpoint for giving a user write access to a specific private category.

- `PUT /categories/{category_id}/users/{user_id}/access/{access_type}`
Endpoint for revoking a type of access to a specific private category.

- `GET /categories/privilaged-users/{category_id}`
Endpoint for retrieving a list of users with access to a specific private category along with their access type.

- `PUT /categories/lock/{category_id}`
Endpoint for locking a category.

### Topics
- `POST /topics`
Endpoint for topic creation.

- `GET /topics`
Endpoint for retrieving a list of all topics with pagination, filtering, and sorting options.

- `GET /topics/{topic_id}`
Endpoint for retrieving information about a specific topic and its replies.

- `PUT /topics/{topic_id}/lock`
Endpoint for locking a topic.

### Replies
- `POST /replies`
Endpoint for reply creation.

- `GET /replies/{reply_id}`
Endpoint for retrieving information about a specific reply.

- `POST /replies/{reply_id}/vote`
Endpoint for upvoting or downvoting a reply once per user.

- `POST /replies/{reply_id}/best-reply`
Endpoint for setting a reply as the best reply by the topic author.

### Messages
- `POST /messages`
Endpoint for message creation.

- `GET /messages/conversations`
Endpoint for retrieving a list of all conversations for the authenticated user.

- `GET /messages/conversation/{user_id}`
Endpoint for retrieving a conversation with a specific user.

### Users
- `GET /users/info`
Endpoint for retrieving information about the authenticated user.

- `PUT /users/{user_id}/role`
Endpoint for changing the role of a user.


## Contributors

|       Name            |                   Github Username                 |
|:---------------------:|:-------------------------------------------------:|
| Alexander Videnov     | [AlexVidenov1](https://github.com/AlexVidenov1)   |
| Konstantin Ivanov     | [dnrubinart](https://github.com/dnrubinart)       |
| Radostin Mihaylov     | [radoooo11](https://github.com/radoooo11)         |
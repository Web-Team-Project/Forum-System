# Forum System API

## Description

This is a RESTful API for a Forum System, built with FastAPI and SQLAlchemy ORM, using SQLite as the database. The client-side is developed using React.

## Features

- User authentication
- Users can read and create topics and message other users
- Administrators manage users, topics and categories
- Commenting on topics
- Upvoting/Downvoting replies

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

3. Run the client-side and server-side applications in separate terminals:

    ```uvicorn main:app --reload```

    ```npm start```


## API Endpoints

- `/categories`: Endpoint for category-related operations
- `/topics`: Endpoint for topic-related operations
- `/replies`: Endpoint for reply-related operations

## Contribution

|       Name            |                   Github Username                 |
|:---------------------:|:-------------------------------------------------:|
| Alexander Videnov     | [AlexVidenov1](https://github.com/AlexVidenov1)   |
| Konstantin Ivanov     | [dnrubinart](https://github.com/dnrubinart)       |
| Radostin Mihaylov     | [radoooo11](https://github.com/radoooo11)         |
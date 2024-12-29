# FastAPI SQL CRUD REST API Example

This project demonstrates a REST API built with FastAPI, featuring multiple endpoints to perform CRUD operations. The application follows the best practices for structuring a large FastAPI application.


## Getting Started
### Prerequisites

This application uses Poetry for dependency management. Ensure you have Poetry installed on your system. You can install it by following the official Poetry installation guide.

### Setting Up the Environment

#### 1. Create a Virtual Environment

Use the following command to activate a virtual environment:

```poetry shell```
#### 2. Install Dependencies
Install all required dependencies with:

```poetry install```

### Configuration
Create a .env file in the root directory of the project and define the following environment variables:

 - _POSTGRES_CONN_STRING_ : Connection string for your PostgreSQL database.
 - _ACCESS_TOEKN_SECRET_KEY_  : Secret key for generating access tokens.


## Run application locally
To run the application in development mode, use the following command:

```uvicorn main:app --reload```

Server will start running at this url 

```http://127.0.0.1:8080```


### Additional Notes
- This project adheres to FastAPI's recommended folder structure for scalability and maintainability.
- Ensure your PostgreSQL database is running and accessible before starting the application.


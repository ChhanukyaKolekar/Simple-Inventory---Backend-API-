# Simple-Inventory---Backend-API-

This API provides functionality for user registration, login, and CRUD operations on inventory items. It leverages JWT (JSON Web Tokens) for authentication and includes caching for efficient data retrieval.

Features
User registration and authentication
Item creation, retrieval, updating, and deletion
ORM queries for interaction with MySQL database 
The API employs caching to optimize item retrieval. When an item is requested, it first checks the cache before querying the database.

1.User Registration
Endpoint: /api/reg_user/
Method: POST
Request Body:
json
{
  "username": "string",
  "password": "string"
}
Response:201 Created:
{
  "Message": "USER CREATED"
}
400 Bad Request: Validation errors

2. User Login
Endpoint: /api/login_user/
Method: POST
Request Body:
{
  "username": "string",
  "password": "string"
}
Response: 200 OK
{
  "refresh": "string",
  "access": "string"
}
400 Bad Request: Error message for incorrect credentials

3. Create Item
Endpoint: /api/items/
Method: POST
Authentication: Required (JWT)
Request Body:
{
  "name": "string",
  "description": "string",
  "price": "integer"
}
Response: 201 Created: Item data
400 Bad Request: Validation errors

4. Retrieve, Update, or Delete Item
Endpoint: /api/items/<int:pk>/
Method: GET, PUT, or DELETE
Authentication: Required (JWT)

Responses:
GET: 200 OK: Item data
404 Not Found: Item does not exist
   
PUT: 200 OK: Updated item data
404 Not Found: Item does not exist
400 Bad Request: Validation errors
   
DELETE: 200 OK:
{
  "Msg": "Deletion Successful"
}
404 Not Found: Item does not exist

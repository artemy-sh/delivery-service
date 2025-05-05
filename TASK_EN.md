## Microservice for the International Delivery Service

### Task
The service must receive package data and calculate their delivery cost.

## The service must include the following routes:

### 1. Register a package
The package information must include: name, weight, type, and content value in dollars.  
Input data must be in JSON format. Upon receipt, the data must be validated.  
If validation is successful — an individual package ID must be issued, accessible only to the user who submitted the registration request, within their session.

### 2. Get all package types and type IDs
There are three types of packages: clothing, electronics, and miscellaneous.  
Types must be stored in a separate table in the database.

### 3. Get a list of your packages
With all fields included, including the package type name and delivery cost (if already calculated).  
Pagination must be implemented, with the ability to filter packages by type and by whether the delivery cost has been calculated.

### 4. Get package data by its ID
The data should include: name, weight, package type, its value, and delivery cost.

## Periodic tasks:

Every 5 minutes, assign a delivery cost in rubles to all unprocessed packages.

Delivery cost is calculated using the following formula:

> Delivery Cost = (weight in kg * 0.5 + content value in dollars * 0.01) * USD to RUB exchange rate

The USD to RUB exchange rate must be taken from: https://www.cbr-xml-daily.ru/daily_json.js and cached in Redis.

## Notes:
- If the delivery cost has not yet been calculated — display "Not calculated".
- Add the ability to run periodic tasks manually for debugging purposes.

## Mandatory requirements:

- The application must NOT include authentication.
- The application must track users by session, meaning each user has their own list of packages.
- Data must be stored in MySQL.
- Implementation options: Django or FastAPI (with validation through Pydantic).
- API documentation via Swagger.
- Dockerization of the result (`docker-compose up` to run the service and all dependencies).

## Special attention must be paid to:

- Standardization of errors and responses.
- Logging.
- Caching.
- Error handling.
- Code clarity and cleanliness.
- Following widely accepted Python programming standards.
- Documenting the main methods.

## Bonus points for:

- If Django is selected — implementation through DjangoRestFramework.
- Using asynchronous programming (if FastAPI is selected).
- API test coverage.
- A web interface for the application.

## Completion of one of the additional tasks:

- Assume there are about a million packages per day.  
There is a technical requirement to store delivery cost calculation logs in MongoDB.  
Propose and implement a method for calculating the total delivery cost per package type per day using the information from this log.

- Implement package registration using RabbitMQ.  
Packages from the registration route should not be sent directly to the database but through a message broker and workers, which will immediately calculate the delivery cost.  
The periodic delivery cost calculation task would no longer be needed.

- Create a route for assigning a package to a transportation company (adding a company ID — any positive number — to the package record).  
Different companies might attempt to assign themselves to the same package, so it is necessary to guarantee that the first company to request will secure the package.  
This is a high-load system — requests may arrive several times per second.
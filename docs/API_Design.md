API Design

# API Design Doc

### Requirements

#### Functional

- Create User API
- Create TinyURL
- Read TinyURL from Database
- Delete TinyURL
- Delete User Account


#### Non-Functional

- Reading TinyURL must have low latency

### Technical Plan

 - Create User Endpoint
	 - Request Body
		 - userid, name, email
		 - auto generate api_dev_key using uuid4
		 - auto generate user creation date using datetime object
		 - set lastlogin as creation date using datetime object
	  ```
	  POST Method
	  /v1/user
	  
		{
			"userid": "john_001",
			"name": "John Doe",
			"email": "johndoe@gmail.com"
		}
	  
	  ```
		 
	 - Process
		 - Perform sanity check on userid duplication, already registered account
		 - insert into database

	 - Response Body
		 - Success : 200 http code
		 - Already account exist: 409 http code
		 - Error while processing: 500 http code
	
	 ```
	 {
	 	"msg":"User Account Created",
	 }
	 ```

 - Delete User Account
 	 - Request Body
		 - userid, email
		```
		DELETE Method
		/v1/delete-user
		{
			"userid": "john_001",
			"email": "johndoe@gmail.com"
		}
		```
	 
	 - Process
		 - Perform sanity check on userid is already deleted
		 - delete from database and also call Delete TinyURL Module for that user.

	 - Response Body
		 - Success : 200 http code
		 - Already already deleted: 409 http code
		 - Error while processing: 500 http code
		```
			{
				"msg" : "User account deleted",
			}
		```
	
 - Create TinyURL
	 - Request Body
		 - api-dev-key, original url, expiry date
		 - auto generate creation date
		 - if expiry date not given set to 2 years from now
		
		```
		POST Method
		/v1/encode-url
			{
				"api-dev-key": "UUID('ce7f084b-cae8-4679-a3c1-2273424b413b')",
				"original_url": "www.wikipedia.com/john_doe-at-summerfest-university",
				"expiry_date": "2022-12-12"
			}
		```
	 - Process
		 - Encode Original Url and get key for that url
		 - create the tinyurl and dump to database
	 
	 - Response Body
		 - Success 200 http code
		 - Any Error in fetching from DB: 500 internal server error
		
		```
			{
				"msg": "Tiny URL Encoded",
			}
		```
 
 - Read TinyURL
	 - Request Body
		 - tiny_url
	 ```
	 GET Method
	 /{shortkey}
	  shortkey = encode key from original url

	 ```
	 - Process
		 - Get key from tiny url and fetch from database
		 - Redirect to original url
	 - Response Body
		 - Success: Redirect 300
		 - Failure: 500 Internal server error
	```
		{
			"msg": "Redirecting to Original URL"
		}
	```
 - Delete TinyURL
		
	```
		DELETE Method
		/v1/delete-tinyurl

		{
			"key": "sadf211",
			"api-dev-key": "UUID('ce7f084b-cae8-4679-a3c1-2273424b413b')"
		}

	```
	 - Request URL
		 - tiny_url, api-dev-key
	 - Process
		 - Delete row from DB
	 - Response Body
		 - Success: 200
		 - Error: 500 Internal Server Error
		 - 
	```
		{
			"msg": "TinyURL deleted"
		}
	```

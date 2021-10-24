
## Keygen Logic v1

### Functional Requirements:

1. Key generated must be unique across all users
2. Each user can have multiple keys
3. Key Collision is not allowed.
4. Key must of length 6 or 8



### HashIDS Generation Flow:

1. Use [HashID](https://hashids.org/python/) library to create hash given a salt and length
2. HashID will generate a short key with unique salt and integer.


### User Key Generation Flow:

1. URL table created has **unique** constraint over encoded url, such that each time a new key generated must be unique across users
2. Grab the `api_dev_key` from user
3. Add random integer to api_dev_key and create a unique salt for that request only
4. Use HashIDs library to create a short key given integer.
5. Store short key in table.

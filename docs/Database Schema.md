Database Schema


# Database Schema Design Doc

### Requirements

#### Functional


- Have Users details in one Table
- Have URL details in one Table
- Offline Key Generation must have one table
- One table to store used keys
- Used Keys will be transferred to UsedKeys Table
- Each User can have multiple URLs


#### Non-Functional


- Discourage usage on joins, as Tables are read heavy.
- High Consistency

### Technical Plan


![TinyURL DB Schema v1_2_.jpeg](./assets/TinyURL_DB_Schema_v1.jpeg)


- UserID will have 1:N relationship between Users Table and URLs Table 
- Users Table can have different user details
- API dev key can also be added in v2.
- Offline Key Generation Script will be run every time when the number of new keys goes below a threshold.
- New Keys will be dumped to UsedKey Table


##### User Query After login:

```
Select UserID, Name, Email from Users where UserID = 1234
```

##### URL Redirection Query:

```
Select OriginalURL from URLS where UserID = ”1234” and ExpirationDate < GetDate() and EncodedURL = ‘short_url_clicked”
```

##### Offline Key Generator Service Query:

```
Insert Into Table NewKeyGenerated (CreationDate, key) Values (GetDate(), Key)
```

```
Select Key from NewKeyGenerated limit 1
```

##### UsedKeys Dumping:

``` 
Insert Into Table UsedKeys (Key, isitUsed, ExpirationDate, CreationDate) values (key, True, ExpirationDate, CreationDate)
```
##### Usedkeys Flag Set when user deletes key or expires:

```
Update table UsedKeys set isitUsed=False where key=’user_key’
```

##### UsedKeys Cleanup:

```
Select key from UsedKeys where isitUsed=False or ExpirationDate < GetToday()
```

```
Insert Into Table NewKeyGenerated (CreationDate, key) Values (GetDate(), Key)
# key same as above query from UsedKeys
```






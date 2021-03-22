# Computer Vulnerability System

#### Afeka - College of Engineering in Tel Aviv

#### Students:

* **Lir Shindelman**
* **Niv Sorek**

**Lecturer: Eli Weintraub**

## How to install:

* Clone Project from git
* In Terminal:

```
venv\Scripts\activate
pip install -r requirements.txt
set FLAST_APP=server.py
flask run
```


* Make sure you have a Constants.py file in `sec/resources`

## Http Requests:

Get full organisation details JSON:

 ```
GET /organisation
```

Get **single** user details JSON:

 ```
GET /user/{user_id}
```
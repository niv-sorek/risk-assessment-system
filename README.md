# Computer Vulnerability System
####Afeka - College of Engineering in Tel Aviv
#### Students:
* **Lir Shindelman**  
* **Niv Sorek**  
##### Lecturer: Eli Weintraub   


## How to install:
* Clone Project from git
* Open Terminal
* Navigate to your project main directory
* Create a virtual environment by:
```
    python -m venv venv
```

* navigate to this dir: 
```
/venv/scripts
```
   
* run:
    `activate`
   
* Navigate back to project's main folder and run
 ```
    pip install -r requirements.txt
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
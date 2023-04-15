# api_yamdb by "Python 74"

### Brief Description

The project YaMDb collects users recalls on publications.
The publications do not store in YaMDb, there is no option to see movie or listen to music.
The publications categorized such as "Books", "Movies", "Music". For example in "Books" category there may be publications as "Vinnie-Pukh and all-all-all", "Martian chronicle", and "Davecha" song of "Bugs"-banda and Bakh second suite.
Categories list might be expanded (for example, it can be added category "Art" or "Jeweler").
It could be committed pre-set genre as "Fairy tale", "Rock" or "Arthouse" to publication.

Adding of Titles, Categories or Genres may be done by Administrator only.
Grateful or indignant Users leave text Reviews for the works and Score/Rate the work in the range from 1 to 10 (an integer); from User Score, an Average Score of the Title is applied - Rating (integer). A User can leave only one Review per a Title.
Users can leave Comments on Review.
Only Authenticated Users can add Reviews, Comments and Score.

Anonym — could read Titles descriptions, Reviews and Comments.
Authenticated User (user) — could, as Anonym, additionally he could POST Reviews and put Score to Titles (Movies/Books/Songs), could Comment on foreign Reviews; Could edit and delete own Reviews and Comments. This role applied by default to any new User.
Moderator (moderator) — same rights, as for Authenticated User with rights addition to remove any Reviews and Comments.
Administrator (admin) — all rights to control all pproject content. Could create and delete Titles, Categories & Genres. Can adjust Roles to Users.
Django Superusers — poses Administrator rights (Admin).

The project has endpoints sections (with -requests | endpoints):

#####AUTH
```
(POST | http://127.0.0.1:8000/api/v1/auth/signup/), 
(POST | http://127.0.0.1:8000/api/v1/auth/token/);
```

#####CATEGORIES 
```
(POST or GET | http://127.0.0.1:8000/api/v1/categories/), 
(DELETE | http://127.0.0.1:8000/api/v1/categories/{slug}); 
```

#####GENRES 
```
(POST or GET | http://127.0.0.1:8000/api/v1/genres/), 
(DELETE | http://127.0.0.1:8000/api/v1/genres/{slug});
```

#####TITLES 
```
(POST or GET | http://127.0.0.1:8000/api/v1/titles/), 
(GET, PATCH, DELETE | http://127.0.0.1:8000/api/v1/titles/{titles_id}/);
```

#####REVIEWS 
```
(POST or GET | http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/), 
(GET, PATCH, DELETE | http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/);
```

#####COMMENTS 
```
(POST or GET | http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/),
(GET, PATCH, DELETE | http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/);
```

#####USERS 
```
(POST or GET | http://127.0.0.1:8000/api/v1/users/), 
(GET, PATCH, DELETE | http://127.0.0.1:8000/api/v1/users/{username}/),
(GET, PATCH | http://127.0.0.1:8000/api/v1/users/me/)
```

#### For further details please refer: http://127.0.0.1:8000/redoc/


### How to lauch the project:

##### Clone repository:

```
git clone git@github.com:smart2004/api_yamdb.git
```

##### Switch to the folder:

```
cd api_yamdb
```

##### Create and activate virtual environment:

```
py -3.9 -m venv venv
```

```
source venv/scripts/activate
```


##### Setup dependencies from requirements.txt file:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

##### Apply migrations:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

##### Launch server:

```
python manage.py runserver
```

# 202112-25-Roommate-Apartment-Finding-Platform
EECS E6893 Big Data Analytics final project

## Introduction
The number of international students in the United States is increasing these years. It is a little hard for new international students to find roommates and apartments which fit their needs. So, this project is going to build a roommates and apartments platform for new students. We designed our own frontend website and will use cluster algorithm like euclidean distance, cosine similarity and K-Means to get our recommendation, the result will show on the frontend back. Besides, we will compare algorithm we used to find which one is better for our platform.

## Prerequisites
### VM Environment

### Packages

## Datasets
Roommates: a dataset contains 13+ features and 3000+ rows including first name, last name, email address, uni, gender, hobbies, etc. 
Apartments: a dataset contains 10+ features and 40000+ rows including name, address, location, distance, etc.
## Demo

You can see the demonstration of our project throught this link: https://www.youtube.com/watch?v=ccGrH4LN8sA
## Flow Chart

## Results

## Organization
```
./
├── .gitignore
├── README.md
├── data
│   ├── airbnb.csv
│   ├── countries.txt
│   ├── majors.txt
│   ├── roommates.csv
│   └── shcools.txt
├── docs
│   ├── 6893_progress_paper.doc
│   ├── figs
│   │   ├── fig1arch.png
│   │   ├── fig2flowchart.png
│   │   ├── fig3frontinfo.png
│   │   ├── fig4frontresult.png
│   │   └── flowchart.png
│   ├── progress_report.docx
│   └── ~$93_progress_paper.doc
├── final_BDA
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── search.cpython-38.pyc
│   │   ├── search2.cpython-38.pyc
│   │   ├── settings.cpython-38.pyc
│   │   ├── urls.cpython-38.pyc
│   │   ├── views.cpython-38.pyc
│   │   └── wsgi.cpython-38.pyc
│   ├── asgi.py
│   ├── search.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── src
│   ├── create_table_gbp.py
│   ├── knn+cosine_similarity.ipynb
│   ├── pull_from_gbq.py
│   └── push_to_gbq.py
├── static
│   ├── css
│   │   ├── postPatt.css
│   │   └── resultsPatt.css
│   ├── js
│   │   ├── button.js
│   │   └── display.js
│   └── picture
│       ├── Columbia.jpg
│       └── columbia_university.jpg
└── templates
    ├── post.html
    └── results.html
```

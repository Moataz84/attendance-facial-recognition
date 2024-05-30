# Attendance Facial Recognition

A simple solution for taking attendance using facial recognition in Python.

## Table of Contents
- [Description](#description)
- [Technologies](#technologies)
- [Setup](#setup)
- [License](#license)

## Description

This project is intended to be used as 

# Technologies

This project uses Python, Flask and OpenCV.

## Setup
To run this project:

1. Clone this repository.
2. Create a new Python environment using `python -m venv <name-of-your-environment>`.
3. Activate your environment then run `pip install -r requirements.txt`.
4. Create a folder named `SSL` and run the command `openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365` to create a self-signed certificate.
5. Create a `tmp` folder to store temporary images.
6. Create a `public/imgs` folder and add all of your images to it.
7. Create a `data/encoded.json` file, a `data/list.json` file and a `data/present.json` file.
8. Create a list in `list.json` and for each person add:
- `id`: An id for the person
- `name`: The person's name
- `profile`: The file name of the person's profile picture
- `imgs`: Array containing all of the filenames of images for that person.
9. Run the `encode.py` to create a list of people with encoded images.
10. Copy the contents of `list.json` to `present.json` and replace the `imgs` property with the `present` property and set it to `false`. Add a `time` property to the `list.json` file and set it to `null`.
11. Run the app using `python app.py`.

## License

MIT License

Copyright (c) [2024]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
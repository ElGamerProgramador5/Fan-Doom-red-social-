# Fan_Doom Mini Social Network

Fan_Doom is a mini social network that combines the features of Reddit and Wikipedia, allowing users to create, share, and discuss content related to their favorite fandoms. This project is built using Django for the backend and utilizes HTML, CSS, and JavaScript for the frontend.

## Features

- **User Authentication**: Users can register, log in, and manage their profiles.
- **Post Creation**: Users can create posts related to various fandoms, including text, images, and links.
- **Discussion Threads**: Each post can have comments, allowing for discussions among users.
- **Wiki Pages**: Users can create and edit wiki pages to provide detailed information about different fandoms.
- **Voting System**: Users can upvote or downvote posts and comments, influencing their visibility.

## Project Structure

```
Fan_Doom
├── fan_doom
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── templates
│       └── core
│           ├── base.html
│           ├── home.html
│           └── post_detail.html
│   └── static
│       └── core
│           ├── css
│           │   └── style.css
│           └── js
│               └── main.js
├── manage.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Fan_Doom.git
   ```
2. Navigate to the project directory:
   ```
   cd Fan_Doom
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
6. Run database migrations:
   ```
   python manage.py migrate
   ```
7. Start the development server:
   ```
   python manage.py runserver
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
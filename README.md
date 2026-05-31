# Kanban App - CS50x Final Project
#### Video Demo:  <URL HERE>
#### Description:
I chose to build this app as my final project for CS50x because I wanted an intuitive
way to organize my thoughts and tasks ahead of me.

Having benefited from the open-source community, I wanted create something that someone else
could use, build upon, and learn from.

There are many existing solutions out there for this type of project, but I've always
found that they lack something for me personally. So I set out to create my own version
that can hopefully bridge those gaps. (unfortunately this isn't it either)

---

#### Implemented Features

- **User Authentication (Login/Register)**
  - Dedicated pages for logging in and creating accounts.
  - Uses `flask session` to manage user's information.
  - Stores passwords securely using `flask_bcrypt` as hashing algorithm.

- **Tasks Management**
  - Create/Delete tasks.
  - Create/Delete columns.

- **Drag-and-Drop functionality**
  - Tasks can be moved to different columns using the mouse.

- **Responsive UI**
  - Used `Bootstrap` to create the UI.
  - Automatically switches between dark/light mode based on user's system settings
  - Dedicated button for theme switching

- **SQLite Database**
  - All data is stored and managed in a single SQLite database

---

#### Design choices and what I learned
- **File Structure**
  - One of the challenges I faced was structuring my project files.
    I tried to research best practices and found that I can structure my project in a way
    that is modular. which allows me copy/paste/delete parts of my project but still allows it to function.
  - I still have a lot to learn in this aspect. In the future I might separate the backend and frontend.

- **Security**
  - I learned about how to securely store password and sensitive data in the database.
  - I stored the passwords using hash+salt.
  - I used flask's session with a configurable 'SECRET KEY'. (but honestly, I still need to learn more about this)
  - Used `Flask-WTF` to protect against CSRF. (for the login and creating accounts)

- **Frontend**
  - I used `Bootstrap` as a way to style my app.
  - I have also learned of other frameworks, but I decided to use bootstrap for its simplicity.
  - JavaScript was very challenging to me because of it's syntax and the fact that my time with it was very limited.
  - I found that my javascript was very difficult to read. In the future, I would like to learn more about
    how to write clean code.

- **Backend**
  - I used `Flask` to manage the backend of my app.
  - I really enjoyed Python as a language and also Flask once I learned about it.
  - while I did have some challenges going back and forth from Python and JavaScript,
    it was overall a fun and rewarding learning two languages at once.
  - In the future I would like to separate the code for the backend and the frontend.
  - One of the biggest problems was deciding whether something should be handled client side or server side.
  - I think it will be much better if in the future I just make flask handle API requests only.
  
- **Git and project management**
  - I used git to manage and track my project's changes.
  - There are still a lot of features git offers that I haven't utilize and I look forward trying in the future.

- **UI / UX**
  - One of the topics I looked forward to learning about was UX design.
  - I learned a lot about good design and intuitive UI.
  - Learned about creating beautiful interfaces that guides the user visually.
  - In the future, I would like to dive deeper in this area because I find that
    this aspect is what I really enjoyed.

---

#### Current Limitations
I tried my best with the knowledge I had to create this app. however, the project got more and more
complicated and hard to read as time went on. I picked up new techniques but it would have been a huge hassle
to go back and change things.

While I am satisfied with what I created despite the limitations. there are some features I would like
to include in the future versions.

Missing features:
- task due dates or priority levels
- task tags and categories
- comments or attachments per task
- user profile page

---

#### Installation & Setup
```bash
# clone this repository
git clone https://codeberg.org/ssaturgo/kanban-app
cd kanban-app

# create a virtual environment
python3 -m venv .venv

# activate virtual environment
# - for windows
.venv\Scripts\activate
# - for linux and mac
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# initialize db
flask --app kanban init-db

# run the app
flask --app kanban run
```
then go to http://127.0.0.1:5000 on your browser

---

#### Author
CS50 Final Project — Sheikh Norsam Saturgo  
*Built with patience, debug output, and rubber ducks.* 🦆
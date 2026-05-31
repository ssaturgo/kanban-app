# Kanban App - CS50X Final Project
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

> *Detailed setup instructions will be added here.*  
> Typical steps will include:
> - Creating a virtual environment
> - Installing dependencies (`pip install -r requirements.txt`)
> - Initializing the database (`flask init-db`)
> - Running the app (`flask run`)
> - Accessing `http://127.0.0.1:5000`

---

#### Author
CS50 Final Project — Sheikh Norsam Saturgo  
*Built with patience, debug output, and rubber ducks.* 🦆
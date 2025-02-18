# Calgary Connect

Calgary Connect is a web-based solution designed to help individuals who are **new to Calgary** (or new to living independently) by offering a **community forum**, **real-time/private messaging**, and **personal finance tracking**—all in one place. We aim to provide practical tools and local guidance to ease the transition to independent living in Calgary.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Setup & Installation](#setup--installation)
4. [Usage](#usage)
5. [Key Highlights](#key-highlights)
6. [Future Enhancements](#future-enhancements)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

1. **Community Forum**
   - Browse, create, and comment on posts about budgeting tips, grocery deals, household advice, etc.
   - Attach images to illustrate local store flyers or share photos of recommended items.
   - Filter posts by category (e.g., *FinancialAdvice*, *MealPreps*, *HouseholdTips*).

2. **Direct Messaging**
   - One-on-one chats for personalized support or to build friendships with other new Calgarians.
   - In the future it will use WebSockets (via Django Channels) for real-time messaging but for now it's a JavaScript polling fallback.

3. **Finance Manager**
   - Track income and expenses directly on the site—no external spreadsheet required.
   - View total income, total expenses, and your balance at a glance.
   - Ideal for those new to managing rent, groceries, and other bills in Calgary.

4. **User Profiles**
   - Each user has a profile with optional bio and profile picture upload.
   - Follow/unfollow other users and “like” their posts.
   - Start a private chat directly from someone’s profile.

5. **Search & Filtering**
   - Easily filter forum posts by category.
   - Search for specific keywords or tags (planned enhancement).

---

## Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) (Python)  
- **Database**: [MySQL](https://www.mysql.com/)  
- **Real-Time**: JavaScript Polling using [setInterval](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) to update messages every second  
- **Frontend**: [Bootstrap 5](https://getbootstrap.com/) along with custom CSS  
- **Authentication**: Django’s built-in user model and session management

---

## Setup & Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/YourUsername/CalgaryConnect.git
   cd CalgaryConnect
2. **Create and Activate a Virtual Environment (optional but recommended)**  
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
4. **Configure the Database**

Update the DATABASES configuration in app/settings.py with your MySQL credentials.

5. **Run Migrations**  
   ```bash
    python manage.py makemigrations
    python manage.py migrate
6. **Create a Superuser (optional, for Django admin)**  
   ```bash
    python manage.py createsuperuser
7. **Run the Development Server**  
   ```bash
    python manage.py runserver


## Usage

- **Sign Up / Log In:**  
  Create an account or log in using your credentials.

- **Community Forum:**  
  - Post content with optional image attachments.  
  - Comment on posts and like/unlike posts.

- **Direct Messaging:**  
  - Start a one-on-one chat from the messages page or directly from a user’s profile.

- **Finance Manager:**  
  - Enter your income and expense entries.  
  - View a summary including total income, total expenses, and your balance.

- **User Profiles:**  
  - Edit your bio and update your profile picture.  
  - Follow or unfollow other users.  
  - Start a direct message from any user’s profile.

---

## Key Highlights

- **Local-Focused Guidance:**  
  Tailored financial advice and community tips specifically for Calgary residents.

- **All-in-One Platform:**  
  Integrates community support, finance management, and direct messaging.

- **User-Friendly:**  
  A straightforward interface that simplifies independent living and financial tracking.

---

## Future Enhancements

- **Advanced Budget Visualizations:**  
  Graphs and charts to visualize spending patterns.

- **Enhanced Real-Time Messaging:**  
  Transition from JavaScript polling to full WebSocket integration.

- **Group Chats:**  
  Enable group discussions for broader community support.

- **Personalized Financial Tips:**  
  Automated suggestions based on user spending habits and local deals.

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository and clone it locally.
2. Create a new branch for your feature or fix.
3. Commit your changes with descriptive commit messages.
4. Open a pull request with a summary of your changes.

Please follow our coding guidelines and ensure all tests pass before submitting a PR.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the software while giving proper credit to the original contributors.

---

## About the Project

We developed **Calgary Connect** to address the challenges faced by newcomers to Calgary. Many individuals moving to a new city struggle to find reliable financial advice, local shopping recommendations, and community support. Inspired by our own experiences and extensive research, we built a platform that combines a community forum, direct messaging, and a finance manager into a single, user-friendly site.

### What We Learned

- **Collaborative Development:**  
  Working as a team allowed us to blend diverse ideas into a cohesive solution.

- **Local Insights:**  
  We leveraged local data to provide relevant financial tips and community advice.

- **Technical Growth:**  
  Integrating Django, MySQL, and real-time messaging challenged us to learn and adapt quickly.

- **User Experience Focus:**  
  Balancing functionality with simplicity was key to making the platform accessible to all users.

### Challenges Faced

- **Database Integration:**  
  Configuring MySQL and managing migrations required careful attention.

- **Real-Time Messaging:**  
  Implementing a real-time chat system with fallback mechanisms was a complex task.

- **Responsive Design:**  
  Ensuring the interface worked well on both desktop and mobile devices was a priority.

- **Feature Integration:**  
  Combining financial management, community interaction, and messaging into a single platform was challenging but ultimately rewarding.

---

**Thank you for checking out Calgary Connect!**  
We’re excited to continue evolving the platform to better serve the Calgary community.


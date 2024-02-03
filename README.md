# Yatube: A Platform for Publishing Posts

## Choose Your Language

- [English](README.md)
- [Русский](README.ru.md)

---

## About The Project

Yatube is a platform for those who love to write and share their thoughts and ideas. Here, you can create your unique page, post your writings, follow interesting authors, and comment on their posts.

### Key Features:
- **Author's Personal Page:** The author's page displays general information about them and all their posts.
- **Post Creation and Editing:** Users can create new posts and edit existing ones.
- **Subscriptions:** Follow authors whose works inspire you.
- **Commenting:** Engage with the community through comments on posts.
- **Publication in Communities:** Posts can be published in various communities created by the site administrator.
- **Post Sorting:** Posts on the personal page are displayed in order from newest to oldest.
- **Testing:** The project's functionality is covered by tests, ensuring its reliability and stable operation.

### Technologies

- Django
- Python
- HTML & CSS

### Project Setup

1. **Clone the repository:**
    ```sh
    git clone git@github.com:nir0k/hw02_community.git
    cd hw02_community
    ```
2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```
3. **Install dependencies:**
    ```sh
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. **Apply migrations:**
    ```sh
    cd yatube
    python3 manage.py migrate
    ```
5. **Start the project:**
    ```sh
    python3 manage.py runserver
    ```

### Tests
To run the tests, use the following command:
```sh
python manage.py test
```
This will enable you to check the correctness of the main functions and the platform's stability.
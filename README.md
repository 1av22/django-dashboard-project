# Global Development Data Dashboard

A full-stack web application that visualizes economic and demographic data from the World Bank. The project features a secure Django backend serving a REST API to an interactive, dynamic JavaScript frontend.

**Live URL:** [https://your-project-name.onrender.com](https://your-project-name.onrender.com) ---
## Features

* **User Authentication:** Secure user registration, login, and logout functionality.
* **Interactive Dashboard:** A multi-chart dashboard built with Chart.js.
* **Dynamic Filtering:** Users can filter data by country and year, with charts updating in real-time.
* **Conditional Chart Rendering:** The main GDP chart dynamically switches between a pie chart for multi-country comparison and a bar chart for a single country's time-series trend.
* **Robust Data Pipeline:** A backend management command uses the Pandas library to clean, transform, and load raw World Bank CSV data into the database.
* **REST API:** A RESTful API built with Django REST Framework serves the cleaned data to the frontend.

---
## Tech Stack

-   **Backend:** Django, Django REST Framework, Gunicorn
-   **Frontend:** HTML, CSS, Vanilla JavaScript, Chart.js
-   **Database:** PostgreSQL (Production), SQLite3 (Development)
-   **Data Processing:** Pandas
-   **Deployment:** Render

---
## Local Setup Instructions

To run this project locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up the Database:**
    ```bash
    python manage.py migrate
    ```

5.  **Load the World Bank Data:**
    *(Note: The required `final_data.csv` file should be placed in a `/data/` directory in the project root).*
    ```bash
    python manage.py seed_data
    ```

6.  **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---
## Test User Credentials

To test the live application without registering, you can use the following credentials:

* **Username:** `testuser`
* **Password:** `testpassword123`

*(Note: To create this user, I deployed the application and used the built-in signup form to register a new account.)*
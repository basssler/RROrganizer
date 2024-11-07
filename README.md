# RRO Python Book Categorizer
A simple book cataloging app built with Streamlit, allowing users to add books by scanning ISBN barcodes or entering information manually. The app integrates with Google Sheets to store cataloged books and utilizes the Google Books API to fetch book details based on ISBN. The public version does not include private credentials.

## Features
- Scan ISBN barcodes to add books automatically.
- Manually enter book information.
- Store cataloged books in Google Sheets.
- Fetch book details like title, author, and genre from Google Books API.
- Download cataloged data as a CSV.
## Technologies Used
- **Streamlit:** Web framework used to build the user interface.
- **Docker:** For containerizing the application, making it easy to deploy.
- **Fly.io:** Hosting platform for deploying the Dockerized Streamlit app.
- **Google Sheets API:** Used to store and retrieve book data.
- **Google Books API:** Used to fetch book information based on ISBN.
## Requirements
- **Python** 3.7+
- **Docker** (for deployment)
- **Fly.io Account** (for deployment)
- **Google Cloud Project** (for access to Google Sheets and Google Books APIs)

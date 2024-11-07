import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyzbar.pyzbar import decode
from PIL import Image
import requests

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("ENTER GOOGLE SHEET NAME HERE").sheet1  # Use your sheet's name

# Load existing data from Google Sheets
def load_catalog():
    rows = sheet.get_all_records()
    return pd.DataFrame(rows)

# Function to add a new row to Google Sheets
def add_book_to_sheet(book_info):
    sheet.append_row(list(book_info.values()))

# Title of the app
st.title("Razorbook Reach Organizer")
st.text("Thanks ChatGPT :)")

# Load the existing catalog
book_catalog = load_catalog()

# Function to get book information from Google Books API
def get_book_info(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()
    if "items" in data:
        book_info = data["items"][0]["volumeInfo"]
        return {
            "Title": book_info.get("title", "Unknown Title"),
            "Author": ", ".join(book_info.get("authors", ["Unknown Author"])),
            "Genre": ", ".join(book_info.get("categories", ["Unknown Genre"])),
            "Published Date": book_info.get("publishedDate", "Unknown Date"),
            "ISBN": isbn,
            "Lexile": "Unknown Lexile"  # Modify if you have a way to retrieve Lexile
        }
    return None

# Camera input to scan ISBN barcode
st.header("Scan ISBN Barcode")
isbn_image = st.camera_input("Scan the book's ISBN barcode")

# Function to decode ISBN from the barcode image
def decode_isbn(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")
    return None

# Process the ISBN image and get book information
if isbn_image:
    image = Image.open(isbn_image)
    isbn_code = decode_isbn(image)
    
    if isbn_code:
        book_info = get_book_info(isbn_code)
        
        if book_info:
            add_book_to_sheet(book_info)
            st.success(f"Book '{book_info['Title']}' added to the catalog!")
        else:
            st.error("Book information could not be retrieved. Please try a different ISBN.")
    else:
        st.error("No valid ISBN barcode found. Please try again.")

# Section for Manual Book Entry
st.header("Manually Add a New Book")
manual_title = st.text_input("Title")
manual_author = st.text_input("Author")
manual_genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Other"])
manual_published_date = st.text_input("Published Date")
manual_isbn = st.text_input("ISBN")
manual_lexile = st.text_input("Lexile Measure (optional)")

# Button to add the manually entered book
if st.button("Add Book Manually"):
    manual_book = {
        "Title": manual_title,
        "Author": manual_author,
        "Genre": manual_genre,
        "Published Date": manual_published_date,
        "ISBN": manual_isbn,
        "Lexile": manual_lexile or "Unknown Lexile"
    }
    add_book_to_sheet(manual_book)
    st.success(f"Book '{manual_title}' added to the catalog!")

# Display the current catalog of books
st.header("Cataloged Books")
st.dataframe(book_catalog)

# Download button for cataloged books
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

csv = convert_df(book_catalog)

st.download_button(
    label="Download Catalog as CSV",
    data=csv,
    file_name="book_catalog.csv",
    mime="text/csv",
)

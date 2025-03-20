import streamlit as st
import json
import os
import time

# Custom CSS for modern and animated UI
st.markdown("""
    <style>
    /* Background animation */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    body {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    .stApp {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    /* Responsive heading */
    .responsive-heading {
        font-size: 32px;
        text-align: center;
        margin-bottom: 20px;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    @media (max-width: 600px) {
        .responsive-heading {
            font-size: 24px;
        }
    }
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Input field styling */
    .stTextInput>div>div>input {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        transition: border-color 0.3s ease;
        width: 100%;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
    }
    /* Radio button styling */
    .stRadio>div {
        flex-direction: row;
        align-items: center;
    }
    .stRadio>div>label {
        margin-right: 10px;
    }
    /* Markdown styling */
    .stMarkdown {
        font-size: 16px;
        color: #333333;
    }
    /* Success and warning messages */
    .stSuccess {
        color: #4CAF50;
        font-weight: bold;
    }
    .stWarning {
        color: #FFA500;
        font-weight: bold;
    }
    /* Mobile-specific styles */
    @media (max-width: 600px) {
        .stTextInput>div>div>input {
            font-size: 14px;
        }
        .stButton>button {
            font-size: 14px;
            padding: 8px 16px;
        }
        .stMarkdown {
            font-size: 14px;
        }
        .stRadio>div {
            flex-direction: column;
            align-items: flex-start;
        }
        .stRadio>div>label {
            margin-right: 0;
            margin-bottom: 5px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

fileData = 'library.txt'

def loadingLibrary():
    if os.path.exists(fileData):
        with open(fileData, 'r') as file:
            return json.load(file)
    return []  

def saveLibrary(library):
    with open(fileData, 'w') as file:
        json.dump(library, file)

def addBook(library, title, author, year, genre, read):
    newBook = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    library.append(newBook)
    saveLibrary(library)
    st.balloons()
    st.success(f'Book "{title}" added successfully!')

def removeBook(library, title):
    initialLength = len(library)
    library = [book for book in library if book['title'].lower() != title.lower()]
    if len(library) < initialLength:
        saveLibrary(library)
        st.success(f"Book \"{title}\" removed successfully.")
    else:
        st.warning(f"Book \"{title}\" not found in the library.")
    return library

def searchBook(library, searchingBook, searchingTerm):
    result = [book for book in library if searchingTerm.lower() in book[searchingBook].lower()]
    return result

def display_all_books(library):
    if library:
        for book in library:
            status = 'Read' if book['read'] else 'Unread'
            st.markdown(f"""
                <div class="fadeIn">
                    <p><b>{book['title']}</b> by <b>{book['author']}</b> - <b>{book['year']}</b> - <b>{book['genre']}</b> - <b>{status}</b></p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("The library is empty.")

def display_statistics(library):
    total_books = len(library)
    read_book = len([book for book in library if book['read']])
    percentage_read = (read_book / total_books) * 100 if total_books > 0 else 0
    st.write(f"**Total books:** {total_books}")
    st.write(f"**Percentage read:** {percentage_read:.2f}%")

def main():
    library = loadingLibrary()

    # Streamlit UI setup
    st.markdown('<h1 class="responsive-heading">📚 Library Management System</h1>', unsafe_allow_html=True)

    menu = ["Add Book", "Remove Book", "Search for Book", "Display All Books", "Statistics", "Exit"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add Book":
        st.subheader("Add a new book")
        title = st.text_input('Title')
        author = st.text_input('Author')
        year = st.text_input('Publication Year')
        genre = st.text_input('Genre')
        read = st.radio('Has the book been read?', ('Yes', 'No'), index=1)

        if st.button("Add Book"):
            with st.spinner('Adding book...'):
                time.sleep(1)  # Simulate loading
                addBook(library, title, author, year, genre, read == 'Yes')

    elif choice == "Remove Book":
        st.subheader("Remove a book")
        title = st.text_input('Enter the title of the book to remove')

        if st.button("Remove Book"):
            with st.spinner('Removing book...'):
                time.sleep(1)  # Simulate loading
                library = removeBook(library, title)

    elif choice == "Search for Book":
        st.subheader("Search for a book")
        searchingBook = st.radio("Search by", ["title", "author"])
        searchingTerm = st.text_input(f"Enter the {searchingBook}")

        if st.button("Search"):
            with st.spinner('Searching...'):
                time.sleep(1)  # Simulate loading
                result = searchBook(library, searchingBook, searchingTerm)
                if result:
                    for book in result:
                        status = "Read" if book['read'] else 'Unread'
                        st.markdown(f"""
                            <div class="fadeIn">
                                <p><b>{book['title']}</b> by <b>{book['author']}</b> - <b>{book['year']}</b> - <b>{book['genre']}</b> - <b>{status}</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No books found with the term '{searchingTerm}' in the {searchingBook} field.")

    elif choice == "Display All Books":
        st.subheader("All Books")
        display_all_books(library)

    elif choice == "Statistics":
        st.subheader("Library Statistics")
        display_statistics(library)

    elif choice == "Exit":
        st.write("Goodbye!")

if __name__ == '__main__':
    main()
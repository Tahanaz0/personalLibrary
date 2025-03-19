import streamlit as st
import json
import os


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
            st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        st.write("The library is empty.")

def display_statistics(library):
    total_books = len(library)
    read_book = len([book for book in library if book['read']])
    percentage_read = (read_book / total_books) * 100 if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

def main():
    library = loadingLibrary()

    # Streamlit UI setup
    st.title('Library Management System')

    menu = ["Add Book", "Remove Book", "Search for Book", "Display All Books", "Statistics", "Exit"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add Book":
        st.subheader("Add a new book")
        title = st.text_input('Enter the title of the book')
        author = st.text_input('Enter the author of the book')
        year = st.text_input('Enter the publication year of the book')
        genre = st.text_input('Enter the genre of the book')
        read = st.radio('Has the book been read?', ('Yes', 'No'))

        if st.button("Add Book"):
            addBook(library, title, author, year, genre, read == 'Yes')

    elif choice == "Remove Book":
        st.subheader("Remove a book")
        title = st.text_input('Enter the title of the book to remove')

        if st.button("Remove Book"):
            library = removeBook(library, title)

    elif choice == "Search for Book":
        st.subheader("Search for a book")
        searchingBook = st.radio("Search by", ["title", "author"])
        searchingTerm = st.text_input(f"Enter the {searchingBook}")

        if st.button("Search"):
            result = searchBook(library, searchingBook, searchingTerm)
            if result:
                for book in result:
                    status = "Read" if book['read'] else 'Unread'
                    st.write(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
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

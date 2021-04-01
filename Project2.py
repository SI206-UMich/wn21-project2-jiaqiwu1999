from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
#I know we only need to include 1 author but I have already finished finding all authors, I hope this is still fine!


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    output = []
    with open(filename, 'r') as fopen:
        soup = BeautifulSoup(fopen, "html.parser")
        titles = soup.find_all('span', attrs={"itemprop":"name", "role":"heading", "aria-level":"4"})
        title_list = []
        for item in titles:
            if item.string != None:
                title_list.append(item.string.strip())
        author_list = []
        spans = soup.find_all("span", attrs={"itemprop":"author"})
        for span in spans:
            div = span.find("div", class_="authorName__container")
            names = div.find_all("span")
            #(Adaptation)
            author_name = ""
            if (len(names) == 2):
                author_name = names[0].text.strip() + names[1].text.strip()
            else:
                author_name = names[0].text.strip()
            author_list.append(author_name)
        for i in range(len(title_list)):
            tup = (title_list[i], author_list[i])
            output.append(tup)
    return output


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    base = "https://www.goodreads.com"

    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find("table", class_="tableList")
    output = []
    for item in table.find_all("a", class_="bookTitle"):
        link = item.get("href", None)
        if link != None:
            output.append(base + link)
    return output[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    req = requests.get(book_url)
    soup = BeautifulSoup(req.content, "html.parser")
    title = soup.find("h1", id="bookTitle")
    author_div = soup.find("div", class_="authorName__container")
    author_name = author_div.find("span")
    page = soup.find("span", attrs={"itemprop":"numberOfPages"})
    if page != None and title != None and author_name != None:
        reg = "([0-9]+).*"
        num = re.findall(reg, page.text)
        if len(num) != 0:
            return (title.text.strip(), author_name.text.strip(), int(num[0]))
        else:
            print("Page not found")
            return None
    else:
        print("Details missing")
        return None



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    output = []
    with open(filepath, 'r') as fopen:
        soup = BeautifulSoup(fopen, 'html.parser')
        categories = soup.find_all("div", class_="category clearFix")
        for cat in categories:
            category = cat.h4.text.strip()
            link = cat.a.get("href", None)
            title = cat.find("img", class_="category__winnerImage").get("alt", None)
            if link != None and title != None:
                tup = (category, title, link)
                output.append(tup)
    return output



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    fout = open(filename, 'w')
    csv_writer = csv.writer(fout)
    csv_writer.writerow(["Book title", "Author Name"])
    for tup in data:
        csv_writer.writerow([tup[0], tup[1]])
    fout.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles_output = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles_output), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(titles_output), list)
        # check that each item in the list is a tuple
        self.assertEqual(type(titles_output[0]), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles_output[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(titles_output[0][1], "J.K. Rowling")
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles_output[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(titles_output[-1][1], "J.K. Rowling")

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for each in TestCases.search_urls:
            self.assertEqual(type(each), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        reg = "https://www.goodreads.com/book/show.+"
        for each in TestCases.search_urls:
            self.assertTrue(re.search(reg, each))

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        # check that the number of book summaries is correct (10)
        summaries = []
        for link in TestCases.search_urls:
            current = get_book_summary(link)
            # check that each item in the list is a tuple
            self.assertEqual(type(current), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(current), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(current[0]), str)
            self.assertEqual(type(current[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(current[2]), int)
            summaries.append(current)
        # check that the first book in the search has 337 pages
        self.assertEqual(len(summaries), 10)
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best), 20)
            # assert each item in the list of best books is a tuple
        for each in best:
            self.assertEqual(type(each), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(each), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best[0], ("Fiction", "The Midnight Library", "https://www.goodreads.com/choiceawards/best-fiction-books-2020"))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best[-1], ("Picture Books", "Antiracist Baby", "https://www.goodreads.com/choiceawards/best-picture-books-2020"))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        result = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(result, "test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open("test.csv", 'r') as fhand:
            csv_reader = csv.reader(fhand)
            csv_lines = [r for r in csv_reader]
            # check that there are 21 lines in the csv
            self.assertEqual(len(csv_lines), 21)
            # check that the header row is correct
            self.assertEqual(csv_lines[0], ["Book title", "Author Name"])
            # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
            self.assertEqual(csv_lines[1], ["Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"])
            # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'
            self.assertEqual(csv_lines[-1], ["Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"])



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)






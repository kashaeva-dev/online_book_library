import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def render_website():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template('template.html')

    with open('tululu_books/books_details.json', 'r', encoding="utf8") as file:
        books_details = json.load(file)

    books_details_chuncked = list(chunked(books_details, 15))

    os.makedirs('pages', exist_ok=True)

    pages_count = len(books_details_chuncked)
    for index, books_details_chunck in enumerate(books_details_chuncked):
        rendered_page = template.render(
            books_details=books_details_chunck,
            pages_count=pages_count,
            current_page=index + 1,
        )
        with open(f'pages/index{index + 1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    render_website()

    server = Server()

    server.watch('/Users/nataly/Projects/online_book_library/tululu_books/', render_website)
    server.watch('/Users/nataly/Projects/online_book_library/template.html', render_website)
    server.serve(root='./pages', port=8080, host='127.0.0.1', default_filename='index1.html', )


if __name__ == '__main__':
    main()

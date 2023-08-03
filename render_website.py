import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def render_website():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template('tululu_books/template.html')

    with open('tululu_books/books_details.json', 'r', encoding="utf8") as file:
        books_details = json.load(file)

    rendered_page = template.render(
        books_details=books_details,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    render_website()

    server = Server()

    server.watch('/Users/nataly/Projects/online_book_library/tululu_books/', render_website)
    server.serve(root='index.html')


if __name__ == '__main__':
    main()

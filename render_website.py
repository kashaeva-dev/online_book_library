import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template('template.html')

    with open('books_details.json', 'r', encoding="utf8") as file:
        books_details = json.load(file)

    books_details_chuncked = list(chunked(books_details, 15))

    os.makedirs('pages', exist_ok=True)

    pages_count = len(books_details_chuncked)
    for index, books_details_chunck in enumerate(books_details_chuncked):
        rendered_page = template.render(
            books_details=books_details_chunck,
            pages_count=pages_count,
            current_page=index + 1,
            cwdir=os.getcwd(),
        )
        with open(f'pages/index{index + 1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    render_website()

    server = Server()

    books_path = os.path.join(os.getcwd(), 'tululu_books/')
    books_details_path = os.path.join(os.getcwd(), 'books_details.json')
    template_path = os.path.join(os.getcwd(), 'template.html')
    server.watch(books_path, render_website)
    server.watch(books_details_path, render_website)
    server.watch(template_path, render_website)
    server.serve(root='.', port=8080, host='127.0.0.1', default_filename='pages/index1.html', )


if __name__ == '__main__':
    main()

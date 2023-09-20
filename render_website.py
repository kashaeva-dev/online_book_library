import argparse
import json
import os
from functools import partial

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website(filepath):
    books_per_page = 16

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    with open(filepath, "r", encoding="utf8") as file:
        books_details = json.load(file)

    chuncked_books_details = list(chunked(books_details, books_per_page))

    os.makedirs("pages", exist_ok=True)

    pages_count = len(chuncked_books_details)
    for index, books_details_chunck in enumerate(chuncked_books_details, start=1):
        rendered_page = template.render(
            books_details=books_details_chunck,
            pages_count=pages_count,
            current_page=index,
            cwdir=os.getcwd(),
        )
        with open(f"pages/index{index}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Online book library",
    )
    parser.add_argument("filepath",
                        nargs="?",
                        help="You can spesify filepath to the books' data in json format",
                        default="books_details.json",
                        )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    render_website(args.filepath)

    render_website_partial = partial(render_website, args.filepath)

    server = Server()

    server.watch(os.path.join(os.getcwd(), "template.html"), render_website_partial)
    server.serve(root=".", port=8080, host="127.0.0.1", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()

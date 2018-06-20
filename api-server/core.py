from apistar import App, Route
from models import Link

def add_links(link: Link) -> dict:
    return {'Success': True}


routes = [
    Route('/add_link', method='POST', handler=add_links)
]


if __name__ == '__main__':
    app = App(routes=routes)
    app.serve('0.0.0.0', 5000, debug=True)
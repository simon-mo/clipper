from apistar import App, ASyncApp, Route
from apistar.exceptions import BadRequest
from models import Link, Application, Model


def link(l: Link):
    app = Application.get_all(l.app_name)
    models = {
        model_name: Model.get_all(model_name)
        for model_name in l.model_names
    }

    if app is None:
        raise BadRequest(f"No app with name '{l.app_name}' exists.")

    for name, model in models.items():
        if model == None:
            raise BadRequest(f"No model with name '{name}' exists.")

        if model.input_type != app.input_type:
            raise BadRequest(
                f"Model with name '{name}' has incompatible input_type '{model.input_type}'."
                 "Requested app to link has input_type '{app.input_type}'."
            )

    linked_models = Link.get_all(l.app_name)
    if linked_models is not None:
        raise BadRequest(f"Model with name '{linked_models[0]}' is already linked to '{app.name}'.")
        
    l.save()
    return f"Successfully linked model with name '{l.model_names[0]}' to application '{l.app_name}'"


routes = [Route('/link', method='POST', handler=link)]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
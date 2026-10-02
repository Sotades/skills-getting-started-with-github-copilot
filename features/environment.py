from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app


def before_scenario(context, scenario):
    context.original_activities = deepcopy(activities)
    context.client_context = TestClient(app)
    context.client = context.client_context.__enter__()


def after_scenario(context, scenario):
    try:
        context.client_context.__exit__(None, None, None)
    finally:
        activities.clear()
        activities.update(context.original_activities)
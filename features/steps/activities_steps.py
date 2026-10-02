from urllib.parse import quote

from behave import given, then, when

from src.app import activities


@given('the activity "{activity_name}" exists')
def step_activity_exists(context, activity_name):
    assert activity_name in activities


@given('student "{email}" is registered for "{activity_name}"')
def step_student_is_registered(context, email, activity_name):
    response = context.client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )
    assert response.status_code == 200, response.text


@when("I request the available activities")
def step_request_activities(context):
    context.response = context.client.get("/activities")


@when('student "{email}" signs up for "{activity_name}"')
def step_student_signs_up(context, email, activity_name):
    context.response = context.client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )


@when('student "{email}" unregisters from "{activity_name}"')
def step_student_unregisters(context, email, activity_name):
    context.response = context.client.delete(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )


@then("the response status is {status:d}")
def step_response_status(context, status):
    assert context.response.status_code == status, context.response.text


@then('the activities include "{activity_name}"')
def step_activities_include(context, activity_name):
    assert activity_name in context.response.json()


@then('the response message is "{message}"')
def step_response_message(context, message):
    assert context.response.json()["message"] == message


@then('the error detail is "{detail}"')
def step_error_detail(context, detail):
    assert context.response.json()["detail"] == detail


@then('student "{email}" is registered once for "{activity_name}"')
def step_student_is_registered_once(context, email, activity_name):
    assert activities[activity_name]["participants"].count(email) == 1


@then('student "{email}" is not registered for "{activity_name}"')
def step_student_is_not_registered(context, email, activity_name):
    assert email not in activities[activity_name]["participants"]
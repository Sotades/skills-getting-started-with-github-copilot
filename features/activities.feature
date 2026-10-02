Feature: Activity registrations
  Students can view activities and manage their registrations.

  Scenario: View available activities
    When I request the available activities
    Then the response status is 200
    And the activities include "Chess Club"

  Scenario: Register for an activity
    Given the activity "Chess Club" exists
    When student "bdd-student@example.com" signs up for "Chess Club"
    Then the response status is 200
    And the response message is "Signed up bdd-student@example.com for Chess Club"
    And student "bdd-student@example.com" is registered once for "Chess Club"

  Scenario: Reject duplicate registration
    Given student "bdd-student@example.com" is registered for "Chess Club"
    When student "bdd-student@example.com" signs up for "Chess Club"
    Then the response status is 400
    And the error detail is "Student already signed up for this activity"
    And student "bdd-student@example.com" is registered once for "Chess Club"

  Scenario: Reject registration for an unknown activity
    When student "bdd-student@example.com" signs up for "Unknown Activity"
    Then the response status is 404
    And the error detail is "Activity not found"

  Scenario: Unregister from an activity
    Given student "bdd-student@example.com" is registered for "Chess Club"
    When student "bdd-student@example.com" unregisters from "Chess Club"
    Then the response status is 200
    And the response message is "Removed bdd-student@example.com from Chess Club"
    And student "bdd-student@example.com" is not registered for "Chess Club"

  Scenario: Reject unregistering from an unknown activity
    When student "bdd-student@example.com" unregisters from "Unknown Activity"
    Then the response status is 404
    And the error detail is "Activity not found"

  Scenario: Reject unregistering a student who is not registered
    Given the activity "Chess Club" exists
    When student "bdd-student@example.com" unregisters from "Chess Club"
    Then the response status is 404
    And the error detail is "Student is not signed up for this activity"
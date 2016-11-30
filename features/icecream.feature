Feature: The icecream service back-end
    As an icecream lover
    I need a RESTful catalog service
    So that I can keep track of all my icecream flavors

Background:

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Ice-cream REST API"
    Then I should not see "404 Not Found"

Scenario: List all icecreams
    Given the following icecreams
        | name          | id  |
        | vanilla       | 4   |
        | chocolate     | 6   |
        | strawberry    | 7  |
    When I visit '/ice-cream'
    Then I should see 'vanilla'
    And I should see 'chocolate'
    And I should see 'strawberry'

    Scenario: Action on the ice-cream
      Given I want to melt or freeze an icecream
      When I append melt at the end of the url
      Then I should have 'melted'
      And I should have melted 'Vanilla'
      When I append freeze at the end of the url
      Then I should have 'frozen'
      And I should have frozen 'Vanilla'

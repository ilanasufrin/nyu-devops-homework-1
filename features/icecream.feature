Feature: The icecream service back-end
    As an icecream lover
    I need a RESTful catalog service
    So that I can keep track of all my icecream flavors

Background:

Scenario: The server is running
    When I visit the "home page"
    Then I should not see "404 Not Found"

Scenario: List all icecream
    Given the following icecream
        | name          | id  |
        | Vanilla       | 4   |
        | Chocolate     | 6   |
        | Strawberry    | 7   |
    When I visit '/ice-cream'
    Then I should see 'Vanilla'
    And I should see 'Chocolate'
    And I should see 'Strawberry'

Scenario: Get an icecream
    Given the following icecream
        | name          | id  |
        | Vanilla       | 4   |
    When I visit '/ice-cream/4'
    Then I should see 'Vanilla'

Scenario: Create an icecream
    Given the following icecream
        | name          | id  |
        | Vanilla       | 4   |
        | Chocolate     | 6   |
        | Strawberry    | 7   |
    When I visit '/ice-cream'
    Then I should not see 'Pistachio'
    When I create '/ice-cream'
        | name          | id  | description     | status  | base    | price   | popularity  |
        | Pistachio     | 10  | Made from Nuts  | melted  | milk    | $1.00   | 1/5         |
    And I visit '/ice-cream/10'
    Then I should see 'Pistachio'


Scenario: Delete an icecream
  Given the following icecream
        | name          | id  |
        | Strawberry    | 7   |
  When I visit '/ice-cream/7'
  Then I should see 'Strawberry'
  When I delete '/ice-cream/7'
  And I visit '/ice-cream'
  Then I should not see 'Strawberry'

Scenario: Update an icecream
  Given the following icecream
      | name          | id  |
      | Chocolate     | 6   |
  When I visit '/ice-cream/6'
  Then I should see 'Chocolate'
  When I update '/ice-cream/6'
      | name          | id  | description     | status  | base    | price   | popularity  |
      | Mango         | 6   | Made from fruit | frozen  | sorbet  | $15.00  | 5/5         |
  And I visit '/ice-cream/6'
  Then I should see 'Mango'








Scenario: Action on the ice-cream
  Given I want to melt or freeze an icecream
  When I append melt at the end of the url
  Then I should have 'melted'
  And I should have melted 'Vanilla'
  When I append freeze at the end of the url
  Then I should have 'frozen'
  And I should have frozen 'Vanilla'

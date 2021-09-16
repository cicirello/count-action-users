# count-action-users

[![count-action-users](.github/preview/count-action-users640.png)](#count-action-users)

Check out all of our GitHub Actions: https://actions.cicirello.org/

## About

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/count-action-users?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/count-action-users)
[![build](https://github.com/cicirello/count-action-users/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/build.yml)
[![samples](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml)
[![CodeQL](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/github/license/cicirello/count-action-users)](https://github.com/cicirello/count-action-users/blob/main/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/cicirello/count-action-users)](https://github.com/cicirello/count-action-users)

The [cicirello/count-action-users](https://github.com/cicirello/count-action-users) GitHub Action 
generates a [Shields endpoint](https://shields.io/endpoint) with the count of the number of 
workflows that use a GitHub Action. It is thus a tool for
maintainers of GitHub Actions, and it can be used to insert a badge with a users count into the
README for a GitHub Action. The key features include:
* __Designed to Run on a Schedule__: The intended usage is to run the action on a 
  schedule (e.g., nightly) to update the endpoint. 
* __Customizable__: It is configurable in a number of ways (e.g., badge color, logo, style)
  using action inputs, but you can also override these things when you embed the badge using 
  Shield's URL parameters.
* __Multiple Action Support__: For those who maintain multiple GitHub Actions, the `count-action-users`
  action accepts a list of GitHub Actions as an input, generating endpoints for all actions 
  in the list. In this way, a single run of the action in a single workflow in a single repository
  is sufficient to regularly monitor the number of users of all of the actions that you maintain.
  Or, if you prefer, you can run the action separately within the repositories of each action.

_The developers of the `count-action-users` GitHub Action are not affiliated 
with the developers of Shields, although like most of GitHub we use their badges
in most of our repositories._

__Here are a Few Example Badges__
* Example with moderate number of users: 
  ![Count of Action Users](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcicirello%2Fcount-action-users%2Fsamples%2Fendpoints%2Fjacoco-badge-generator.json)
* Example with very large number of users (`actions/setup-python`): 
  ![Count of Action Users](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcicirello%2Fcount-action-users%2Fsamples%2Fendpoints%2Fsetup-python.json)
* Example with huge number of users (`actions/checkout`): 
  ![Count of Action Users](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcicirello%2Fcount-action-users%2Fsamples%2Fendpoints%2Fcheckout.json)


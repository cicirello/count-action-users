# count-action-users

Check out all of our GitHub Actions: https://actions.cicirello.org/

## About

<!--- COMMENT FOR NOW

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/count-action-users?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/count-action-users)
[![build](https://github.com/cicirello/count-action-users/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/build.yml)
[![samples](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml)
[![CodeQL](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/github/license/cicirello/count-action-users)](https://github.com/cicirello/count-action-users/blob/main/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/cicirello/count-action-users)](https://github.com/cicirello/count-action-users)

-->

The [cicirello/count-action-users](https://github.com/cicirello/count-action-users) GitHub Action 
generates a [Shields endpoint](https://shields.io/endpoint) with the number of 
users of a GitHub Action. It is thus a tool for
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

__Why not instead submit a pull request to Shields to add direct support to their 
awesome project for an actions users count badge?__ The GitHub Code Search API, which 
we utilize for this action, has a rate limit of 30 queries per minute for an 
authenticated user. By running this as an action, the necessary queries benefit 
from the GITHUB_TOKEN of the user of this action, and in theory the rate limit should 
never come into effect unless you attempt to run
it to generate endpoints for more than 30 actions within a single workflow run, or are 
otherwise querying the code search API at the same time with another tool. I imagine the rate
limit would be significantly more challenging for a solution directly integrated with 
Shields.

__How does `count-action-users` work?__ The `count-action-users` action queries GitHub's
Code Search API. The search is restricted to the contents of files in the `.github/workflows`
directory (since active workflows must be in that directory to run) and restricted to 
the YAML language (the language for workflows). The search terms then include
the owner of the action and the name of the action. It is possible that some false positives
may be included in the count. For example, although GitHub requires actions in the marketplace to
have unique names, if an action has a simple enough name, that name may be found within that
of another action with a longer name. Including the owner name in the search should
minimize false positives. See the documentation of 
GitHub's [code search](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-code)
for details of what code is (and is not) indexed by GitHub.

## Table of Contents

The remainder of the documentation is organized as follows:
* [Example Workflows](#example-workflows): Several example workflows illustrating 
  usage of the action.
* [Inputs](#inputs): Documentation of the action's inputs.
* [Outputs](#outputs): Documentation of the action's outputs.
* [All Possible Action Inputs](#all-possible-action-inputs): A workflow showing all
  of the action's inputs with their default values.
* [Support the Project](#support-the-project): The various ways that you can support
  the project.
* [License](#license): License information (MIT License).

## Example Workflows

### Example 1: Monitoring one action, storing endpoint at root of repository

This first workflow runs on a schedule (daily at 4am), and it can also
be run manually if need be (via the `workflow_dispatch` event). It uses all
of the default action inputs. The default location for the generated endpoint
is the root of the repository. In this example, there is a single action that
we are monitoring: `owner/action-name`. The action names the endpoint file using
the name of the action, so in this case, the name of the file it creates is:
`action-name.json`. Please note that the `GITHUB_TOKEN` must be passed as an
environment variable, as shown in the workflow, to authenticate to the GitHub API.

```yml
name: count-action-users

on:
  schedule:
    - cron: '0 4 * * *'
  workflow_dispatch:

jobs:
  count:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2

    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: owner/action-name 
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

### Example 2: Monitoring multiple actions, serving via GitHub Pages from the docs directory

### Example 3: Serving endpoints via GitHub Pages from the gh-pages branch


### Protected branches with required checks


## Inputs

Most of the inputs have default values that should be sufficient in most
cases. Only the `action-list` input is required.

### `action-list` (REQUIRED)

This input is required. All other inputs are optional.
This input is a comma or space separated list of the GitHub Actions for
which you want user count endpoints generated. We recommend that you 
include both owner name and action name, rather than just the action name,
to improve accuracy of results. For example, if I was running this
for this very action, I would set this input as follows: 

```yml
    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: cicirello/count-action-users
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The action will also work if you only use the action name (e.g., `action-list: count-action-users`), 
but the results may be less accurate. Although GitHub requires each action to have a 
unique name, if the name of your action is relatively simple, then there may be other
action names that include your action's name within. By including the owner name
of the action in the search, you can minimize some false positives in the results.

If you maintain several GitHub Actions, then we recommend that you utilize
a YAML multiline string when specifying this input to make your workflow 
easy to read. For example:

```yml
    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: >
          owner/action-one
          owner/action-two
          owner/action-three
          owner/action-four
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The `>` in the above is one of YAML's ways of specifying a multiline string.
The action also doesn't care who the owners of the actions are, and will work if
different actions have different owners, such as with the following:

```yml
    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: >
          owner/action-one
          anotherOwner/action-two
          somebodyElse/action-three
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The filename of each endpoint is of the form: `action-name.json`.

### `target-directory`

This is the directory, relative to the root of the repository in which
the action is run, where the JSON endpoints will be stored. It defaults to
the root of the repository. If the target directory doesn't exist, then the
action will create it.

### `color`

This is the color for the right side of the badge (the side with the count
of action users). The default is a shade of green. You can pass 3-digit hex
(e.g., `color: '#333'`), 6-digit hex (e.g., `color: '#343434'`), or named
colors (e.g., `blue`). Anything that is valid in CSS, SVG, etc is valid
for this input. However, the action does not do any validation of the color that 
you pass. Note that the quotes are required if you use hex because the `#` is 
a special character to YAML.

### `include-logo`

This input controls whether or not a logo is inserted in the badge. The default is
`true`.

### `named-logo`

This controls which logo is inserted if a logo is included in the badge. The default is
`actions`, which is the GitHub Actions logo. Another to consider 
is `github`, which is the GitHub logo. You can pass the name of any logo supported
by [Shields](https://github.com/badges/shields), which also includes 
[simple-icons](https://github.com/simple-icons/simple-icons). 

### `style`

This controls the style of the badge, and can be any style that is supported by 
[Shields](https://github.com/badges/shields). The default is `flat`, which happens to
also be the Shields default.

### `fail-on-error`

This input enables you to control what happens if the
action fails for some reason (e.g., error communicating
with the GitHub's Code Search API, etc). 

The default is `fail-on-error: true`, which means that if
an error occurs it will cause the workflow to fail. The rationale
for this default is that the failed workflow will lead to a
GitHub notification so that you know something went wrong.
If you'd rather just let it quietly fail, to most likely correct
itself during the next run, then pass `fail-on-error: false`
(actually anything other than `true` will be treated as `false`).

### `commit-and-push`

The `commit-and-push` input controls whether the action commits
and pushes the generated JSON endpoints upon creation. It defaults to
`commit-and-push: true`. If the user count changed since
last commit, then as long as you are not running this in a detached
head state (such as on a pull request event), the action will commit
and push the new endpoint. If you are in a detached head
state, such as if you were to run this during a pull request 
(not sure why you would), then the action will simply and quietly
skip the commit/push without issuing an error. 

If your branch is protected with either required reviews or required
checks, then the push will fail with an error. Whether this also
fails your workflow depends on how you have set 
the `fail-on-error` input. See the earlier discussion for what you 
can do if you wish to use the action in a repository 
that has required reviews or required checks:
[Protected branches with required checks](#protected-branches-with-required-checks).

The author of the commit is set to the github-actions bot.

## Outputs

The action has only the following action output variable.

### `exit-code`

If the input `fail-on-error` is set to `false`, then in addition to
quietly failing (i.e., not failing the workflow run), the output `exit-code`
will be set to a non-zero exit code that may be useful in debugging the
issue. If the input `fail-on-error` is set to `true` (the default), your
workflow run won't have the opportunity to check the `exit-code` output.
However, the `exit-code` and a descriptive error message will still be
logged in the workflow output. In either case, if you believe that the
failure is a bug, please include this in any bug reports.

## All Possible Action Inputs

The workflow here shows all possible inputs, with their default
values, and also shows how to access the action's `exit-code`
output if desired.

```yml
name: count-action-users

on:
  schedule:
    - cron: '0 4 * * *'
  workflow_dispatch:

jobs:
  count:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2

    - name: Generate user count JSON endpoint
      id: endpointStep # Only needed if you want to check the exit-code
      uses: cicirello/count-action-users@v1
      with:
        action-list: owner/action # This input is REQUIRED.
        target-directory: '' # Default is root of repository.
        color: '#4c1' # A bright shade of green
        include-logo: true
        named-logo: actions # Defaults to the GitHub Actions logo
        style: flat # Which is Shields's default as well
        fail-on-error: true
        commit-and-push: true
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}

    - name: Check exit code if desired
      run: |
        # Note that if you set fail-on-error to true, you'll
        # never actually get here if an error occurs. But if you
        # set fail-on-error to false, then instead of failing the
        # workflow, the action will output the exit code that would
        # have failed the workflow and you can check it here.
        echo "exitCode = ${{ steps.endpointStep.outputs.exit-code }}"
```

## Support the Project

You can support the project in a number of ways:
* __Starring__: If you find the `count-action-users` action useful, consider starring the
  repository.
* __Sharing with Others__: Consider sharing it with others who you feel might find it useful.
* __Reporting Issues__: If you find a bug or have a suggestion for a new feature, please 
  report it via the [Issue tracker](https://github.com/cicirello/count-action-users/issues).
* __Contributing Code__: If there is an open issue that you think you can help with, submit a pull request.
* __Sponsoring__: You can also consider 
  [becoming a sponsor](https://github.com/sponsors/cicirello).

## License

This GitHub action is licensed under the [MIT License](LICENSE.md). If you contribute
to the project, you agree that your contributions are likewise licensed through
the MIT License. 

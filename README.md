# count-action-users

[![count-action-users](https://actions.cicirello.org/images/count-action-users640.png)](#count-action-users)

Check out all of our GitHub Actions: https://actions.cicirello.org/

## About

| __GitHub Actions__ | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/count-action-users?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/count-action-users) |
| :--- | :--- |
| __Build Status__ | [![build](https://github.com/cicirello/count-action-users/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/build.yml) [![samples](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/generate-samples.yml) [![CodeQL](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cicirello/count-action-users/actions/workflows/codeql-analysis.yml) |
| __Source Info__ | [![License](https://img.shields.io/github/license/cicirello/count-action-users)](https://github.com/cicirello/count-action-users/blob/main/LICENSE) [![GitHub top language](https://img.shields.io/github/languages/top/cicirello/count-action-users)](https://github.com/cicirello/count-action-users) |
| __Support__ | [![GitHub Sponsors](https://img.shields.io/badge/sponsor-30363D?logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/cicirello) [![Liberapay](https://img.shields.io/badge/Liberapay-F6C915?logo=liberapay&logoColor=black)](https://liberapay.com/cicirello) [![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?logo=ko-fi&logoColor=white)](https://ko-fi.com/cicirello) |

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
* Example with very large number of users `actions/setup-python`: 
  ![Count of Action Users](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcicirello%2Fcount-action-users%2Fsamples%2Fendpoints%2Fsetup-python.json)
* Example with huge number of users `actions/checkout`: 
  ![Count of Action Users](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcicirello%2Fcount-action-users%2Fsamples%2Fendpoints%2Fcheckout.json)

## Table of Contents

The remainder of the documentation is organized as follows:
* [Example Workflows](#example-workflows): Several example workflows illustrating 
  usage of the action.
* [FAQ](#faq): List of questions we anticipate you may have, or which have been asked.
* [Inputs](#inputs): Documentation of the action's inputs.
* [Outputs](#outputs): Documentation of the action's outputs.
* [All Possible Action Inputs](#all-possible-action-inputs): A workflow showing all
  of the action's inputs with their default values.
* [Support the Project](#support-the-project): The various ways that you can support
  the project.
* [License](#license): License information (MIT License).

## Example Workflows

### Example 1: Storing endpoint at root of repository

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

You can then pass the URL of the endpoint to Shields to generate and
insert a badge into your README with the following Markdown. Just be sure to
replace `OWNERUSERID`, `REPOSITORY`, and `BRANCH` as appropriate.

```markdown
![Count of Action Users](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/OWNERUSERID/REPOSITORY/BRANCH/action-name.json)
```

Note that in the above, you are relying on GitHub's `raw.githubusercontent.com`
server for serving the endpoint to Shields. We do not actually recommend doing this
as that server isn't really intended for that purpose, and may create a delay
that will trickle down to Shields serving the badge. However, you might initially
set it up this way to try out the action. 
See [Example 2](#example-2-serving-via-github-pages-from-the-docs-directory) 
and [Example 3](#example-3-serving-via-github-pages-from-the-gh-pages-branch) 
for examples of our recommended approach, serving via GitHub Pages.

See [later in this document](#how-to-link-the-badge-to-search-results) for an 
example of the markdown needed to link the badge to a GitHub search results page
with the workflows represented by the user count. 

If you maintain more than one GitHub Action and want to generate
user count endpoints for all of them with a single application
of this action, then you can pass a list of your GitHub actions
as follows:

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
        action-list: >
          owner/action-one
          owner/action-two
          owner/action-three  
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The above example will generate the following JSON files:
`action-one.json`, `action-two.json`, and `action-three.json`.
Note that the `>` is one of the ways to specify a multiline string
in YAML.

### Example 2: Serving via GitHub Pages from the docs directory

The previous example relies on GitHub's `raw.githubusercontent.com`
server for serving the endpoint to Shields. This is less than ideal
as that server is intended for those browsing GitHub to see the
raw version of files, and isn't really intended for general serving
of files.

__GitHub Pages (our recommended approach)__: We instead recommend utilizing
GitHub Pages. The benefit of this is that you will gain the advantage of the 
CDN that backs GitHub Pages, thus significantly 
enhancing the speed of serving the endpoint to Shields. 
First note that you do not necessarily need to setup a full
website for this purpose. You can literally use it to serve nothing but
your user count JSON endpoint, if you don't want to otherwise set up a full project
page. Follow GitHub's directions for enabling [GitHub Pages](https://pages.github.com/)
on the repository in which you want to use the `count-action-users` action.

To do this, go to the settings tab of that repository, and then select "Pages" in the
left. In this example, we are assuming serving from the "docs" directory of your
default branch, so make those selections as you enable "Pages" for your repository.
Once you do, anything you store in the "docs" directory will be served
from the URL: `https://YOURUSERID.github.io/REPOSITORY/`.

So, now run the action using this workflow:

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
        target-directory: docs
        action-list: owner/action-name 
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

Note that the above workflow uses the 
`target-directory` input to store the endpoint in the docs directory,
which will be created by the action if it doesn't already exist.
Assuming that you have configured GitHub Pages to serve from "docs",
then your endpoint will be accessible from 
`https://YOURUSERID.github.io/REPOSITORY/action-name.json`.

You can then use the following Markdown to insert the badge in your README.
Just be sure to replace `YOURUSERID` and `REPOSITORY` as appropriate.

```markdown
![Count of Action Users](https://img.shields.io/endpoint?url=https://YOURUSERID.github.io/REPOSITORY/action-name.json)
```

If you are also utilizing GitHub Pages for a project site, then you might want
to store the endpoint in a subdirectory of "docs" to keep your site's files organized.
For example, perhaps you want to store it in a directory "endpoints", then you can
accomplish that with the following action input: `target-directory: docs/endpoints`.
This would change the necessary Markdown for inserting the badge to:

```markdown
![Count of Action Users](https://img.shields.io/endpoint?url=https://YOURUSERID.github.io/REPOSITORY/endpoints/action-name.json)
```

See [later in this document](#how-to-link-the-badge-to-search-results) for an 
example of the markdown needed to link the badge to a GitHub search results page
with the workflows represented by the user count.

### Example 3: Serving via GitHub Pages from the gh-pages branch

GitHub Pages allows you to serve your site from either the "docs" directory
(as in the above example), or from the root of any branch. Assuming you are
setting this up in the repository of the action that you maintain, then the
default branch is not a good choice for your project site. Instead, create 
a `gh-pages` branch in your repository (you can then delete everything in the
`gh-pages` branch, as it only needs to contain the source of your project site).
Just like Example 2 above, you don't really need to have a project site, as your
site can literally be just the endpoint you want to pass to Shields.

Now, setup the following workflow in the default branch (e.g., "main") 
of your repository. Note that even though this workflow will be pushing to the `gh-pages` branch,
the workflow itself must be in the default branch, or else the schedule will not run.

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
      with:
        ref: gh-pages

    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: owner/action-name 
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

You'll notice above that the `count-action-users` step
did not change. Instead, the `checkout` step changed to
checkout the `gh-pages` branch of the repository. The
`count-action-users` action commits and pushes to the
checked out branch.

As in the previous example, the JSON endpoint will be at 
the root of the project site 
(`https://YOURUSERID.github.io/REPOSITORY/action-name.json`). Thus, you can then use the 
following Markdown to insert the badge in your README.
Just be sure to replace `YOURUSERID` and `REPOSITORY` as appropriate.

```markdown
![Count of Action Users](https://img.shields.io/endpoint?url=https://YOURUSERID.github.io/REPOSITORY/action-name.json)
```

If you'd rather have it in a subdirectory, you can set the appropriate action input,
such as with: `target-directory: endpoints`. Doing so would then require
the following Markdown for inserting the badge into the README:  

```markdown
![Count of Action Users](https://img.shields.io/endpoint?url=https://YOURUSERID.github.io/REPOSITORY/endpoints/action-name.json)
```

See [later in this document](#how-to-link-the-badge-to-search-results) for an 
example of the markdown needed to link the badge to a GitHub search results page
with the workflows represented by the user count.

### Protected branches with required checks

The default permissions of the `GITHUB_TOKEN` are sufficient for pushing 
to a protected branch, provided that the branch protection hasn't been 
configured with required reviews nor with required checks. If the repository where
you are running the `count-action-users` action does have a branch protection 
rule with required reviews or required checks, there are a couple solutions.

__Not Recommended__: First, you could create a personal access token (PAT) 
with necessary permissions, save it as a repository secret, and use the PAT 
with during the actions/checkout step 
(see [actions/checkout](https://github.com/actions/checkout)'s documentation). 
However, we do not recommend doing so. If anyone else has write access to the 
repository, then they can potentially create additional workflows using that PAT
to bypass the required checks and/or reviews; and you obviously had a reason for
putting those requirements in place.

__Recommended__: Although your default branch likely has branch protection rules
that include required checks and/or reviews, you do not need to store your
user count endpoint in the default branch.
See [Example 3](#example-3-serving-via-github-pages-from-the-gh-pages-branch)
earlier, which uses the `gh-pages` branch along with GitHub Pages to serve the
endpoint to Shields. You can configure branch protection on the `gh-pages`
branch, and as long as you don't add any required checks or reviews for that
specific branch, the action will be able to push to it without the need for a PAT.

### Specific version vs major release

All of the above examples used the major release tag
for the `count-action-users` step 
(i.e., `uses: cicirello/count-action-users@v1`):

```yml
    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1
      with:
        action-list: owner/action-name 
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The advantage to this is that you will automatically
get all non-breaking changes and bug fixes without the
need to alter your workflow. If you prefer to 
use a specific release, just use the SemVer of the
release that you wish to use, such as with the following:

```yml
    - name: Generate user count JSON endpoint
      uses: cicirello/count-action-users@v1.0.2
      with:
        action-list: owner/action-name 
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

If you do use a specific release, then we recommend
configuring [GitHub's Dependabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/)
in your repository.  Dependabot can be used to monitor dependencies,
including GitHub Actions, and generates automated pull requests to update
versions. The PRs it generates includes the text of release notes and ChangeLogs
giving you the opportunity to decide whether to upgrade the version.

### How to Link the Badge to Search Results

It is common practice to link status badges to something relevant
(e.g., a build status badge to workflow runs). For a users count badge,
you might consider linking it to a GitHub search results page. You can do that
with the following Markdown. Replace "YOURUSERID" with the user id of the owner
of the action, and replace "ACTIONNAME" with the name of the action. Also replace
"RELEVANT_SHIELDS_URL" with the link that generates the badge from the endpoint
(see the examples in the workflow examples above).

```markdown
[![Count of Action Users](RELEVANT_SHIELDS_URL)](https://github.com/search?q=YOURUSERID+ACTIONNAME+path:.github/workflows+language:YAML&type=Code)
```

## FAQ

__Why not instead submit a pull request to Shields to add direct support to their 
awesome project for an actions users count badge?__ The GitHub Code Search API, which 
we utilize for this action, has a rate limit of 30 queries per minute for an 
authenticated user; and can also potentially interact with other secondary rate limits,
including some secondary limits that are not published. 
By running this as an action, the necessary queries benefit 
from the GITHUB_TOKEN of the user of this action, and in theory we can more easily
stay within the rate limits. I imagine the rate
limit would be significantly more challenging for a solution directly integrated with 
Shields. We additionally have a built-in time delay in between queries for those using
the action to monitor multiple GitHub actions.

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

__Can't we further minimize false positives with "owner/action-name" as a single search 
term?__ Unfortunately, GitHub's code search drops various special characters that are often
used as wildcards from searches, including `/`, replacing them with 
spaces. Due to this, combining owner and the 
action's name into a single search 
term in this way is equivalent to the search we are currently doing.

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
of action users). The default is the shade of blue that is currently
used by Shields to designate that the badge is "informational". You can pass 3-digit hex
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
`githubactions`, which is the GitHub Actions logo. Another to consider 
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

### `query-delay`

This input specifies a delay, in seconds, in between queries for 
cases where multiple actions are being monitored. The purpose of this
delay is to decrease chance of hitting API rate limits. The default is
65 seconds, which ensures that no more than one code search query is
executed per minute. This input doesn't accept values less than 33. For example,
if you attempt to pass 0 (or anything else less than 33), the minimum of
33 will be used instead. That minimum ensures that at most two code search queries
will be executed per minute.

Why is the default, and minimum, query delays so high? Although the rate limit
is 30 code search queries per minute, there are other unpublished secondary rate 
limits. During our initial testing, we occasionally ran into such secondary limits
when using a lower query delay that allowed for four queries in a 
minute, specifically on the fourth query. It is unclear what other activity 
was interacting to hit those secondary rate limits. The default, and minimum,
query delays are designed to help you avoid rate limit effects.

Additionally, there is no reason for the action to collect usage statistics
of the actions that you maintain more than once per day, so the length of the delay 
between queries shouldn't really matter much to you. The one case where it might is
if you have reason to run this in a private repository, and thus the delay time
will count against your actions minutes. In that case you can simply setup one workflow
per action that you maintain (thus no delay will be inserted), and make sure
you schedule them so that they are far enough apart in time.

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
        color: '#007ec6' # The shade of blue used by Shields for informational badges
        include-logo: true
        named-logo: githubactions # Defaults to the GitHub Actions logo
        style: flat # Which is Shields's default as well
        fail-on-error: true
        commit-and-push: true
        query-delay: 65
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
* __Sponsoring__: You can also consider [becoming a sponsor](https://github.com/sponsors/cicirello).

## License

This GitHub Action is licensed under the [MIT License](https://github.com/cicirello/count-action-users/blob/main/LICENSE).

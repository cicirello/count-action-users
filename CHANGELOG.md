# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2023-12-08

### Added
  
### Changed

### Deprecated

### Removed

### Fixed

### CI/CD

### Dependencies
* Bump cicirello/pyaction from 4.25.0 to 4.27.0


## [1.0.7] - 2023-10-05

### CI/CD
* Bump Python to 3.12 in CI/CD workflows when running unit tests.

### Dependencies
* Bump cicirello/pyaction from 4.10.0 to 4.25.0, including upgrading Python within the Docker container to 3.12.


## [1.0.6] - 2022-10-20

### Fixed
* Replaced the usage of GitHub Action's deprecated `set-output` workflow command with the new `$GITHUB_OUTPUT` environment file.
* Disabled pycache to protect against potential future bug. Currently no imports so no pycache created, but if future versions import local py modules, a pycache would be created during run in repo. Disabled creation of pycache now to avoid.

### Dependencies
* Bump cicirello/pyaction from 4.2.0 to 4.10.0, including upgrading Python within the Docker container to 3.10.7


## [1.0.5] - 2022-03-04

### Changed
* Bumped python to 3.10.
* Bumped base Docker image from pyaction:4.0.0 to pyaction:4.2.0.


## [1.0.4] - 2021-12-13

### Changed
* The base Docker image is now set to a specific version tag of pyaction,
  specifically 4.0.0.

### Fixed
* Query results should never be 0 since the workflow running the action is
  referencing the name of the workflow whose users are to be counted. GitHub
  code search API periodically returns 0 results, typically correcting itself next
  run. This patch prevents the badge JSON file from being written if result is 0.


## [1.0.3] - 2021-09-30

### Fixed
* Changed the default badge color to the shade of blue that is commonly used
  by Shields' badges for those badges that are informational. Our previous use
  of green was inconsistent with the common use of green for a passing status.
  Badges with counts of users is not a status that can be passed or failed. It
  is strictly informational, and potentially useful to maintainers of actions
  to know size of user-base and thus scale of the effects of potential changes.
  Users can still override the color to any that they desire with the color input.


## [1.0.2] - 2021-08-19

### Fixed
* Increased default `query-delay` to 65 seconds to minimize
  potential of hitting secondary rate limits for the use-case of
  monitoring multiple actions.
* Increased minimum `query-delay` to 33 seconds to minimize
  potential of hitting secondary rate limits for the use-case of
  monitoring multiple actions.
* Added cache directive to queries ("--cache 1h").


## [1.0.1] - 2021-08-05

### Fixed
* Significantly decreased chance of hitting code search API rate limits,
  or secondary limits, on cases where the user is using the action to 
  monitor multiple actions, by introducing a time delay between the queries
  for each subsequent action. Length of delay is controlled by a new optional
  action input, `query-delay`.
* Updated docs to clarify what this counts (number of workflows using the action).
   

## [1.0.0] - 2021-08-04

### Added
* This is the initial release.

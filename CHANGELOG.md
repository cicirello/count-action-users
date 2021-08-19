# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-08-19

### Added
  
### Changed
* Increased default `query-delay` to 65 seconds to minimize
  potential of hitting secondary rate limits for the use-case of
  monitoring multiple actions.
* Increased minimum `query-delay` to 33 seconds to minimize
  potential of hitting secondary rate limits for the use-case of
  monitoring multiple actions.
* Added cache directive to queries ("--cache 1h").

### Deprecated

### Removed

### Fixed


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

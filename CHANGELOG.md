# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed
 - Cleaned up the changelog

## [1.1.2] - 2023-02-20

### Fixed

 - Issues with Django default image URL

## [1.1.1] - 2023-02-20

### Fixed
 - Issues with new version of django-crispy-forms

## [1.1.0] - 2023-02-19

### Added
 - Support for adding more than 3 steps and ingredients to the recipe
 - Public recipes
 - Recipes can have images now

## [1.0.0] - 2023-02-11

### Added
 - Login and logout flows
 - Support for demo user
 - Link to the website
 - Logout link in the sidebar

### Changed
 - Settings restructured

### Fixed
 - Issue with CSRF verification that didn't allow form submission in production

## [0.1.3] - 2023-02-05 

### Fixed
 - Take dotenv path from environment

## [0.1.2] - 2023-02-05

### Fixed
 - Move all configuration to the deployer project

## [0.1.1] - 2023-01-30

### Fixed
 - Add missing configuration

## [0.1.0] - 2023-01-30

### Added
 - MVP supporting the full range of CRUDL operations on recipes

# Changelog
All notable changes to this project will be documented in this file.

## [1.1.4] - May 23, 2022
- Removed the template folder and started fetching the templates from github.
- Moved all flavours to one new repo called freshenv-flavours.
- Exception handling in the build command.

## [1.1.2] - May 23, 2022
- fixed the manifest file to add the template/simple dockerfile.

## [1.1.1] - May 23, 2022
- fixed the manifest file to add the template/simple dockerfile.

## [1.1.0] - May 21, 2022
- Enabled custom flavours by adding build command.
- removed the default value "zsh" to the --command/-c option to the provision command.
- An empty freshenv config file will be automatically created if no config is found when running the build command.
- Users can check build logs by passing the --logs/-l flag.
- Created a simple dockerfile template for custom flavours.
- Added new dependencies configparser and jinja2.
- Updated readme and versions.

## [1.0.3] - May 6, 2022
### Added
- Released on producthunt
- Added snap support
- This is the main version

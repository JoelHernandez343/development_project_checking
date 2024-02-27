# Development project checking

This tool searchs for every python project defined as:

-   a folder with a valid `env` folder
-   a folder with any `.py` file inside it

And checks for:

-   git repo existance
    -   pending changes
    -   .gitignore existance
-   if env detected:
    -   requirements.txt existance
    -   requirements.txt content vs pip freeze output

## To Do

-   [ ] Add support for javascript projects
-   [ ] Add support for github remote detection

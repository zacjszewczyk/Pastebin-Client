PastebinClient
==============

This is less of a project, and more of a quick app I whipped up one afternoon to fix a minor annoyance: interacting with Pastebin.com. I like the service, and use it often, but I wanted a quicker way to access the information I stored there. After a look at their API page, and some experimentation with the Python Requests library, I put together a simple command-line interface that lists every note I have stored there, and allows me to view or download them. It doesn't do much, but it scratches this itch for me, and so I thought I'd share it with you.

## Usage

In addition to the project files here, you will need to create one additional file to make this script work. Once you have downloaded this code, create a plain text "settings.txt" in the same directory as "pastebin.py". Format it as follows:

```
key=test_key
username=test_username
password=test_password
```

Replace "test_key" with your Pastebin developer key, "test_username" with your Pastebin username, and "test_password" with your Pastebin password. Do not incldue any spaces, quotation marks, or any other special characters, or any lines except those three. Now run "pastebin.py".

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/). a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Read more about the license, and my other disclaimers, [at my website](https://zacs.site/disclaimers.html).
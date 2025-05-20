# Basic Password Manager

## Description

Basic password management tool for storing and retrieving encrypted passwords.

## Features

- simple window UI (User Interface) that hides password values
- add, edit, and search for passwords
- automatically add passwords to clipboard by clicking on the designated row in the password list
- import text file of passwords
- encryption using AES (Advanced Encryption Standard) based on master user passcode

## Usage

To install and use this app:

1. Clone the repository.

```shell
git clone https://github.com/ColeBallard/basic-password-manager.git
```

2. Download [Python 3.12](https://www.python.org/downloads/). (Other versions will likely work fine).

3. Create the Virtual Environment.

```shell
python -m venv venv
```

4. Activate the Virtual Environment.

Windows (Command Prompt):

```shell
venv\Scripts\activate
```

Windows (PowerShell):

```shell
venv\Scripts\Activate.ps1
```

macOS/Linux:

```shell
source venv/bin/activate
```

5. Install the requirements.

```shell
pip install -r requirements.txt
```

6. Run the app.

```shell
python sdrowssap.py
```

7. Create an executable and move it to your desired location.

```shell
pyinstaller sdrowssap.spec
```

8. Run the app.

```shell
sdrowssap.exe
```

8. Either import a text file of passwords or create a new one by 

## Import Text File

To use the Import feature:

1. Create a text file that contains all of your passwords in the following schema:

```
service
attribute - value

service
attribute - value
attribute - value
attribute - value

service
attribute - value
attribute - value
```

2. Ensure that between each attribute and value is a dash with spaces around it and between each service group is a new line.

3. Save the text file, then run **main.exe**.

4. Press the Import button and select your password text file.

5. Enter a master password in the text box and press Go.

6. In the text box above the Search button, type in the service you want to find and press the Search button.

7. To copy the value to your clipboard, click the row where the attribute and value is at.

## Future Features

- button to let user see password values instead of masking them
  - starts off by default
- button to let user change master passcode
  - maintains file with old passcode by duplicating encrypted text file with timestamp
- button to let user export into a decrypted text file
- more advanced searching
  - possibly search by attribute name
- sort by date
- ensuring uniform font for all text input
- better ui
  - better button layout and space usage
  - might experiment with using toolbar for all buttons

## Contribution

If you have an idea or want to report a bug, please create an issue.

## **[Contact](https://github.com/ColeBallard/coleballard.github.io/blob/main/README.md)**

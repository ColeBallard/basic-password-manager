# Basic Password Manager

## Description

Basic password management tool for storing and retrieving encrypted passwords.

## Features

- simple window UI (User Interface)
- add and search for passwords
- automatically add passwords to clipboard by clicking on the designated row in the password list
- import text file of passwords
- encryption using AES (Advanced Encryption Standard) based on master user passcode

## Usage

To install and use this app:

1. Navigate to the [Releases page](https://github.com/ColeBallard/basic-password-manager/releases) of this repository.

2. Under the latest release, find the section **Assets**.

3. Click on the **sdrowssap.zip** file to download it to your computer.

4. Extract the contents of **sdrowssap.zip** by right-clicking on the file and selecting **Extract All...**.

5. Open the extracted folder and run **main.exe**.

6. From here, either import your data or add each service individually.

7. To add each service individually, enter a master password in the text box of the first window and press Go. 

8. The next window will have a list of your passwords. 

9. To add a new service, press the Add button. Click the <- button to go back to the list, the + button to add an attribute, and the - button to remove an attribute.

10. In the top text box, write your service. In the bottom text boxes, write your attributes and values in the format `attribute : value`.

11. Click submit once you've finished creating your service and all your attribute/values.

12. Scroll through the list of your passwords and click on a row to copy its value.

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

6. Scroll through the list of your passwords and click on a row to copy its value.

## Contribution

If you have an idea or want to report a bug, please create an issue.

## **[Contact](https://coleb.io/contact)**

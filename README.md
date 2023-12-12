<h1 style="text-align: center"> AirBnB clone - The console</h1>
<div style="display: flex;justify-content: center" >
<img src="img.png" width="70%" style="text-align: center"/>
</div>

## Description


>The project is built to be a clone of the AirBnB website. This repository contains the initial stage of the project, which implements a backend interface, or console, to manage program data. Console commands allow the user to create, update, and destroy objects, as well as manage file storage. Using a system of JSON serialization/deserialization, storage is persistent between sessions.



## How to Start

To start the project, you need to run the `console.py` file in your terminal. 
This will launch the console, where you can begin entering commands.

## Usage

Commands available in the console include:

| Command  | Syntax                                                                                                                               | Description                                                                    |
|----------|--------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `create` | -`create <class name>`                                                                                                               | Creates an instance based on given class.saves it and prints the id<br/>       |
| `show`   | -`show <class name> <id>`<br/>-`<class name>.show(<id>)`                                                                             | Prints the string representation of an instance based on the class name and id |
| `destroy` | -`destroy <class name> <id>`<br/>-`<class name>.destroy(<id>)`                                                                       | Deletes an instance based on the class name and id                             |
| `all`    | -`all <class name>` <br/>-`all`<br/>-`<class name>.all(<id>)`                                                                        | Shows all objects the program has access to, or all objects of a given class   |
| `update` | -`update <class name> <id> <attribute name> <attribute value>`<br/>-`<class name>.update(<id>, <attribute name>, <attribute value>)` | Updates existing attributes an object based on class name and UUID             |
|          | -`<class name>.update(<id>, <dictionary representation>)`                                                                            | update an instance based on his ID with a dictionary                           |
| `count`  | -`<class name>.count()`                                                                                                              | retrieve the number of instances of a class                                    |





## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [MIT](https://mit-license.org/) License.

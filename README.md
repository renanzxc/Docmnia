# Docmnia
Documentation generator for Insomnia API. 🐍

## Dependencies
* Python 3.x
  * Jinja2 
```sh
$ sudo apt-get install python3.6
```
```sh
$ pip3 install jinja2
```
## Command to run
Inside the root folder execute:
```sh
$ python3 main.py -insomnia EXPORTED_INSOMNIA_FILE.json -output FORMAT
```
## Example

```sh
$ python3 main.py -i api.json -o yaml
```
## Release History

* v0.1
  * Basic yaml documentation generator

# CLI fetching from RandomUserAPI
  Command line utility fetching number (default: 25) of users from [RandomUserAPI](https://randomuser.me), saving their thumbnails in given directory and creating a index.html table of'em.

## Prerequisites:
* Python 3.5+

## Running
```
pip install -r requirements.txt
```
```
./randomuser.py output_directory [-n Number_Of_Users, -v]
```
## Example
Fetch two users, write all files to ./output/
```
./randomuser.py output -n 2
```

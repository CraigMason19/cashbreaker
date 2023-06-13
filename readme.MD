# cashbreaker

A Python console project to help solve cashbreakers that are found in the UK puzzle magazines. Program allows you to load in a text file representing the cashbreaker and then to manipulate it or automatically try and solve it.

## Requirements
Checked with python 3.11.2

Also requires numpy 1.23.2

## Usage

Run the caller.py script to run the program.

##### Console commands
```Python
Exit -> ['close', 'c', 'exit', 'e']
Clear screen -> ['cls', 'clear']
Reset -> ['reset', 'r']
Show representation -> ['repr']
Show help -> ["help", 'h']
Guess words / solve -> ['guess', 'g', 'fill', 'f', 'solve', 's']
All possible words = ['all', 'a']
All possible words by lowest number of matches = [ 'all order', 'ao']
```


##### Assign letter to number
```python
(number)=(letter) 
e.g. 9=a

# To clear use
9=_
```
##### Assign letter to location (horizontal then vertical)
```python
(x,y)=(letter) 
e.g. 5,7=a

# To clear use
5,7=_
```
##### Show potential words
```python
w=_at_le  
['battle', 'cattle', 'pattle', 'rattle', 'tattle', 'wattle']
```

## Screenshots
![solved_breaker_5](https://github.com/CraigMason19/cashbreaker/blob/master/screenshots/solved_breaker_5.png?raw=true)
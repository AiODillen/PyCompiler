
# Setup

- Clone the Repository

# Running the Compiler

- Fill in your Code into the Input.dillen file.
- Run the Main.py file.
- The created Python file will be the ./out/out.py file.
- The created Python Byte Code will be the ./out/__pycache__/xxx.pyc file.

# Running Compiled Code

- Either:
	- Run the out.py file with a python version of your liking
	- Run the xxx.pyc file with "python <path_to_pyc_file>"
		- Make sure that you use the same python version to run this than you did for creating the file.
      	- Otherwise, a bad magic number error will occur...


# Example Code
```
var x:str = "sdf";
var y:int = 3;
var z:float = 3.3;
var u:int = 3.3;
var l:list = [1, 2, 3, 4]

var m:int = 2+5;
var s:str = "Hello" + "World";

print(s);

func test: str (c:int, v:str) {
    var k:float = 3.2;
    if (1 == 2) {
        var d:int = 3;
    };
};
```
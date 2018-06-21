# 1. K64F

The code that K64F runs contains the IR gesture, XBee, uLCD modules. Using hand gestures as input, the corresponding function is determined and the command will be sent to the PC through XBee, and the result will be display on the uLCD.

The wire connection is just as same as the labs are.

# 2. PC

PC runs python codes "main.py", which intakes the command from K64F and executes. It supports the following functions:

- Swipe UP for [git lab crawler](#git lab crawler)

- Swipe LEFT to [display the content](#display the content) of your git lab repositories

- Swipe RIGHT to select some [basic shell commands](#basic shell commands)

## <a name="git lab crawler"></a> git lab crawler

main.py imports test_selenium.git_lab_inquiry

test_selenium.git_lab_inquiry is a web crawler, which is used to retrieve data on Internet automatedly. It uses a invisible web browser - PhantomJS as a simulated user to request a html and using some functions to locate the target html tags, thus collecting data and storing in the local PC files.

## <a name="display the content"></a> display the content

main.py imports serial_put.serialPut and serial_put.sendOneChar

Both functions are used to send data from PC to K64F through XBee - serial_put.serialPut sends a whole text file while serial_put.sendOneChar only sends a single character.

When the uLCD screen are full of texts, user need to swipe RIGHT to print next page and swipe LEFT to print previous in serial_put.serialPut. All the text transmission is done in real time since the K64F doesn't have a file system for me to store the data, so it is quite a task for me to do the page turing feature.

## <a name="basic shell commands"></a> basic shell commands

main.py imports shell_command.oneTimeShell

shell_command.oneTimeShell creates a subprocess for shell, so basically is should be as powerful as a shell can be. Due to the lack of input modules, it can only support 3 hot commands:

- swipe UP to perform "ls"

- swipe RIGHT to preform "git status"

- swipe DOWN to perform "pwd"

and the function subprocess.check_output() will return the result, then print it on the screen. 
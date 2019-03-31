# DAS-Aero

*For use with Ardupilot.*

ENVIRONMENT SETUP:
1. Install pip and python3 and add to path/environment variables
2. Install git and git bash
3. Navigate to directory of choice and clone repo ("git init" then "git clone https://github.com/mwlkhoo/DAS-Aero.git"
4. Run "pip install virtualenv"
5. Navigate to directory of choice and "git clone https://github.com/mavlink/mavlink.git" then "git submodule update --init --recursive"
6. For all "import <dependecy>" or "from <dependency> import <...>" at the top of .py file, in command line enter: pip install <dependency> 

*EDIT: "pip install pymavlink" should be the only dependency that needs to be installed"*

MISSION PLANNER:
1. <ctrl + f>
2. mavlink
3. select TCP host -> connect

CONFIGURE CODE:
1. Go to the <file>.py
2. set "the_connection: tcp:localhost:14550"
3. Check that the servo number matches the servo for each component (for "<component>Servo = servoData.servo<number>_raw") -> find in the if statements within the main loop 
4. Check that for "<component>Trigger = <value>" the value makes sense for servo configuration
5. Check that for "if(<component>Servo > <component>Trigger):" boolean comparator makes sense with servo trigger -> find in the if statements within the main loop 

RUN CODE: 
1. Navigate to directory containing file
2. Enter: "python das-output.py"
3. To quit program: "ctrl + c"

Triggering servo release should now. 

**IMPORTANT: Trigger servo by setting either "high" or "low", not "toggle" (change in signal may be too quick to be detected)**

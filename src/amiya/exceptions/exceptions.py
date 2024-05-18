# MIT License
#
# Copyright (c) 2024 Kevin L.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from amiya.utils.constants import BASENAME, VERSION

class AmiyaBaseException(Exception):
    __module__ = 'builtins'
    def __init__(self, message="An unknown error has occurred."):
        super().__init__(message)

class Amiya_AppExistsException(Exception):
    __module__ = 'builtins'
    def __init__(self, app_name):
        self.message = f"The app ({app_name}) already exists under Amiya."
        super().__init__(self.message)

class Amiya_AppInvalidPathException(Exception):
    __module__ = 'builtins'
    def __init__(self, path):
        self.message = f"The path configured for the application ['{path}'] cannot be verified (most likely due to an incorrect path). Please reconfigure the path for the app."
        super().__init__(self.message)
        
class Amiya_DuplicateTagException(Exception):
    __module__ = 'builtins'
    def __init__(self, tag, tagged_app_name):
        self.message = f"The tag ({tag}) already exist under the app '{tagged_app_name}'."
        super().__init__(self.message)

class Amiya_NoSuchTagException(Exception):
    __module__ = 'builtins'
    def __init__(self, tag):
        self.message = f"The tag ({tag}) does not coorespond to any of the apps."
        super().__init__(self.message)    

class Amiya_ConfigDoesNotExistException(Exception):
    __module__ = 'builtins'
    def __init__(self, config_file):
        self.message = f"The config file '{config_file}' does not exist and therefore cannot be read."
        super().__init__(self.message) 
        
class Amiya_ConfigAlreadyExistException(Exception):
    __module__ = 'builtins'
    def __init__(self, config_file):
        self.message = f"The config file '{config_file}' already exist and overwrite is set to False."
        super().__init__(self.message) 

class Amiya_AppNotFocusedException(Exception):
    __module__ = 'builtins'
    def __init__(self):
        super().__init__(f"\nThe application is not focused during an automation sequence run. Automation stopped.")

class AmiyaOSNotSupported(Exception):
    __module__ = 'builtins'
    def __init__(self):
        super().__init__(f"\n\n\tAs of version {VERSION} (BETA), the {BASENAME} package is only supported on the Windows OS.")

# This is a special exception that is used in place of exit() to avoid IO read error in the CLI environment (to avoid closing STDOUT).
# This error is caught and replaced with 'continue' in the CLI env and 'exit()' in the normal mode. 
class AmiyaExit(Exception):
    __module__ = 'builtins'
    def __init__(self, message="Module internal exit requested (should be caught accordingly)."):
        super().__init__(message)

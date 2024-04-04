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

class AmiyaBaseException(Exception):
    __module__ = 'builtins'
    def __init__(self, message):
        super().__init__(message)

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

class AmiyaOSNotSupported(Exception):
    __module__ = 'builtins'
    def __init__(self):
        super().__init__(f"\nThe Amiya package is only supported on Windows and Linux at the moment.")

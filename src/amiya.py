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


#     _    __  __ _____   __ _       ____ _     ___  
#    / \  |  \/  |_ _\ \ / // \     / ___| |   |_ _| 
#   / _ \ | |\/| || | \ V // _ \   | |   | |    | |  
#  / ___ \| |  | || |  | |/ ___ \  | |___| |___ | |  
# /_/   \_\_|  |_|___| |_/_/   \_\  \____|_____|___|
#
# TO INSTALL THE AMIYA CLI MODULE LOCALLY, RUN
#   
#     $ pip install amiya
# OR
#     $ git clone https://github.com/ReZeroE/Amiya.git
#     $ cd Amiya/
#     $ pip install .
#
#
# RUN THIS SCRIPT TO START THE AMIYA CLI WITHOUT INSTALLATION.

import sys
from amiya.utils.helper import verify_platform
from amiya.entrypoints.entrypoints import start_amiya
from amiya.exceptions.exceptions import AmiyaOSNotSupported

if verify_platform():
    sys.argv = ['amiya']; start_amiya()
else:
    raise AmiyaOSNotSupported()



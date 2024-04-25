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

from amiya.apps_manager.apps_manager import AppsManager
from amiya.automation_handler.automation_controller import AutomationController

am = AppsManager()

# am.record_sequence()
# am.list_sequences()
am.run_sequence()

# # am.create_app("Chrome", "C:\Program Files\Google\Chrome\Application\chrome.exe")
# # am.create_app("Final Fantasy XIV", "abc/abc.exe")
# # am.create_app("LD Player", "E:\LDPlayer\LDPlayer9\dnplayer.exe")
# # am.print_apps()
# am.remove_tag()




# ac = AutomationController("D:/Workspace/Amiya/src/amiya/apps/chrome/automation")
# ac.record_new_sequence("test_auto2", overwrite=False)
# sequence = ac.load_sequence("test_auto.json")
# sequence.run()


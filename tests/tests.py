# count-action-users: Generates Shields endpoint with number of users of a GitHub Action
# 
# Copyright (c) 2021 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
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
#

import unittest

import ActionUserCounter as action
import copy
import os
import json

class TestSomething(unittest.TestCase) :

    def test_splitActionOwnerName(self) :
        cases = [
            "user/action",
            "user/action-name",
            "user/longer-action-name",
            "action",
            "action-name",
            "longer-action-name"
            ]
        expected = [
            ("user", "action"),
            ("user", "action-name"),
            ("user", "longer-action-name"),
            ("", "action"),
            ("", "action-name"),
            ("", "longer-action-name")
            ]
        for i, c in enumerate(cases) :
            self.assertEqual(expected[i], action.splitActionOwnerName(c))

    def test_formatCount(self) :
        cases = [
            (0, "0"),
            (1, "1"),
            (9, "9"),
            (10, "10"),
            (99, "99"),
            (100, "100"),
            (999, "999"),
            (1000, "1000"),
            (9999, "9999"),
            (10000, "10.0K"),
            (10099, "10.0K"),
            (10100, "10.1K"),
            (99900, "99.9K"),
            (99999, "99.9K"),
            (100000, "100.0K"),
            (100099, "100.0K"),
            (100100, "100.1K"),
            (999900, "999.9K"),
            (999999, "999.9K"),
            (1000000, "1.00M"),
            (1009999, "1.00M"),
            (1010000, "1.01M"),
            (1019999, "1.01M"),
            (1020000, "1.02M"),
            (1099999, "1.09M"),
            (1100000, "1.10M"),
            (1109999, "1.10M"),
            (9999999, "9.99M"),
            (10000000, "10.00M")
            ]
        for caseInput, expected in cases :
            self.assertEqual(expected, action.formatCount(caseInput))

    def test_toDictWithShieldsKeys(self) :
        cases = [
            ("100", "green", None, None),
            ("100", "green", "actions", None),
            ("100", "green", "github", None),
            ("100", "green", None, "flat"),
            ("100", "green", "actions", "flat"),
            ("100", "green", "github", "flat")
            ]
        expected = [
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green"},
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "actions"},
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "github"},
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "style" : "flat"},
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "actions", "style" : "flat"},
            {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "github", "style" : "flat"}
            ]
        for i, (count, color, logo, style) in enumerate(cases) :
            self.assertEqual(expected[i], action.toDictWithShieldsKeys(count, color, logo, style))

    def test_toJsonEndpoints(self) :
        case = {
            "action-1" : "100",
            "action-2" : "120",
            "action-3" : "303",
            "action-4" : "104",
            "action-5" : "155",
            "action-6" : "600"
            }
        expected1 = {
            "action-1" : {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green"},
            "action-2" : {"schemaVersion" : 1, "label" : "used by", "message" : "120", "color" : "green"},
            "action-3" : {"schemaVersion" : 1, "label" : "used by", "message" : "303", "color" : "green"},
            "action-4" : {"schemaVersion" : 1, "label" : "used by", "message" : "104", "color" : "green"},
            "action-5" : {"schemaVersion" : 1, "label" : "used by", "message" : "155", "color" : "green"},
            "action-6" : {"schemaVersion" : 1, "label" : "used by", "message" : "600", "color" : "green"}
            }
        expected2 = {
            "action-1" : {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-2" : {"schemaVersion" : 1, "label" : "used by", "message" : "120", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-3" : {"schemaVersion" : 1, "label" : "used by", "message" : "303", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-4" : {"schemaVersion" : 1, "label" : "used by", "message" : "104", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-5" : {"schemaVersion" : 1, "label" : "used by", "message" : "155", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-6" : {"schemaVersion" : 1, "label" : "used by", "message" : "600", "color" : "green", "namedLogo" : "github", "style" : "flat"}
            }
        self.assertEqual(expected1, action.toJsonEndpoints(case, "green", None, None))
        self.assertEqual(expected2, action.toJsonEndpoints(case, "green", "github", "flat"))

    def test_writeToFiles(self) :
        case1 = {
            "action-1" : {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green"},
            "action-2" : {"schemaVersion" : 1, "label" : "used by", "message" : "120", "color" : "green"},
            "action-3" : {"schemaVersion" : 1, "label" : "used by", "message" : "303", "color" : "green"},
            "action-4" : {"schemaVersion" : 1, "label" : "used by", "message" : "104", "color" : "green"},
            "action-5" : {"schemaVersion" : 1, "label" : "used by", "message" : "155", "color" : "green"},
            "action-6" : {"schemaVersion" : 1, "label" : "used by", "message" : "600", "color" : "green"}
            }
        case2 = {
            "action-1" : {"schemaVersion" : 1, "label" : "used by", "message" : "100", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-2" : {"schemaVersion" : 1, "label" : "used by", "message" : "120", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-3" : {"schemaVersion" : 1, "label" : "used by", "message" : "303", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-4" : {"schemaVersion" : 1, "label" : "used by", "message" : "104", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-5" : {"schemaVersion" : 1, "label" : "used by", "message" : "155", "color" : "green", "namedLogo" : "github", "style" : "flat"},
            "action-6" : {"schemaVersion" : 1, "label" : "used by", "message" : "600", "color" : "green", "namedLogo" : "github", "style" : "flat"}
            }
        os.chdir("tests")
        action.writeToFiles(copy.deepcopy(case1), False)
        for actionName, expected in case1.items() :
            filename = actionName + ".json"
            self.assertTrue(os.path.exists(filename))
            with open(filename, "r") as f :
                self.assertEqual(expected, json.load(f))
            os.remove(filename)

        action.writeToFiles(copy.deepcopy(case2), False)
        for actionName, expected in case2.items() :
            filename = actionName + ".json"
            self.assertTrue(os.path.exists(filename))
            with open(filename, "r") as f :
                self.assertEqual(expected, json.load(f))
            os.remove(filename)
        os.chdir("..")


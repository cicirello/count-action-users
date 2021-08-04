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

import os
import json

class TestIntegration(unittest.TestCase) :

    def test_integration(self) :
        # verify creates directory if necessary
        self.assertTrue(os.path.exists("tests/endpoints"))
        # verify that the json files were created
        self._validate("tests/endpoints/jacoco-badge-generator.json")
        #self._validate("tests/endpoints/setup-python.json")
        self._validate("tests/endpoints/aFakeActionForTestingThatCannotPossiblyActuallyExistShouldHaveCountOfZero.json", True)
        
    def _validate(self, filename, zeroCount=False) :
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r") as f :
            d = json.load(f)
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("used by", d["label"])
            messageParts = d["message"].split()
            try:
                if messageParts[0][-1]=="K" or messageParts[0][-1]=="M" :
                    count = float(messageParts[0][:-1])
                else :
                    count = int(messageParts[0])
                if zeroCount :
                    # The search might return this workflow, so might be 1.
                    self.assertTrue(count <= 1)
            except ValueError:
                self.fail("count not an int")
            #self.assertTrue(messageParts[1].startswith("repo"))
            self.assertEqual("#4c1", d["color"])
            self.assertEqual("githubactions", d["namedLogo"])
            self.assertFalse("style" in d)


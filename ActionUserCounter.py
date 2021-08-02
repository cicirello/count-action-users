#!/usr/bin/env python3
#
# action-user-count: Reports count of repositories using a GitHub Action
# as a Shields.io endpoint
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

import sys

if __name__ == "__main__" :
    actionList = sys.argv[1].strip().replace(",", " ").split()

    targetDirectory = sys.argv[2].strip()
    
    failOnError = sys.argv[3].strip().lower() == "true"
    
    commitAndPush = sys.argv[4].strip().lower() == "true"
    
    color = sys.argv[5].strip()
    
    includeLogo = sys.argv[6].strip().lower() == "true"
    
    logoName = sys.argv[7].strip()
    
    style = sys.argv[8].strip()
    
    exitCode = 0
    
    print("::set-output name=exit-code::" + str(exitCode))
    

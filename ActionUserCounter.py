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
import json
import os
import os.path
import pathlib

queryTemplate = """search/code?q={0}+path%3A.github%2Fworkflows+language%3AYAML"""

def splitActionOwnerName(action) :
    """Takes the name of an action that may include both owner and action
    name, and splits it.

    Keyword arguments:
    action - Name of action, possibly including both owner and name.
    """
    s = action.split("/")
    return (s[0], s[1]) if len(s) > 1 else ("", s[0])

def executeCommand(arguments) :
    """Execute a subprocess and return result and exit code.
    
    Keyword arguments:
    arguments - The arguments for the command.
    """
    result = subprocess.run(
        arguments,
        stdout=subprocess.PIPE,
        universal_newlines=True
        )
    return result.stdout.strip(), result.returncode

def executeQuery(owner, actionName, failOnError) :
    """Executes a query for an owner actionName combination.

    Keyword arguments:
    owner - The owner of the action, which may be the empty string for this query.
    actionName - The name of the action.
    failOnError - Pass True to fail the workflow if an error occurs.
    """
    q = owner + "+" + actionName if len(owner) > 0 else actionName
    result, exitCode = executeCommand(["gh", "api", queryTemplate.format(q)])
    if exitCode != 0 :
        print("Error: An error with code", exitCode, "occurred during GitHub API query.")
        print(result)
        print("::set-output name=exit-code::" + str(exitCode))
        exit(exitCode if failOnError else 0)
    result = json.loads(result)
    if "total_count" in result :
        return result["total_count"]
    else :
        print("Error: total_count missing from GitHub API query result")
        exitCode = 1
        print("::set-output name=exit-code::" + str(exitCode))
        exit(exitCode if failOnError else 0)

def collectRepoCounts(actionList, failOnError) :
    """Executes all necessary queries to gather the user counts of
    all actions in the actionList. Returns a map from action name to
    associated count.

    Keyword arguments:
    actionList - A list of actions to report usage on
    failOnError - Pass True to fail the workflow if an error occurs
    """
    countMap = {}
    for action in actionList :
        owner, actionName = splitActionOwnerName(action)
        count = executeQuery(owner, actionName, failOnError)
        countMap[actionName] = count
    return countMap

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
    
    countMap = collectRepoCounts(actionList, failOnError)
    if len(targetDirectory) > 0 :
        if not os.path.exists(targetDirectory) :
            p = pathlib.Path(targetDirectory)
            os.umask(0)
            p.mkdir(mode=0o777, parents=True, exist_ok=True)
        os.chdir(targetDirectory)

    # Iterate over countMap.items() and generate JSON for each

    # Commit and push
    
    
    print("::set-output name=exit-code::" + str(exitCode))
    

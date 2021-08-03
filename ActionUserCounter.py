#!/usr/bin/env python3
#
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
        countMap[actionName] = formatCount(count)
    return countMap

def formatCount(count) :
    """Formats the integer count ready.

    Keyword arguments:
    count - The count of number of repositories using the action as an integer,
    """
    if count == 1 :
        return "{0} repo".format(count)
    elif count < 10000 :
        return "{0} repos".format(count)
    elif count < 1000000 :
        return "{0:.1f}K repos".format(count // 100 * 100 / 1000)
    else :
        return "{0:.2f}M repos".format(count // 10000 * 10000 / 1000000)

def toJsonEndpoints(countMap, color, logoName, style) :
    """Creates the Python dictionaries that will be written to files as JSON endpoints.

    Keyword arguments:
    countMap - A Python dictionary mapping action name to Python dictionaries
       ready to write to files as JSON.
    color - The color for the data portion of the badge.
    logoName - A named logo or None for no logo in badge.
    style - The name of the shields style to use.
    """
    return { actionName : toDictWithShieldsKeys(count, color, logoName, style) for actionName, count in countMap.items() }

def toDictWithShieldsKeys(count, color, logoName, style) :
    """Creates a Python dictionary with all of the necessary
    keys for a Shields endpoint.

    Keyword arguments:
    count - The count of the number of repositories using an action.
    color - The color for the data portion of the badge.
    logoName - A named logo or None for no logo in badge.
    style - The name of the shields style to use or None for Shields default.
    """
    d = {
        "schemaVersion" : 1,
        "label" : "used by",
        "message" : count,
        "color" : color
        }
    if logoName != None :
        d["namedLogo"] = logoName
    if style != None :
        d["style"] = style
    return d

def writeToFiles(endpointMap, failOnError) :
    """Writes the endpoints to json files. Returns a list of all of
    the filenames written to.

    Keyword arguments:
    endpointMap - A Python dictionary mapping action name, which is used for filename,
        to Python dictionary with the Shields key value pairs.
    failOnError - Pass True to fail the workflow if an error occurs
    """
    allFilenames = []
    for actionName, endpointdata in endpointMap.items() :
        filename = actionName + ".json"
        try :
            with open(filename, "w") as jsonOut :
                json.dump(endpointdata, jsonOut)
                allFilenames.append(filename)
        except:
            print("Error: Failed while writing:", filename)
            exitCode = 2
            print("::set-output name=exit-code::" + str(exitCode))
            exit(exitCode if failOnError else 0)
    return allFilenames

def commitAndPush(allFilenames, name, login, failOnError) :
    """Commits and pushes the endpoint files.
    
    Keyword arguments:
    allFilenames - A list of all filenames written to
    name - The name of the committer.
    login - The login id of the committer.
    failOnError - Pass True to fail the workflow if an error occurs.
    """
    # Make sure this isn't being run during a pull-request or some other detached head scenario.
    result = executeCommand(["git", "symbolic-ref", "-q", "HEAD"])
    if result[1] == 0 :
        # Check if anything json endpoints changed
        args = ["git", "status", "--porcelain"]
        args.extend(allFilenames)
        result = executeCommand(args)
        if len(result[0]) > 0 :
            # Commit and push
            executeCommand(["git", "config", "--global", "user.name", name])
            executeCommand(["git", "config", "--global",
                            "user.email", login + '@users.noreply.github.com'])
            args = ["git", "add"]
            args.extend(allFilenames)
            executeCommand(args)
            args = ["git", "commit", "-m",
                    "Automated change by https://github.com/cicirello/count-action-users"]
            args.extend(allFilenames)
            executeCommand(args)
            r = executeCommand(["git", "push"])
            if r[1] != 0 :
                print("Error: push failed.")
                exitCode = 3
                print("::set-output name=exit-code::" + str(exitCode))
                exit(exitCode if failOnError else 0)

if __name__ == "__main__" :
    actionList = sys.argv[1].strip().replace(",", " ").split()

    targetDirectory = sys.argv[2].strip()
    
    failOnError = sys.argv[3].strip().lower() == "true"
    
    commit = sys.argv[4].strip().lower() == "true"
    
    color = sys.argv[5].strip()
    if len(color) == 0 :
        color = '#4c1'
    
    includeLogo = sys.argv[6].strip().lower() == "true"
    
    logoName = sys.argv[7].strip()
    if len(logoName) == 0 or not includeLogo:
        logoName = None
    
    style = sys.argv[8].strip()
    # Keep endpoint size down by not specifying style if
    # user just wants the Shields default of flat.
    if len(style) == 0 or style == "flat":
        style = None

    exitCode = 0
    
    countMap = collectRepoCounts(actionList, failOnError)
    if len(targetDirectory) > 0 :
        if not os.path.exists(targetDirectory) :
            p = pathlib.Path(targetDirectory)
            os.umask(0)
            p.mkdir(mode=0o777, parents=True, exist_ok=True)
        os.chdir(targetDirectory)

    allFilenames = writeToFiles(
        toJsonEndpoints(countMap, color, logoName, style),
        failOnError
        )

    if commit and len(allFilenames) > 0 :
        commitAndPush(allFilenames, "github-actions", "41898282+github-actions[bot]", failOnError)
    
    print("::set-output name=exit-code::" + str(exitCode))
    

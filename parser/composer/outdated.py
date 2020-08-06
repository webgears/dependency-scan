#!/usr/bin/env python

import subprocess
import json
import re

class OutdatedParser:
    def __init__(self, composer_binary, project_folder):
        self.composer_binary = composer_binary
        self.project_folder = project_folder

    def gather_data(self):
        outdated = self.__run_check()
        patches, minor, major = self.__parse_outdated(outdated)

        return (patches, minor, major)


    def __run_check(self):
        process = subprocess.Popen(self.composer_binary + ' outdated --format=json', cwd=self.project_folder, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()

        out = out.decode('utf-8')
        
        return out

    @staticmethod
    def __parse_outdated(outdated):
        try:
            parsed_json = json.loads(outdated)
            
            patches = 0
            minor = 0
            major = 0

            for element in parsed_json['installed']:

                if 'version' not in element or 'latest' not in element:
                    # skip this if we can't compare
                    continue

                current = element['version']
                latest = element['latest']

                pattern = re.compile('^v?\d+\.\d+(\.\d+)?$')
                if pattern.match(current) and pattern.match(latest):

                    current_split = current.split('.')
                    latest_split = latest.split('.')

                    if current_split[0] != latest_split[0]:
                        major+=1
                    elif current_split[1] != latest_split[1]:
                        minor+=1
                    elif len(current_split) < 3 or len(latest_split) < 3 or current_split[2] != latest_split[2]:
                        patches+=1
                    else:
                        print("Unknown case: " + current + ", " + latest)
                else:
                    print("Not matching semantic versioning: " + current + ", " + latest)
                    # If it is not using semantic versions match is given, we use "major" instead
                    major += 1

            return (patches, minor, major)

        except json.decoder.JSONDecodeError as e:
            print("JSON Decode error: {0}".format(e))
            print(outdated)
            raise e
        
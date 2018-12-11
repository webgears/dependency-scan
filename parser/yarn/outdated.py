#!/usr/bin/env python

import subprocess
import json

class OutdatedParser:
    def __init__(self, yarn_binary, project_folder):
        self.yarn_binary = yarn_binary
        self.project_folder = project_folder

    def gather_data(self):
        outdated = self.__run_check()
        patches, minor, major = self.__parse_outdated(outdated)

        return (patches, minor, major)


    def __run_check(self):
        process = subprocess.Popen(self.yarn_binary + ' outdated --no-progress --non-interactive --json', cwd=self.project_folder, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()

        out = out.decode('utf-8')
        out = out.split("\n")[1]

        return out

    @staticmethod
    def __parse_outdated(outdated):
        parsed_json = json.loads(outdated)
        
        patches = 0
        minor = 0
        major = 0

        for element in parsed_json['data']['body']:
            current = element[1].split('.')
            latest = element[3].split('.')

            if current[0] != latest[0]:
                major+=1
            elif current[1] != latest[1]:
                minor+=1
            elif current[2] != latest[2]:
                patches+=1

        return (patches, minor, major)
        
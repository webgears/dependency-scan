#!/usr/bin/env python

import subprocess
import json

class SecurityParser:
    def __init__(self, security_checker, project_folder):
        self.security_checker = security_checker
        self.project_folder = project_folder

    def gather_data(self):
        audit = self.__run_check()

        return self.__parse_audit(audit)

    def __run_check(self):
        process = subprocess.Popen(self.security_checker + ' security:check --format=json', cwd=self.project_folder, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode('utf-8')

        return out

    @staticmethod
    def __parse_audit(audit):
        try:
            parsed_json = json.loads(audit)

            # As there is no error level, we mark them all as high
            return (0, 0, 0, len(parsed_json.keys()), 0)
        except json.decoder.JSONDecodeError as e:
            print("JSON Decode error: {0}".format(e))
            print(audit)
        
        return (0, 0, 0, 0, 0)
        
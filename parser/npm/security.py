#!/usr/bin/env python

import subprocess
import json

class SecurityParser:
    def __init__(self, npm_binary, project_folder):
        self.npm_binary = npm_binary
        self.project_folder = project_folder

    def gather_data(self):
        audit = self.__run_check()

        return self.__parse_audit(audit)

    def __run_check(self):
        process = subprocess.Popen(self.npm_binary + ' audit --no-progress --non-interactive --json', cwd=self.project_folder, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode('utf-8')

        return out

    @staticmethod
    def __parse_audit(audit):
        try:
            parsed_json = json.loads(audit)

            return (parsed_json['metadata']['vulnerabilities']['info'], 
                parsed_json['metadata']['vulnerabilities']['low'], 
                parsed_json['metadata']['vulnerabilities']['moderate'], 
                parsed_json['metadata']['vulnerabilities']['high'], 
                parsed_json['metadata']['vulnerabilities']['critical']
                )
        
        except json.decoder.JSONDecodeError as e:
            print("JSON Decode error: {0}".format(e))
            print(audit)
            raise e

#!/usr/bin/env python

import subprocess
import json

class SecurityParser:
    def __init__(self, yarn_binary, project_folder):
        self.yarn_binary = yarn_binary
        self.project_folder = project_folder

    def gather_data(self):
        audit = self.__run_check()

        return self.__parse_audit(audit)

    def __run_check(self):
        process = subprocess.Popen(self.yarn_binary + ' audit --no-progress --non-interactive --json', cwd=self.project_folder, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        out = out.decode('utf-8')

        return out

    @staticmethod
    def __parse_audit(audit):
        try:
            summary = audit.splitlines()[-1]
            parsed_json = json.loads(summary)

            if(parsed_json['type'] != "auditSummary"):
                raise Exception('Could not fetch summary')

            return (parsed_json['data']['vulnerabilities']['info'], 
                parsed_json['data']['vulnerabilities']['low'], 
                parsed_json['data']['vulnerabilities']['moderate'], 
                parsed_json['data']['vulnerabilities']['high'], 
                parsed_json['data']['vulnerabilities']['critical']
                )

        except json.decoder.JSONDecodeError as e:
            print("JSON Decode error: {0}".format(e))
            print(audit)
            raise e
        
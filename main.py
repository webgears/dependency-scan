#!/usr/bin/env python

import sheets
from parser.npm.outdated import OutdatedParser as NpmOutdatedParser
from parser.npm.security import SecurityParser as NpmSecurityParser
from parser.yarn.outdated import OutdatedParser as YarnOutdatedParser
from parser.yarn.security import SecurityParser as YarnSecurityParser
from parser.composer.outdated import OutdatedParser as ComposerOutdatedParser
from parser.composer.security import SecurityParser as ComposerSecurityParser

from time import gmtime, strftime

import argparse

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--project", required=False, help="Project Folder")
ap.add_argument("-i", "--spreadsheet_id", required=False, help="Spreadsheet ID for the spreadsheet")
ap.add_argument("-s", "--sheet", required=False, help="Sheet Name to add the data to")
ap.add_argument("-y", "--yarn-audit", required=False, help="Run yarn audit", action="store_true")
ap.add_argument("-n", "--npm-audit", required=False, help="Run npm audit", action="store_true")
ap.add_argument("-c", "--composer-audit", required=False, help="Run composer audit", action="store_true")
ap.add_argument("--npm-bin", required=False, help="Path to npm binary", default="npm")
ap.add_argument("--yarn-bin", required=False, help="Path to yarn binary", default="yarn")
ap.add_argument("--composer-bin", required=False, help="Path to composer binary", default="composer")
ap.add_argument("--symfony-bin", required=False, help="Path to symfony CLI binary", default="symfony")
args = vars(ap.parse_args())

def main():

    outdated = (0, 0, 0) # Patches, Minor, Major
    security_issues = (0, 0, 0, 0 ,0) # Info, Low, Moderate, High, Critical

    if args['npm_audit']:
        outdated_parser = NpmOutdatedParser(args['npm_bin'], args['project'])
        security_parser = NpmSecurityParser(args['npm_bin'], args['project'])
        outdated = add_tuples(outdated, outdated_parser.gather_data())
        security_issues = add_tuples(security_issues, security_parser.gather_data())

    if args['yarn_audit']:
        outdated_parser = YarnOutdatedParser(args['yarn_bin'], args['project'])
        security_parser = YarnSecurityParser(args['yarn_bin'], args['project'])
        outdated = add_tuples(outdated, outdated_parser.gather_data())
        security_issues = add_tuples(security_issues, security_parser.gather_data())
    
    if args['composer_audit']:
        outdated_parser = ComposerOutdatedParser(args['composer_bin'], args['project'])
        security_parser = ComposerSecurityParser(args['symfony_bin'], args['project'])
        outdated = add_tuples(outdated, outdated_parser.gather_data())
        security_issues = add_tuples(security_issues, security_parser.gather_data())

    if args['spreadsheet_id'] and args['sheet']:
        writer = sheets.SheetWriter(args['spreadsheet_id'], args['sheet'])
        writer.send([[strftime("%Y-%m-%d %H:%M:%S", gmtime()), *outdated, *security_issues]])

    print(("Outdated: " + bcolors.GREEN + "%d Patches, " + bcolors.WARNING + "%d Minors, " + bcolors.FAIL + "%d Majors" + bcolors.ENDC) % outdated)
    print(("Security Issues: " + bcolors.BLUE + "%d Info, " + bcolors.GREEN + " %d Low, "  + bcolors.WARNING + "%d Moderate, " + bcolors.FAIL + "%d High, " + bcolors.BOLD + "%d Critical" + bcolors.ENDC) % security_issues)

def add_tuples(a, b):
    return tuple(map(sum, zip(a, b)))

if __name__ == '__main__':
    main()

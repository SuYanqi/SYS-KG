# SYSKG
Online proof-of-concept tool (SoapOperaTG): http://35.78.195.125:8000/#/

SoapOperaTG tool demo video: https://youtu.be/xcXmY8qGDSc

Usage Instructions
1. Search the seed bug ID by using the Search Bar
2. Select a relevant bug report from Relevant Bug Report panel
3. Use the generated soap opera tests in the Exploratory Testing panel to do soap opera testing on software under test (in our work, Firefox (Desktop) Browser)
<!-- Baseline tool: http://47.242.133.237:8092/#/ -->

Dataset link: https://drive.google.com/file/d/1gRkdAUZm6lTWfAJ9byqlR2wd_DQ0_sYl/view?usp=sharing

Directory prepare
1. Construct the data directory under the root directory

Dataset prepare
1. Download dataset from Dataset link
2. put the bugs.json into the data directory
3. put the ftl_files directory into the data directory
4. put the html_files directory into the data directory

Construct the system knowledge graph
1. run 1_filter_bugs.py
2. run 2_get_category_element_dict.py
3. run 3_construct_bug_kg.py

Start up Online proof-of-concept tool
1. Frontend: 
    a. cd client
    b. npm run serve -- --port 8090 (8090 replaced by the port number that you use)
2. Backend:
    a. python -m server.app

Start up Baseline tool
1. Frontend:
    a. cd baseline
    b. cd client_baseline
    c. npm run serve -- -- port 8092 (8092 replaced by the port number that you use)
2. Backend:
    a. python -m baseline.server_baseline.app

Bugs found during the tool development and user study

| No.      | Bug ID | Period |
| -------- | ------ | ------ |
| 1  | https://bugzilla.mozilla.org/show_bug.cgi?id=1744772 | tool development |
| 2  | https://bugzilla.mozilla.org/show_bug.cgi?id=1744892 | tool development |
| 3  | https://bugzilla.mozilla.org/show_bug.cgi?id=1744994 | tool development |
| 4  | https://bugzilla.mozilla.org/show_bug.cgi?id=1745731 | tool development |
| 5  | https://bugzilla.mozilla.org/show_bug.cgi?id=1746357 | tool development |
| 6  | https://bugzilla.mozilla.org/show_bug.cgi?id=1747076 | tool development |
| 7  | https://bugzilla.mozilla.org/show_bug.cgi?id=1747645 | tool development |
| 8  | https://bugzilla.mozilla.org/show_bug.cgi?id=1747871 | tool development |
| 9  | https://bugzilla.mozilla.org/show_bug.cgi?id=1747649 | tool development |
| 10 | https://bugzilla.mozilla.org/show_bug.cgi?id=1746394 | tool development |
| 11 | https://bugzilla.mozilla.org/show_bug.cgi?id=1746402 | tool development |
| 12 | https://bugzilla.mozilla.org/show_bug.cgi?id=1747991 | tool development |
| 13 | https://bugzilla.mozilla.org/show_bug.cgi?id=1747864 | tool development |
| 14 | https://bugzilla.mozilla.org/show_bug.cgi?id=1747759 | tool development |
| 15 | https://bugzilla.mozilla.org/show_bug.cgi?id=1745185 | tool development |
| 16 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764694 | tool development |
| 17 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764686 | tool development |
| 18 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764683 | tool development |
| 19 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764678 | tool development |
| 20 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764789 | tool development |
| 21 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765473 | tool development |
| 22 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765279 | tool development |
| 23 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765739 | tool development |
| 24 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765050 | tool development |
| 25 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764932 | tool development |
| 26 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765088 | tool development |
| 27 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764934 | tool development |
| 28 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764939 | tool development |
| 29 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765368 | tool development |
| 30 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765377 | tool development |
| 31 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765542 | tool development |
| 32 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765547 | tool development |
| 33 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764675 | tool development |
| 34 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764763 | tool development |
| 35 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764756 | tool development |
| 36 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764697 | tool development |
| 37 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764881 | tool development |
| 38 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765087 | tool development |
| 39 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765115 | tool development |
| 40 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765123 | tool development |
| 41 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765720 | tool development |
| 42 | https://bugzilla.mozilla.org/show_bug.cgi?id=1765688 | tool development |
| 43 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766387 | user study |
| 44 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766384 | user study |
| 45 | https://bugzilla.mozilla.org/show_bug.cgi?id=1767141 | user study |
| 46 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766141 | user study |
| 47 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766156 | user study |
| 48 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766143 | user study |
| 49 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766152 | user study |
| 50 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764864 | user study |
| 51 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766367 | user study |
| 52 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766229 | user study |
| 53 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766226 | user study |
| 54 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766579 | user study |
| 55 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766756 | user study |
| 56 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766554 | user study |
| 57 | https://bugzilla.mozilla.org/show_bug.cgi?id=1764787 | user study |
| 58 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766396 | user study |
| 59 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766557 | user study |
| 60 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766154 | user study |
| 61 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766763 | user study |
| 62 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766195 | user study |
| 63 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766205 | user study |
| 64 | https://bugzilla.mozilla.org/show_bug.cgi?id=1766437 | user study |

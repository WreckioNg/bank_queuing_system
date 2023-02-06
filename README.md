###############################################################
###############################################################

## Project Title
========== Bank Queuing System ==========

======== Bank of Singapore(BoS) =========

## Description
This project consists of 4 single page applications(SPA).

Each of them is designed to support a certain end of users.

Here is the diagram of our project structure:

bank_queuing_sys_master  (MSBA-GROUP-B1)
   ├── static/
   │   ├── css/
   │   │   ├── client.css
   │   │   ├── client_queue.css
   │   │   ├── counter_other.css
   │   │   ├── cro_gene.css
   │   │   ├── cro_reinitiate.css
   │   │   ├── cro_reset.css
   │   │   ├── cro_stop.css
   │   │   ├── cro_view.css
   │   │   ├── display.css
   │   │   ├── que_succ.css
   │   │   └── queue_fail.css
   │   ├── pics/
   │   └── templates/
   │       ├── client_fail.html
   │       ├── client_queue.html
   │       ├── client_suceed.html
   │       ├── Counter.html
   │       ├── CRO_general.html
   │       ├── CRO_reinitiate.html
   │       ├── CRO_reset.html
   │       ├── CRO_stop.html
   │       ├── CRO_view.html
   │       └── Display.html
   ├── data_structure.py
   └── server.py

Please make sure everything the application needs are put in the same folder.

The static folder contains css files， templates files and pictures files that supporting the templates.

The data_structure python file pre-defines the class object of bank service.

The server python file launches the application based on all the files above.

## Table of Contents

- [Installation]
- [Usage]
- [License]
- [Contact]
- [Acknowledgments]


## Installation
The whole process of implementation contains 5 steps.

1. Unfold the project zip and check everything inside follow the structure above.

2. Use `pip` or a wheel file to install all the supporting python library like flask, werkzeug.exceptions.

3. Use command `netstat -an` to check the available port in your localhost or cooperate server. Change the port accordingly.

4. Execute the `server.py` to launch the application. You can use `python server.py` in cmd under the corresponding routes.

5. Visit the localhost via Web Browser.(Currently supporting the latest version (2023-FEB-06) of MS Edge/Google Chrome/Firefox. 
   If you are using an older version or IE Explorer, some CSS style may not work correctly. Please follow the `IE_CSS_hack.png` to see solutions.

## Usage
Please refer to `Non-Technical Report.docx` for usage information.

## License
Copyright [2023] [MSBA-GROUP-B1]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Contact

Team Members:

Li Xuanfeng 	LI0073NG@e.ntu.edu.sg
Ni Wenhui 		NIWE0001@e.ntu.edu.sg
Qiao Sheng		SQIAO001@e.ntu.edu.sg
Wang Xinyu		XWANG079@e.ntu.edu.sg
Zhang Yuanfei 	ZHAN0592@e.ntu.edu.sg

Project Link:

https://github.com/xxxxx

## Acknowledgments

Instructor: Koh Choon Chye

Reference Links:

https://www.w3.org/
https://flask.palletsprojects.com/en/2.2.x/
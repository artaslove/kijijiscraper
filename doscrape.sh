#!/bin/bash
scrapy runspider kijijispider.py -t json --nolog -o - > kajiji.json
scp kajiji.json tony@tonyscc.ca:/home/tony/public_html/

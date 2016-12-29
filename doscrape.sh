#!/bin/bash
scrapy runspider kijijispider.py -t json --nolog -o - > kijiji.json

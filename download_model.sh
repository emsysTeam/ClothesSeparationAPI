#!/bin/sh
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1l7PUB8uAGRyqvZ0ti0ZACoI2CzJxOVoI' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1l7PUB8uAGRyqvZ0ti0ZACoI2CzJxOVoI" -O save_ckp_frozen.h5 && rm -rf /tmp/cookies.txt


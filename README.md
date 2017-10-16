# Python translation frontend for MS Translation API
Expects the following environment variable: `MS_TRANSLATION_API_KEY`

Easiest way to use this: Get the API key, create the following shell script as `ms-translation.sh`:
```bash
#!/bin/bash

export MS_TRANSLATION_API_KEY='YOUR API KEY HERE'

python ./ms-translation.py $@
```

Then, put your text to be translated in a file called `input.txt` and execute the script as follows:
```
./ms-translation.sh <input.txt >output.txt
```
Output will be stored in `output.txt`.
# add email sugar for the mailcow automation api


You will be needing these files

- firstnames.txt
- surnames.txt
- mailcow.apib 
- resources.json


Convert the apib into postman
```
bun install -g apib-to-postman
apib2postman mailcow.apib mailcow_collection.json
```

Using the postman json file and import into postman and export swagger files or visit the editors.
https://editor.swagger.io/

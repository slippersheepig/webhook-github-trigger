For my own purpose.
```bash
services:
  tgh:
    image: sheepgreen/tgh-trigger
    container_name: tgh
    environment:
      KEYWORDS: keywords seperated by comma
      GITHUB_REPO: <username>/<repo>
      GITHUB_TOKEN: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      WORKFLOW_FILE: xxx.yml
      TELEGRAM_TOKEN: 1234567890:abcdefghijklmnopqrstuvwxyz
    restart: always
```

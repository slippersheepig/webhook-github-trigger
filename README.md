For my own purpose.
```bash
services:
  ghook:
    image: sheepgreen/gh-webhook
    container_name: ghook
    environment:
      KEYWORDS: keywords seperated by comma
      GITHUB_REPO: <username>/<repo>
      GITHUB_TOKEN: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      WORKFLOW_FILE: xxx.yml
    restart: always
```

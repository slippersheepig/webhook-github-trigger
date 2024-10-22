For my own purpose.

webhook address: `http://<your-server-ip>:5000/webhook`
```bash
services:
  ghook:
    image: sheepgreen/gh-webhook
    container_name: ghook
    ports:
      - 5000:5000
    environment:
      KEYWORDS: keywords seperated by comma
      GITHUB_REPO: <username>/<repo>
      GITHUB_TOKEN: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      WORKFLOW_FILE: xxx.yml
      SSH_HOST: www.example.com
    restart: always
```

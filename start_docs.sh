#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 20
cd /opt/gitco/ai/my-agent/docs-site
npm start -- --host 0.0.0.0 --port 3001

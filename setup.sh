### SETUP file

cp .env.example .env

read -p 'Slack channel : ' slack_channel
read -sp 'Slack token: ' slack_token

# single line replacement so backup isn't inconsistent
sed -i .bak -e "s/your-slack-token/${slack_token}/g" -e "s/your-channel/${slack_channel}/g" .env
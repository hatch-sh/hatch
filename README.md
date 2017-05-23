# easyaws

awseasy is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

## HTTP(S) APIs

This uses API Gateway, AWS Lambda, and Route53 to build HTTP APIs.

    easywas api create # scaffolding
    easyaws api deploy # 0 config deployment to AWS
    easyaws api start # local development

## Static Websites

This uses S3, CloudFront, and Route53.

    easyaws website create # scaffolding
    easyaws website deploy
    easyaws website start

## Cron jobs


## Event handlers

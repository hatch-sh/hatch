# TODO

## General

- [ ] Figure out how to make this installable via `brew`
- [ ] Tag AWS resources?

## API

- [ ] Finish development server
  - [ ] Ensure that it reloads the modules on every request
  - [ ] Create proper mapping between HTTP => AWS Lambda event + context dicts

- [ ] Enable sharing of code between lambdas  
  Currently every lambda is deployed independently which means code can't be shared.
  Upload to S3 bucket and configure Lambdas accordingly?

- [ ] Supported nested/advanced routes.  
  Currently only flat URL are supported. It would be nice to supported nested URL and variables
  in the routes. My current thinking is that it's probably easiest with a little library for
  adding `@annotations` in the code that we can then extract

- [ ] Add support for APIGateway model checking  
  APIGateway can perform simple JSON schema checks on the request before passing it to the lambda.
  It would be cool to add these to the endpoints somehow (maybe through `@annotations`)

## Website

- [ ] Configure CloudFront as well?
- [ ] Configure Route53
- [ ] Create development static server  
  Not super important as most static site will have something like webpack-dev-server etc. but
  I think it's important anyhow.

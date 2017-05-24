import sys
import imp

import tornado.ioloop
import tornado.web


class LambdaHandler(tornado.web.RequestHandler):

    def initialize(self, code):
        self.code = code

    def get(self):
        sys.path.append(self.code)
        handler_module = imp.load_source('handler', '{}/handler.py'.format(self.code))

        # print self.request.method
        # print self.request.uri
        # print self.request.path
        # print self.request.headers
        # print self.request.body

        event = {
            'httpMethod': 'GET',
            'body': self.request.body
        }

        context = dict()

        response = handler_module.handle(event, context)

        for key, value in response['headers'].iteritems():
            self.add_header(key, value)

        self.set_status(response['statusCode'])
        self.write(response['body'])


def run(api, port):
    app = tornado.web.Application([
        (r"/{}".format(endpoint.route), LambdaHandler, dict(code=endpoint.code))
        for endpoint
        in api.endpoints
    ])
    app.listen(port)
    print 'Listening to http://localhost:{}'.format(port)
    tornado.ioloop.IOLoop.current().start()

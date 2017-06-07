import logging
import tornado.ioloop
import tornado.web

logger = logging.getLogger(__name__)


def serve_path(path, port):
    app = tornado.web.Application([
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': path}),
    ])
    app.listen(port)
    logger.info('Hatch is serving files on http://localhost:{}'.format(port))
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass

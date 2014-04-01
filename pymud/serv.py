""" TCP asyncio server
"""
import asyncio
import logging
import concurrent.futures

logger = logging.getLogger('aqua:server')

class TCPServer(object):
    """TCP server class"""

    def __init__(self, **options):
        options['max_request_line_size'] = options.get('max_request_line_size', 1024*2)
        self._bindings = dict()
        self.options = options

    def bind(self, host, port):
        limit = self.options['max_request_line_size']
        loop = self.options.get('loop', asyncio.get_event_loop())
        binding_gen = asyncio.start_server(self.handle_connection, host=host, port=port, loop=loop, limit=limit)
        self._bindings[(host, port)] = loop.run_until_complete(binding_gen)
        logger.info('Listening established on {0}'.format(self._bindings[(host, port)].sockets[0].getsockname()))

    def unbind(self, host, port):
        binding = self._bindings.pop((host, port), None)
        if binding:
            logger.info('Listening finished on {0}'.format(binding.sockets[0].getsockname()))
            binding.close()

    def unbindAll(self):
        for host, port in tuple(self._bindings.keys()):
            self.unbind(host, port)

    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        started_request = False
        missed_line = self.options.get('missed_line', 1)
        accept_timeout = self.options.get('accept_timeout', 5.0)
        shutdown_timeout = self.options.get('shutdown_timeout', 15.0)
        peername = writer.get_extra_info('peername')
        while True:
            timeout = shutdown_timeout if started_request else accept_timeout
            try:
                try:
                    # request_line = yield from asyncio.wait_for(reader.readline(), timeout)
                    request_line = yield from reader.readline()
                except ValueError:
                    logger.warning('Connection from {} closed by max max reading exceeded'.format(peername))
                    break
                if request_line:
                    if request_line == b'\r\n':
                        if missed_line > 0:
                            missed_line -= 1
                            continue
                        else:
                            logger.warning('Connection from {} sends empty request'.format(peername))
                            break
                    started_request = True
                    close_connection = yield from self.handle_request(reader, writer, self.options, request_line)
                    if close_connection:
                        break # normal closing connection
                else:
                    # logger.warning('Connection from {} closed by peer'.format(peername))
                    break
            except concurrent.futures.TimeoutError:
                if not started_request:
                    logger.warning('Connection from {} closed by timeout'.format(peername))
                break
        writer.close()

    @classmethod
    @asyncio.coroutine
    def handle_request(cls, reader, writer, options, request_line):
        """Must return `True` if connection need to close else `False`"""
        print(repr(request_line))
        command = request_line.decode('utf8').split()
        writer.write(bytes(str(command), encoding='utf8'))
        return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    loop = asyncio.get_event_loop()
    server = TCPServer(loop=loop)
    server.bind('127.0.0.1', 2007)
    server.bind('127.0.0.1', 2008)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.unbindAll()
        loop.close()

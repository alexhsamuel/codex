from   contextlib import closing
import os
import socket
import sys

# The default port for HTTP.
DEFAULT_PORT = 80


def _read_socket(sock):
    '''
    Reads all available data from a socket.
    '''
    msg = bytes()
    read_size = 8192
    while True:
        read = sock.recv(read_size)
        if len(read) > 0:
            msg += read
        else:
            # End of data.
            return msg


def send_request(host, port, msg):
    '''
    Sends a request on a new network connection and receives a response.

    Performs the following:
    - Creates a TCP network connection to 'port' on 'host'.
    - Once connected, sends 'msg'.
    - Reads data from the connection.
    - Closes the network connection.

    @type msg
      bytes
    @return
      The response message.
    @rtype
      bytes
    '''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.connect((host, port))
        sock.send(msg)
        return _read_socket(sock)


class GetError(RuntimeError):

    def __init__(self, status, reason):
        super().__init__("GET failed: {} ({})".format(status, reason))



def parse_authority(authority):
    '''
    Parses an HTTP authority.

    The authority may be a 'host:port' pair, where 'host' is a host name and
    'port' is a numerical port number, or just a host name, in which case the
    HTTP default port number is assumed.

    @return
      host, port
    '''
    if ':' in authority:
        host, port = authority.split(':', 1)
        # Convert the port number from a string to an integer.
        port = int(port)
    else:
        # No port given; use the default port.
        host = authority
        port = DEFAULT_PORT

    return host, port
    

def get(url):
    import urlparse, httpmsg

    parts = urlparse.parse(url)
    host, port = parse_authority(parts.authority)

    path = parts.full_path
    # If no path was specified, assume the default path, /.
    if path == '':
        path = '/'

    # Build a GET request with only the 'host' header, and an empty body.
    header = {'Host': host}
    request = httpmsg.Request('GET', path, header, b'')
    req_msg = httpmsg.format_request(request)
    # Send the request and get the response.
    resp_msg = send_request(host, port, req_msg)
    # Parse the response.
    response = httpmsg.parse_response(resp_msg)
    
    if response.status == 200:
        # Success.
        return response.body
    else:
        # Not successful; don't return data.
        raise GetError(response.status, response.reason)


#-------------------------------------------------------------------------------

if __name__ == "__main__":
    # Assume the command line consists of a single URL.
    _, url = sys.argv
    # Get web page.
    data = get(url)
    # Print the raw data, without decoding.
    os.write(1, data)




def get_error_code(client_error):
    """Get the error code from a ClientError (as errorfactory is magic).

    :param pool: the client error exception
    :type pool: :class:`~botocore.client.ClientError`
    :return: The error code or None
    """
    return client_error.response.get('Error', {}).get('Code')

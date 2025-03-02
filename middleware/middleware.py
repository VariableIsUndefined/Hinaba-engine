def fix_environ_middleware(app, url_prefix):
    def fixed_app(environ, start_response):
        path: str = environ['PATH_INFO']
        if path.startswith("/"):
            # strip extra slashes at the beginning of a path that starts
            # with any number of slashes
            path = "/" + path.lstrip("/")

        if url_prefix:
            # NB: url_prefix is guaranteed by the configuration machinery to
            # be either the empty string or a string that starts with a single
            # slash and ends without any slashes
            if path == url_prefix:
                # if the path is the same as the url prefix, the SCRIPT_NAME
                # should be the url_prefix and PATH_INFO should be empty
                path = ""
            else:
                # if the path starts with the url prefix plus a slash,
                # the SCRIPT_NAME should be the url_prefix and PATH_INFO should
                # the value of path from the slash until its end
                url_prefix_with_trailing_slash = url_prefix + "/"
                if path.startswith(url_prefix_with_trailing_slash):
                    path = path[len(url_prefix):]
        environ['SCIPT_NAME'] = url_prefix
        environ['PATH_INFO'] = path
        return app(environ, start_response)

    return fixed_app

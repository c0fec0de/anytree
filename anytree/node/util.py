def _repr(node, args=None):
    classname = node.__class__.__name__
    args = args or []
    for key, value in filter(lambda item: not item[0].startswith("_"),
                             sorted(node.__dict__.items(),
                                    key=lambda item: item[0])):
        args.append("%s=%r" % (key, value))
    return "%s(%s)" % (classname, ", ".join(args))

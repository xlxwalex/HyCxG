def str2bool(v):
    return v.lower() in ("true", "t", "1")

class ArgumentGroup(object):
    def __init__(self, parser, title, des):
        self._group = parser.add_argument_group(title=title, description=des)

    def add_arg(self, name, type, default, help, **kwargs):
        type = str2bool if type == bool else type
        self._group.add_argument(
            "--" + name,
            default=default,
            type=type,
            help=help + ' Default: %(default)s.',
            **kwargs)

class Args_trans(object):
    def __init__(self, args):
        self.args = args
        for k in args:
            if type(args[k]) == str:
                exec("self." + k + "='%s'" % args[k])
            elif type(args[k]) == int:
                exec("self." + k + "=%d" % args[k])
            elif type(args[k]) == float:
                exec("self." + k + "=%f" % args[k])
            elif type(args[k]) == bool:
                if args[k]:
                    exec("self." + k + "=True")
                else:
                    exec("self." + k + "=False")

    def __str__(self):
        for var in self.__dict__:
            print('>> {} : {}'.format(var, self.__dict__[var]))
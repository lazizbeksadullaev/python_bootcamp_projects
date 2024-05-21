class CallTypeMeta(type):
    def __new__(cls, name, *args):
        def __init__(self, **kwargs):
            assert(len(args) == len(kwargs))
            for arg in args:
                if arg.endswith('__int'):
                    suffix_removed_arg = arg.removesuffix('__int')
                    value = int(kwargs[suffix_removed_arg])
                    setattr(self, suffix_removed_arg, value)
                else:
                    setattr(self, arg, kwargs[arg])

        def __str__(self):
            args = {
                CallTypes.CLASS_NAME: self.__class__.__name__,
            } | self.__dict__
            return str(args)

        CallType = type(name, (), {})
        CallType.__init__ = __init__
        CallType.__str__ = __str__
        return CallType


class CallTypes():
    ARGS_SEP = '|'
    ARG_SEP = ':'
    CLASS_NAME = 'type'
    TestStart = CallTypeMeta('TestStart', 'test_id__int')
    TestBestResults = CallTypeMeta('TestBestResults', 'test_id__int')
    TestOnePage = CallTypeMeta('TestOnePage', 'test_result_id__int',
                               'page__int')
    TestOneOption = CallTypeMeta('TestOneOption', 'test_result_id__int',
                                 'test_one_id__int', 'option__int')
    TestFinish = CallTypeMeta('TestFinish', 'test_result_id__int')
    Test = CallTypeMeta('Test', 'test_id__int')
    TestResults = CallTypeMeta('TestResults', 'test_result_id__int',
                               'page__int')
    TestsListPage = CallTypeMeta('TestsListPage', 'page__int')
    Nothing = CallTypeMeta('Nothing')

    @classmethod
    def parse_data(cls, call_data: str):
        args = {}
        for arg in call_data.split(cls.ARGS_SEP):
            key, value = arg.split(cls.ARG_SEP)
            args[key] = value

        call_type_name = args.pop(cls.CLASS_NAME)
        for key, value in cls.__dict__.items():
            if key == call_type_name:
                class_ = value
                return class_(**args)

    @classmethod
    def make_data(cls, call_type):
        args = {
            cls.CLASS_NAME: call_type.__class__.__name__,
        } | call_type.__dict__
        call_data = cls.ARGS_SEP.join(
            map(lambda key: f'{key}{cls.ARG_SEP}{args[key]}', args)
        )
        return call_data

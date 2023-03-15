import inspect


class ApiConfig:

    @classmethod
    def get_attributes(cls):
        """
        获取类属性，以字典形式返回
        @return: dict
        """
        attributes = inspect.getmembers(cls, predicate=lambda a: not (inspect.isroutine(a)))
        return {d[0]: d[1] for d in attributes if not (d[0].startswith('__') and d[0].endswith('__'))}


class A(ApiConfig):
    a = "aaaaaa"
    b = "bbbbbb"
    c = {
        "key_c": "value_c"
    }


    @staticmethod
    def abc():
        print("abc")


if __name__ == '__main__':

    test_a = A.get_attributes()
    print(test_a)







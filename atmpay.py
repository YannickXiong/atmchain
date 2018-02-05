import requests
import time
import hashlib
from abc import ABCMeta, abstractclassmethod
import yaml


__URL__ = "'https://api.atmchain.io/v2"
__HEADERS__ = {
    "Content-Type": "application/json; charset=utf-8",
}


# exceptions
class Error(Exception):
    """
    Base class for exceptions in business module.

    Exception raised when action is invalid.

       Attributes:
           err_msg -- error message
           origin_exception -- origin exception
       """

    def __init__(self, err_msg=None, origin_exception=None):
        self.err_msg = err_msg
        self.origin_exception = origin_exception

    def __str__(self):
        exception_msg = "Exception: %s" % self.err_msg

        if self.origin_exception is not None:
            exception_msg += " Origin exception: %s." % self.origin_exception

        return exception_msg


class RequestMethodError(Error):
    """
    Exception raised when method invalid.
        See __INTERFACE__ to see the valid interface.
    """

    pass


def now():
    """
    返回unix时间，单位为毫秒
    :return:
    """
    _unix_time = time.time()
    _second = int(_unix_time)
    _million_second = int((_unix_time - _second) * 1000)

    return _second * 1000 + _million_second


def send_request(method, url, params=None, data=None, headers=None):
    """
    发送http请求
    :param method:
    :param url:
    :param params:
    :param data:
    :param headers:
    :return:
    """
    try:
        if method == "get":
            response = requests.get(url=url, headers=headers, params=params, data=data)
        elif method == "head":
            response = requests.head(url=url, headers=headers, params=params, data=data)
        elif method == "post":
            response = requests.post(url=url, headers=headers, params=params, data=data)
        elif method == "put":
            response = requests.put(url=url, headers=headers, params=params, data=data)
        elif method == "patch":
            response = requests.patch(url=url, headers=headers, params=params, data=data)
        elif method == "delete":
            response = requests.delete(url=url, headers=headers, params=params, data=data)
        elif method == "options":
            response = requests.options(url=url, headers=headers, params=params, data=data)
        else:
            raise RequestMethodError("%s is invalid to requests." % method)
            # 如果else分支写一个pass，则print引用了response.status_code就会抛出一个warming
            # Local variable 'response' might be referenced before assignment
            # 原因： 如果代码不幸走到了else，则response确实可能没定义就引用了啊。
            # 当有了raise则不会，因为raise后的代码不会被执行到，就不存在这个问题了。
        # print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        # pprint.pprint('Response HTTP Response Body: {content}'.format(content=response.content.decode()))

        response.raise_for_status()  # checking if status_code == 200
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def load_cases(file):
    try:
        with open(file) as fp:
            _data = yaml.load(fp)

        return _data
    except Exception as e:
        raise e


class Signature(metaclass=ABCMeta):
    """
        签名基本类
    """

    def __init__(self, data):
        self.data = data or {}

    def capture_finger_point(self, escape=list("sign")):
        """
        提取data中的特征信息，生成成待加密的指纹串
        :param escape: 指定不参与指纹生成的属性
        :return:
        """

        if not self.data:   # empty {}
            return None

        if escape is None:
            escape = ["sign"]   # 默认的sign永远不参与签名

        if "sign" not in escape:
            escape.append("sign")

        _finger_point = ""
        _keys = sorted(list(self.data.keys()))

        for key in _keys:
            if key in escape:   # 跳过那些不参与计算sign的签名
                continue
            _finger_point += key
            _finger_point += "="
            _finger_point += str(self.data[key])
            _finger_point += "&"

            _finger_point = _finger_point[:-1]

        return _finger_point

    @staticmethod
    def sha256(finger_point=None):
        """

        :param finger_point: 待生成签名的指纹信息，格式同capture_finger_point返回
        :return: 返回签名
        """

        # finger_point为None的时候默认使用字字符加密，这么设计是因为调用方capture_finger_point有可能返回None
        finger_point = finger_point or ""
        _hash = hashlib.sha256()
        _hash.update(finger_point.encode('utf-8'))

        return _hash.hexdigest()

    @abstractclassmethod
    def generate_signature(self):
        """
        根据特征码生成对应的签名信息
        :return:
        """
        pass


class TransactionSign(Signature):
    """
        用途： 用于APP接口/transaction的签名生成
    """

    def __init__(self, data):
        super(TransactionSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point(escape=["detail"]))


class AuthSign(Signature):
    """
        用途： 用于APP接口/auth的签名生成
    """

    def __init__(self, data):
        super(AuthSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class UserLoginSign(Signature):
    """
        用途： 用于WEB接口/user/login的签名生成
    """

    def __init__(self, data):
        super(UserLoginSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class UserTokenSign(Signature):
    """
        用途： 用于WEB接口/user/token的签名生成
    """

    def __init__(self, data):
        super(UserTokenSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class MerchantChangPassWDSign(Signature):
    """
        用途： 用于WEB接口/user/changpwd的签名生成
    """

    def __init__(self, data):
        super(MerchantChangPassWDSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class MerchantSign(Signature):
    """
        用途： 用于WEB接口/merchant的签名生成
    """

    def __init__(self, data):
        super(MerchantSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class MerchantAuditSign(Signature):
    """
        用途： 用于WEB接口/merchant/audit的签名生成
    """

    def __init__(self, data):
        super(MerchantAuditSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class MerchantWithdrawSign(Signature):
    """
        用途： 用于WEB接口/merchant/withdraw的签名生成
    """

    def __init__(self, data):
        super(MerchantWithdrawSign, self).__init__(data)

    def generate_signature(self):

        return super().sha256(self.capture_finger_point())


class ATMInterface(metaclass=ABCMeta):

    def __init__(self, method=None, url=None, headers=None, auth_token=None, params=None, data=None):
        self.method = method
        self.url = url or __URL__
        self.headers = headers or __HEADERS__
        self.auth_token = auth_token
        self.params = params
        self.data = data
        self.response = None

    def send_request(self):
        self.response = send_request(
            url=self.url,
            method=self.method,
            params=self.params,
            headers=self.headers,
            data=self.data)

    @abstractclassmethod
    def check_results(self):
        pass

    def run(self):
        self.send_request()
        self.check_results()


class Auth(ATMInterface):
    """
    App认证接口，返回token
        调用方：第三方App
    """

    def __init__(self, **kwargs):
        super(Auth, self).__init__(**kwargs)

    def check_results(self):
        assert self.response["result"] == "success"
        assert self.response["expire"] == 7200

    def get_token(self):
        _token = self.response.get("token", None)
        return _token


class ATMInterfaceEngine(metaclass=ABCMeta):

    def __init__(self, method=None, url=None, headers=None, auth_token=None, params=None, data=None):
        self.method = method
        self.url = url or __URL__
        self.headers = headers or __HEADERS__
        self.auth_token = auth_token
        self.params = params
        self.data = data

        self.signature = None
        self.params_all = {}

    @abstractclassmethod
    def url_prepare(self):
        pass

    @abstractclassmethod
    def auth_token_prepare(self):
        pass

    @abstractclassmethod
    def method_prepare(self):
        pass

    @abstractclassmethod
    def params_prepare(self):
        pass

    @abstractclassmethod
    def headers_prepare(self):
        pass

    @abstractclassmethod
    def data_prepare(self):
        pass

    @abstractclassmethod
    def signature_prepare(self):
        pass

    def params_all_prepare(self):
        self.params_all = self.__dict__
        # 去掉底层接口(interface->request)不相干的参数
        self.params_all.pop("params_all")
        self.params_all.pop("signature")

    def prepare(self):
        self.url_prepare()

        self.method_prepare()

        self.auth_token_prepare()
        self.headers_prepare()

        self.params_prepare()

        self.signature_prepare()
        self.data_prepare()

        self.params_all_prepare()

    def get_params_all(self):
        return self.params_all


class AuthEngine(ATMInterfaceEngine):

    def url_prepare(self):
        pass

    def auth_token_prepare(self):
        pass

    def method_prepare(self):
        self.method = "get"

    def headers_prepare(self):
        pass

    def data_prepare(self):
        _test_data = load_cases("./testCases/app/auth.yaml")
        _test_data["timestamp"] = now()

        self.data = _test_data

    def signature_prepare(self):
        _sign = AuthSign(self.data)
        _signature = _sign.generate_signature()

        self.signature = _signature

    def params_prepare(self):

        # 对于request.get方法，参数在params，而非data中传递
        self.data["sign"] = self.signature

    def token_prepare(self):
        pass


auth = AuthEngine()
print(auth.params_all)









import hashlib

def get_md5(info):
    if isinstance(info ,str):
        info = info.encode('utf-8')
    m = hashlib.md5()
    m.update(info)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5("2134123"))

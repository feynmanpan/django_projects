

class MSG:
    count = 0

    @classmethod
    def printmsg(cls, msg):
        cls.count += 1
        print(f'{cls.count}. {msg}')

    @classmethod
    def prt_msgs(cls, msgs: list):
        for msg in msgs:
            cls.printmsg(msg)

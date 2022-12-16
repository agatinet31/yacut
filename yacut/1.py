def f1():
    try:
        1/0
    except:
        print('f1')
    finally:
        print('complete!')


def f2():
    try:
        f1()
    except:
        print('f2')


f2()
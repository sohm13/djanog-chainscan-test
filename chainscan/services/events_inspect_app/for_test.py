
class A: 

    a = 'a'
    def print_class(self):
        # print(self.__name__)
        print(self.__class__)


class B(A):

    b= 'b'
    





print(A().__dir__())
print(B().__dir__())


A().print_class()
B().print_class()
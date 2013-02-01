def SecureResource(func):
    def secureResource(self):
        func(self)


    return secureResource
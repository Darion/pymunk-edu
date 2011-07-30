import re

class Parser():
    @staticmethod
    def get_type():
        pass
    @staticmethod
    def get_params():
        pass
    @staticmethod
    def parse(string):
        reg = '(set) (\w*)=(\w*)'
        regobj = re.match(reg, string)
        if(regobj != None):
            return {
                    'type': regobj.group(1),
                    'params': [
                        regobj.group(2),
                        regobj.group(3),
                    ]
                }

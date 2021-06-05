

class CSVItemType:
    
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def match_item(self, current_char_name: str) -> str:
        '''
        匹配到条目时
        '''
        raise NotImplementedError
    
    def switch_next_item(self) -> str:
        '''
        将要切换到下一个条目时
        '''
        raise NotImplementedError
    
    def get_declaration(self) -> str:
        """
        关于变量如何声明
        """
        raise NotImplementedError

    def get_enum_name(self) -> str:
        return 'E' + self.var_name.capitalize()

    def line_end(self) -> str:
        '''
        行结束时发生点什么
        '''
        return ''

class CSVIgnore(CSVItemType):
    def match_item(self, current_char_name: str):
        return ''
    def switch_next_item(self):
        return ''


class CSVInteger(CSVItemType):

    def __init__(self, var_name: str, bits: int, signed=False) -> None:
        """
        bits: 8 -> uint8/int8, 32 -> uint32/int32
        signed: signed int
        """
        super().__init__(var_name)
        assert bits in [8, 16, 32, 64]
        self.bits = bits
        
        self.signed = signed


class CSVDecimal(CSVInteger):
    
    def __init__(self, var_name: str, bits: int, signed=False) -> None:
        super().__init__(var_name, bits, signed=signed)

    def get_declaration(self) -> str:
        type = f"{'' if self.signed else 'u'}int{self.bits}_t"
        return f"{type} {self.var_name} = 0;"

    def match_item(self, current_char_name: str) -> str:
        return f"{self.var_name} = {self.var_name} + {current_char_name} - '0';"

    def switch_next_item(self) -> str:
        return ""

class CSVString(CSVItemType):
    pass


class CSVASCIISring(CSVString):
    pass


class CSVFixedASCIISring(CSVASCIISring):
    pass


class CSVLimitedASCIISring(CSVASCIISring):
    pass


class CSVUnlimitedASCIISring(CSVASCIISring):
    pass

from csv_types import *


class CSVRowDef:

    def __init__(self, row_items: list[CSVItemType], sep=',', ignore_blank=False, current_col_name='current_col') -> None:
        assert len(sep) == 1, 'only use 1-length sep'
        self.sep = sep
        self.row_items = row_items
        self.ignore_blank = ignore_blank
        self.current_col_name = current_col_name

    @staticmethod
    def _generate_switch(switch_from: str, case_contents: dict[list[str], list[str]], defalut_content: str = ''):
        cases = ''

        for k, v in case_contents.items():
            cases += f"case {k}: \n{v}\nbreak;\n"
        
        default = ''
        if defalut_content:
            default = f'defalue: \n{defalut_content}\nbreak;'

        return '''switch (%(switch_from)s) {
    %(cases)s
    %(default)s
}
        ''' % {'switch_from': switch_from, 'cases': cases, 'default': default}

    def generate(self):
        _enums = [i.get_enum_name() for i in self.row_items]
        enums = '''enum col_item {\n    %s\n}\n''' % (', '.join(_enums)) + ';'

        open_file = f'''
boost::iostreams::mapped_file mmap(file_name, boost::iostreams::mapped_file::readonly);
auto f = mmap.const_data();
auto l = f + mmap.size();
        '''

        declarations =(
            "\n".join([i.get_declaration() for i in self.row_items]) + 
            '\n' + 
            f'int {self.current_col_name} = 0;\n'
        )

        switch_next_item_contents = []
        for i, e in zip(self.row_items, _enums[1:]):
            switch_next_item_contents.append(
                i.switch_next_item() + '\n' + f'{self.current_col_name} = {e};'
            )


        switch_next_item_switch = self._generate_switch(
            self.current_col_name, 
            dict([(e, c) for e, c in zip(_enums[:-1], switch_next_item_contents)])
        )
        on_line_end = "\n".join([i.line_end() for i in self.row_items])


        match_item_contents = [i.match_item(self.current_col_name) for i in self.row_items]

        match_item_contents_switch = self._generate_switch(
            self.current_col_name, 
            dict([(e, m) for e, m in zip(_enums, match_item_contents)])
        )

        main_loop = '''
%(open_file)s

%(declarations)s

while (f && f != l) {
    switch (*f) {
        case %(sep)d: // sep is [%(sep_char)s]
            %(switch_next_item_switch)s
        case '\\n':
            %(last_switch_next)s
            %(on_line_end)s
        default: 
            %(match_item_contents_switch)s
            break;
        f++;
    }

}
        ''' % {
            'sep': ord(self.sep), 'sep_char': self.sep, 
            'switch_next_item_switch': switch_next_item_switch, 
            'last_switch_next': self.row_items[-1].switch_next_item(),
            'on_line_end': on_line_end + f'{self.current_col_name} = {_enums[0]};',
            'match_item_contents_switch': match_item_contents_switch,
            'open_file': open_file,
            'declarations': declarations
        }
        codes = '''
#include <cstdint>
#include <boost/iostreams/device/mapped_file.hpp>


%(enums)s
void parser(char* file_name) {
    %(main_loop)s
}
        ''' % {'enums': enums, 'main_loop': main_loop}
        return codes
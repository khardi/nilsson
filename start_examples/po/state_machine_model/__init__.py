from start_examples.po.state_machine_model.commands import ParsePathCommand, ParseIdCommand, ParseStrCommand
from start_examples.po.state_machine_model.event import Event
from start_examples.po.state_machine_model.state import State

waiting_new_line = State('waiting_new_line')
new_line_finded = Event('new_line_finded')


waiting_paths = State('waiting_paths')
paths_finded = Event('paths_finded')


waiting_msgid = State('waiting_msgid')
waiting_msgid.add_command('parse_path')
msgid_finded = Event('msgid_finded')


waiting_msgstr = State('waiting_msgstr')
waiting_msgstr.add_command('parse_msgid')
msgstr_finded = Event('msgstr_finded')


waiting_new_line.add_transition(target=waiting_paths, event=new_line_finded)
waiting_paths.add_transition(target=waiting_msgid, event=paths_finded)
waiting_msgid.add_transition(target=waiting_msgstr, event=msgid_finded)
waiting_msgstr.add_transition(target=waiting_new_line, event=msgstr_finded)

command_channel = {
    'parse_path': ParsePathCommand('parse_path'),
    'parse_msgid': ParseIdCommand('parse_msgid'),
    'parse_msstr': ParseStrCommand('parse_msstr'),
}

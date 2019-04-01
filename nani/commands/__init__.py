from .command import CommandManager
from .template import template
from .category import category
from .gallery import gallery
from .help import help
from .refresh import refresh

command_manager = CommandManager()
command_manager.add_command(template)
command_manager.add_command(category)
command_manager.add_command(gallery)
command_manager.add_command(help)
command_manager.add_command(refresh)

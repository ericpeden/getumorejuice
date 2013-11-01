# Copyright (C) 2013  Eric Peden
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import simplejson as json

from pelican import signals
from pelican.contents import Content, is_valid_content
from pelican.generators import Generator
from pelican.readers import BaseReader
from pelican.signals import signal

from . import parsers

logger = logging.getLogger('__name__')

signals.recipe_generator_init = signal('recipe_generator_init')
signals.recipe_generator_finalized = signal('recipe_generator_finalized')
signals.recipe_generator_preread = signal('recipe_generator_preread')
signals.recipe_generator_context = signal('recipe_generator_context')

class Recipe(Content):
    mandatory_properties = ('title', 'ingredients')
    default_template = 'recipe'

class RecipeReader(BaseReader):
    enabled = True
    file_extensions = ['recipe']
    
    def read(self, filename):
        with open(filename) as f:
            recipe = parsers.parse_recipe(f.read())
            
        parsed = {}
        
        for key, value in recipe.iteritems():
            parsed[key] = self.process_metadata(key, value)
            
        return json.dumps(recipe), parsed
        
class RecipesGenerator(Generator):
    """Generate pages"""

    def __init__(self, *args, **kwargs):
        self.recipes = []
        super(RecipesGenerator, self).__init__(*args, **kwargs)
        signals.recipe_generator_init.send(self)

    def generate_context(self):
        all_recipes = []
        for f in self.get_files(
                self.settings.get('RECIPE_DIR', 'recipes'),
                exclude=self.settings.get('RECIPE_EXCLUDES', ())):
            try:
                recipe = self.readers.read_file(
                    base_path=self.path, path=f, content_class=Recipe,
                    context=self.context,
                    preread_signal=signals.recipe_generator_preread,
                    preread_sender=self,
                    context_signal=signals.recipe_generator_context,
                    context_sender=self)
            except Exception as e:
                logger.warning('Could not process {}\n{}'.format(f, e))
                continue

            if not is_valid_content(recipe, f):
                continue

            self.add_source_path(recipe)
            all_recipes.append(recipe)

        self.recipes = all_recipes

        self._update_context(('recipes', ))
        self.context['RECIPES'] = self.recipes

        signals.recipe_generator_finalized.send(self)

    def generate_output(self, writer):
        for recipe in self.recipes:
            writer.write_file(recipe.save_as, self.get_template(recipe.template),
                    self.context, recipe=recipe,
                    relative_urls=self.settings['RELATIVE_URLS'],
                    override_output=hasattr(recipe, 'override_save_as'))
    
    
def add_readers(readers):
    readers.reader_classes['recipe'] = RecipeReader
    
def add_generators(generators):
    return RecipesGenerator
    
def debug_context(gen, metadata):
    print metadata

def register():
    signals.readers_init.connect(add_readers)
    signals.get_generators.connect(add_generators)
    signals.article_generator_context.connect(debug_context)
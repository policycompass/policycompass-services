from django.core.management.base import BaseCommand, CommandError
from apps.searchmanager import index_utils

class Command(BaseCommand):
    args = 'Type of item (or items) to index (metric,visualization,event).Leave empty for all'
    help = 'Rebuilds the elastic search index for metrics,events,visualizations,FCMs'

    def handle(self, *args, **options):
            try:
                #if the user has provided arguments
                self.stdout.write(index_utils.update_index_item('metric',26))
                import pdb;pdb.set_trace()
                if args:
                  for itemtype in args:
                     self.stdout.write('Indexing started for ' + itemtype + '.Please wait a few minutes')
		     #Call the Rebuild Index util for the specific item type
                     res = index_utils.rebuild_index_itemtype(itemtype)
                else:
                    self.stdout.write('Indexing started for all item types.Please wait a few minutes')
                    #Call the Rebuild Index util for all item types
                    res = index_utils.rebuild_index()
            except Exception as e:
                raise CommandError(str(e))

            self.stdout.write(res)
            self.stdout.write('Indexing finished.')

from django.core.management.base import BaseCommand, CommandError
from apps.searchmanager import index_utils

class Command(BaseCommand):
    #args = '<parameters>'
    help = 'Rebuilds the elastic search index for metrics,events,visualizations,FCMs'

    def handle(self, *args, **options):
            try:
				#Call the Rebuild Index util
                res = index_utils.rebuild_index()
            except Exception as e:
                raise CommandError(str(e))

            self.stdout.write(res)

from django.core.management.base import BaseCommand, CommandError
from product.models import ZCategory, ZProduct

# DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(DIR_BASE)
# sys.path.append(DIR_BASE)
# from zopynfacts import products
from zopynfacts import products


class Command(BaseCommand):
    help = 'Initialize or alternately Update Product module database'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        categories_dct = products.download_categories('fr', 'fr')
        print('Categories count:', categories_dct['count'])

        for poll_id in options['poll_ids']:
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully read poll "%s"' % poll_id))
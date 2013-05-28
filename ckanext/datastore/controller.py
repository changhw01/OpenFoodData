import StringIO
import unicodecsv as csv

import pylons

import ckan.plugins as p
import ckan.lib.base as base
import ckan.model as model

LARGE_NUMBER = 1e12


class DatastoreController(base.BaseController):
    def dump(self, resource_id):
        context = {
            'model': model,
            'session': model.Session,
            'user': p.toolkit.c.user
        }

        data_dict = {
            'resource_id': resource_id,
            'limit': LARGE_NUMBER
        }

        action = p.toolkit.get_action('datastore_search')
        result = action(context, data_dict)

        pylons.response.headers['Content-Type'] = 'text/csv'
        pylons.response.headers['Content-disposition'] = \
            'attachment; filename="{name}.csv"'.format(name=resource_id)
        f = StringIO.StringIO()
        wr = csv.writer(f, encoding='utf-8')

        header = [x['id'] for x in result['fields']]
        wr.writerow(header)

        for record in result['records']:
            wr.writerow([record[column] for column in header])
        return f.getvalue()
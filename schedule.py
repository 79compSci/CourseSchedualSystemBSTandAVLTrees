import csv
from search_trees import BSTMap, AVLTreeMap
from schedule_item import ScheduleItem

class Schedule:
    def __init__(self, backend='BST'):
        self.backend = backend.upper()
        self.map = {'BST': BSTMap, 'AVL': AVLTreeMap}[self.backend]()
        self.rows = self.duplicates = 0
        self.errors = []

    def load(self, path):
        fresh = Schedule(self.backend)
        with open(path, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            if not {'Subject', 'Catalog', 'Section', 'Instructor'} <= set(reader.fieldnames or []):
                raise ValueError('Missing required CSV headers')
            for number, row in enumerate(reader, 2):
                fresh.rows += 1
                if None in row or any(v is None for v in row.values()) or any(not row[k].strip() for k in ('Subject','Catalog','Section')):
                    fresh.errors.append(f'Row {number}: malformed record')
                    continue
                item = ScheduleItem.from_row(row)
                if fresh.map.search(item.key) is not None:
                    fresh.duplicates += 1
                fresh.map.insert(item.key, item)
        self.__dict__.update(fresh.__dict__)

    def find(self, subject, catalog, section):
        return self.map.search(tuple(x.strip().upper() for x in (subject,catalog,section)))

    def items(self):
        return [item for _, item in self.map.inorder_items()]

    def filter(self, subject='', catalog='', section='', instructor=''):
        subject, catalog, section = (x.strip().upper() for x in (subject,catalog,section))
        surname = instructor.strip().casefold()
        return [item for item in self.items() if
                (not subject or item.subject == subject) and
                (not catalog or item.catalog == catalog) and
                (not section or item.section == section) and
                (not surname or item.instructor.split(',')[0].strip().casefold() == surname)]

    def height(self):
        return self.map.height()

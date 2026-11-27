from dataclasses import dataclass

@dataclass(frozen=True)
class ScheduleItem:
    subject: str
    catalog: str
    section: str
    instructor: str
    details: tuple = ()

    @property
    def key(self):
        return self.subject, self.catalog, self.section

    @classmethod
    def from_row(cls, row):
        fields = tuple((k, v.strip()) for k, v in row.items())
        return cls(*(row[k].strip().upper() for k in ('Subject', 'Catalog', 'Section')),
                   row['Instructor'].strip(), fields)

    def __str__(self):
        return f'{self.subject:6} {self.catalog:7} {self.section:8} {self.instructor}'

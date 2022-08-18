class Attachment:
    def __init__(self, id=None, bug_id=None, summary=None, description=None, file_name=None, content_type=None):
        self.id = id
        self.bug_id = bug_id
        self.summary = summary
        self.description = description
        self.file_name = file_name
        self.content_type = content_type
        self.url = f"https://bug{bug_id}.bmoattachments.org/attachment.cgi?id={id}"

    def __repr__(self):
        return f'{self.id} - {self.bug_id} - {self.url} ' \
               f'- {self.summary} - {self.description} - ' \
               f'{self.file_name} - {self.content_type}'

    def __str__(self):
        return f'{self.id} - {self.bug_id} - {self.url} ' \
               f'- {self.summary} - {self.description} - ' \
               f'{self.file_name} - {self.content_type}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

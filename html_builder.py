class HtmlBuilder:

    def __init__(self, tracks, filename):
        self.tracks = tracks
        self.html_file = filename
        self.building = None

    def build(self):
        try:
            self.building = open(self.html_file, "a")

            print("<html>", file=self.building)

            for key in self.tracks:
                records = self.tracks[key]
                if len(records) > 0:
                    self.write_header(key, len(records))
                    self.start_table()

                    for record in records:
                        self.add_record(record)

                    self.end_table()

                    print("<html>", file=self.building)
        finally:
            self.building.close()

    def write_header(self, header, size):
        print("<h1>{} ({})</h1>".format(header, size), file=self.building)

    def start_table(self):
        print("<ul>", file=self.building)

    def end_table(self):
        print("</ul>", file=self.building)

    def add_record(self, record):
        print("<li>{}</li>".format(record), file=self.building)
# SQL Table Definition

from functools import reduce

# Converts a single foreign key into a SQL statement of the form:
# `FOREIGN KEY [atts] REFERENCES [table][atts]
def fk_to_string(fk):
    (my_atts, foreign_table, foreign_atts) = fk

    return "FOREIGN KEY(`" + \
    "`, `".join(str(a) for a in my_atts) + \
    "`) REFERENCES `" + \
    foreign_table + "`(`" + \
    "`, `".join(str(a) for a in foreign_atts) + \
    "`)"

# Corresponds to a MySQL table that supports primary and foreign keys and only INT attributes.
# It consists of four member variables:
#   * [name] The name of the table (unique identifier/slug)
#   * [attributes] The set of string-valued attributes in this table
#   * [primary_key] The set of string-valued attributes that form the primary key of this table
#   * [foreign_keys] The set of foreign keys. Each foreign key is a three-tuple of:
#       - An ordered tuple of attributes in this table to which the FK is applied
#       - The name of the table that the foreign key should reference
#       - An ordered tuple of attributes in the foreign table that are being referenced
class Table:
    name = 'T'
    attributes = set()
    primary_key = set()
    foreign_keys = set()
    def __init__(self, name, attributes, primary_key, foreign_keys):
        self.name = name
        self.attributes = attributes
        self.primary_key = primary_key
        self.foreign_keys = foreign_keys
    def __str__(self):
        return "CREATE TABLE `" + \
        self.name + \
        "`(" + \
        (("`" + "` INT, `".join(self.attributes) + "` INT") if len(self.attributes) > 0 else "") + \
        ")" + \
        ((", PRIMARY KEY(`" + "`, `".join(self.primary_key) + "`)") if len(self.primary_key) > 0 else "") + \
        (", " + ", ".join([fk_to_string(fk) for fk in self.foreign_keys]) if len(self.foreign_keys) > 0 else "") + \
        ");"
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(self.name) ^ reduce(lambda x,y: x^y, [hash(x) for x in self.attributes])
    def __eq__(self, other):
        return \
        self.name == other.name and \
        self.attributes == other.attributes and \
        self.primary_key == other.primary_key and \
        self.foreign_keys== other.foreign_keys

# Corresponds to an entire MySQL database of tables
# It consists of just one member variable:
#   * An unordered list of the Table objects that make up this database
class Database:
    tables = []
    def __init__(self, tables):
        self.tables = tables
    def __eq__(self, other):
        return set( self.tables ) == set( other.tables )


# An example instantiation of the Database class.

sample_db = Database([ \
    Table('A', set(['a1','a2','c1']), set(['a1']), set([(('c1',), 'C', ('c1',))])), \
    Table('B', set(['b1','b2']), set(['b1']), set()), \
    Table('C', set(['c1', 'c2']), set(['c1']), set()), \
    Table('R1', set(['a1','b1','x']), set(['a1','b1']), \
        set([(('a1',), 'A', ('a1',)), (('b1',), 'B', ('b1',))]))])

sample_db1 = Database([ \
    Table('A', set(['a1']), set(['a1']), set())])

sample_db2 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1', 'a2']), set())])

sample_db3 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a2']), set())])

sample_db4 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1']), set()), \
    Table('B', set(['b1', 'b2']), set(['b2']), set()), \
    Table('R1', set(['a1', 'b2']), set(['a1', 'b2']), \
        set([ (('a1',), 'A', ('a1',)), (('b2',), 'B', ('b2',)) ]))])

sample_db5 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1']), set()), \
    Table('B', set(['b1', 'b2']), set(['b2']), set()), \
    Table('R1', set(['a1', 'b2', 'x']), set(['a1', 'b2', 'x']), \
        set([ (('a1',), 'A', ('a1',)), (('b2',), 'B', ('b2',)) ]))])

sample_db6 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1']), set()), \
    Table('B', set(['b1', 'b2']), set(['b2']), set()), \
    Table('R1', set(['a1', 'b2', 'x1', 'x2']), set(['a1', 'b2', 'x2']), \
        set([ (('a1',), 'A', ('a1',)), (('b2',), 'B', ('b2',)) ]))])

sample_db7 = Database([ \
    Table('A', set(['a1', 'a2', 'b2']), set(['a1']), set([ (('b2',), 'B', ('b2',)) ])), \
    Table('B', set(['b1', 'b2']), set(['b2']), set())])

sample_db8 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1']), set()), \
    Table('B', set(['b1', 'b2']), set(['b2']), set()), \
    Table('R1', set(['a1', 'b2', 'x']), set(['a1','x']), \
        set([ (('a1',), 'A', ('a1',)), (('b2',), 'B', ('b2',)) ]))])

sample_db9 = Database([ \
    Table('A', set(['a1', 'a2']), set(['a1']), set()), \
    Table('B', set(['b1', 'b2', 'a1']), set(['b2', 'a1']), set([ (('a1',), 'A', ('a1',)) ]))])

sample_db10 = Database([ \
    Table('A', set(['a1', 'a2', 'b2']), set(['a1', 'b2']), set([ (('b2',), 'B', ('b2',)) ])), \
    Table('B', set(['b1', 'b2']), set(['b2']), set())])

sample_db21 = Database([ \
    Table('A', set(['a1', 'a2', 'b2', 'c1']), set(['a1', 'b2', 'c1']), set([ (('b2',), 'B', ('b2',)), (('c1',), 'C', ('c1',)) ])), \
    Table('B', set(['b1', 'b2', 'c1', 'd2']), set(['b2', 'c1']), set([ (('d2',), 'D', ('d2',)), (('c1',), 'C', ('c1',)) ])), \
    Table('C', set(['c1', 'c2']), set(['c1']), set()), \
    Table('D', set(['d1', 'd2']), set(['d2']), set())])

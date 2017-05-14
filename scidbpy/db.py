"""
Connect to SciDB
----------------

Connect to SciDB using "connect()" or "DB()":

>>> db = connect()
>>> db = DB()


Display information about the "db" object:

>>> db
DB('http://localhost:8080', None, None, None, None, None)

>>> print(db)
scidb_url  = 'http://localhost:8080'
scidb_auth = None
http_auth  = None
role       = None
namespace  = None
verify     = None


Provide Shim credentials:

>>> db_ha = connect(http_auth=('foo', 'bar'))

>>> db_ha
DB('http://localhost:8080', None, ('foo', PASSWORD_PROVIDED), None, None, None)

>>> print(db_ha)
scidb_url  = 'http://localhost:8080'
scidb_auth = None
http_auth  = ('foo', PASSWORD_PROVIDED)
role       = None
namespace  = None
verify     = None

To prompt the user for the password, use:

# >>> import getpass
# >>> db_ha = connect(http_auth=('foo', getpass.getpass()))
# Password:


Use SSL:

>>> db_ssl = connect('https://localhost:8083', verify=False)

>>> print(db_ssl)
scidb_url  = 'https://localhost:8083'
scidb_auth = None
http_auth  = None
role       = None
namespace  = None
verify     = False

See Python "requests" library SSL Cert Verification section [1] for
details on the "verify" parameter.

[1] http://docs.python-requests.org/en/master/user/advanced/
    #ssl-cert-verification


Use SSL and SciDB credentials:

>>> db_sdb = connect(
...   'https://localhost:8083', scidb_auth=('foo', 'bar'), verify=False)

>>> print(db_sdb)
scidb_url  = 'https://localhost:8083'
scidb_auth = ('foo', PASSWORD_PROVIDED)
http_auth  = None
role       = None
namespace  = None
verify     = False



Access SciDB Arrays
-------------------

Access SciDB arrays using "db.arrays":

>>> iquery(db, 'create array foo<x:int64>[i=0:2]')

>>> dir(db.arrays)
... # doctest: +ELLIPSIS
[...'foo']

>>> iquery(db, 'remove(foo)')

>>> dir(db.arrays)
[]

Arrays specified explicitly are not checked:

>>> db.arrays.foo
'foo'
>>> db.arrays.bar
'bar'

In IPython, you can use <TAB> for auto-completion of array names:

# In []: db.arrays.<TAB>
# In []: db.arrays.foo


Use "iquery" function
---------------------

Use "iquery" to execute queries:

>>> iquery(db, 'store(build(<x:int64>[i=0:2], i), foo)')


Use "iquery" to download array data:

>>> iquery(db, 'scan(foo)', fetch=True)
... # doctest: +NORMALIZE_WHITESPACE
array([(0, (255, 0)), (1, (255, 1)), (2, (255, 2))],
      dtype=[('i', '<i8'), ('x', [('null', 'u1'), ('val', '<i8')])])

Optionally, download only the attributes:

>>> iquery(db, 'scan(foo)', fetch=True, atts_only=True)
... # doctest: +NORMALIZE_WHITESPACE
array([((255, 0),), ((255, 1),), ((255, 2),)],
      dtype=[('x', [('null', 'u1'), ('val', '<i8')])])

>>> iquery(db, 'remove(foo)')


Download operator output directly:

>>> iquery(db, 'build(<x:int64 not null>[i=0:2], i)', fetch=True)
... # doctest: +NORMALIZE_WHITESPACE
array([(0, 0), (1, 1), (2, 2)],
      dtype=[('i', '<i8'), ('x', '<i8')])

Optionally, download only the attributes:

>>> iquery(db,
...        'build(<x:int64 not null>[i=0:2], i)',
...        fetch=True,
...        atts_only=True)
... # doctest: +NORMALIZE_WHITESPACE
array([(0,), (1,), (2,)],
      dtype=[('x', '<i8')])


If dimension names collide with attribute names, unique dimension
names are created:

>>> iquery(db, 'apply(build(<x:int64 not null>[i=0:2], i), i, i)', fetch=True)
... # doctest: +NORMALIZE_WHITESPACE
array([(0, 0, 0), (1, 1, 1), (2, 2, 2)],
      dtype=[('i_1', '<i8'), ('x', '<i8'), ('i', '<i8')])


If schema is known, it can be provided to "iquery":

>>> iquery(db,
...        'build(<x:int64 not null>[i=0:2], i)',
...        fetch=True,
...        schema=Schema(None,
...                      (Attribute('x', 'int64', not_null=True),),
...                      (Dimension('i', 0, 2),)))
... # doctest: +NORMALIZE_WHITESPACE
array([(0, 0), (1, 1), (2, 2)],
      dtype=[('i', '<i8'), ('x', '<i8')])

>>> iquery(db,
...        'build(<x:int64 not null>[i=0:2], i)',
...        fetch=True,
...        atts_only=True,
...        schema=Schema.fromstring('<x:int64 not null>[i=0:2]'))
... # doctest: +NORMALIZE_WHITESPACE
array([(0,), (1,), (2,)],
      dtype=[('x', '<i8')])


Download as Pandas DataFrame:

>>> iquery(db,
...        'build(<x:int64>[i=0:2], i)',
...        fetch=True,
...        as_dataframe=True)
... # doctest: +NORMALIZE_WHITESPACE
   i x
0  0 0.0
1  1 1.0
2  2 2.0

>>> iquery(db,
...        'build(<x:int64>[i=0:2], i)',
...        fetch=True,
...        atts_only=True,
...        as_dataframe=True)
... # doctest: +NORMALIZE_WHITESPACE
   x
0  0.0
1  1.0
2  2.0

>>> iquery(db,
...        'build(<x:int64>[i=0:2], i)',
...        fetch=True,
...        atts_only=True,
...        as_dataframe=True,
...        dataframe_promo=False)
... # doctest: +NORMALIZE_WHITESPACE
   x
0  (255, 0)
1  (255, 1)
2  (255, 2)


Use SciDB Operators
-------------------

>>> dir(db)
... # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
[...'aggregate',
 ...'apply',
 ...
 ...'xgrid']

>>> db.apply
... # doctest: +NORMALIZE_WHITESPACE
SciDB(db=DB('http://localhost:8080', None, None, None, None, None),
      operator='apply', args=[])

>>> print(db.apply)
apply()

>>> db.missing
Traceback (most recent call last):
    ...
AttributeError: 'DB' object has no attribute 'missing'

In IPython, you can use <TAB> for auto-completion of operator names:

# In []: db.<TAB>
# In []: db.apply

>>> db.create_array('foo', '<x:int64>[i]')
>>> dir(db.arrays)
... # doctest: +ELLIPSIS
[...'foo']

>>> db.remove(db.arrays.foo)
>>> dir(db.arrays)
[]

>>> db.build('<x:int8>[i=0:2]', 'random()')
... # doctest: +NORMALIZE_WHITESPACE
SciDB(db=DB('http://localhost:8080', None, None, None, None, None),
      operator='build', args=['<x:int8>[i=0:2]', 'random()'])
"""

import copy
import enum
import itertools
import logging
import numpy
import pandas
import re
import requests

from .schema import Attribute, Dimension, Schema


class Shim(enum.Enum):
    cancel = 'cancel'
    execute_query = 'execute_query'
    new_session = 'new_session'
    read_bytes = 'read_bytes'
    release_session = 'release_session'


class Password_Placeholder(object):
    def __repr__(self):
        return 'PASSWORD_PROVIDED'


class DB(object):
    """SciDB Shim connection object.

    >>> DB()
    DB('http://localhost:8080', None, None, None, None, None)

    >>> print(DB())
    scidb_url  = 'http://localhost:8080'
    scidb_auth = None
    http_auth  = None
    role       = None
    namespace  = None
    verify     = None
    """

    _show_query = "show('{}', 'afl')"

    def __init__(
            self,
            scidb_url='http://localhost:8080',
            scidb_auth=None,
            http_auth=None,
            role=None,
            namespace=None,
            verify=None):
        self.scidb_url = scidb_url
        self.role = role
        self.namespace = namespace
        self.verify = verify

        if http_auth:
            self._http_auth = requests.auth.HTTPDigestAuth(*http_auth)
            self.http_auth = (http_auth[0], Password_Placeholder())
        else:
            self._http_auth = self.http_auth = None

        if scidb_auth:
            if not self.scidb_url.lower().startswith('https'):
                raise Exception(
                    'SciDB credentials can only be used ' +
                    'with https connections')

            self._scidb_auth = {'user': scidb_auth[0],
                                'password': scidb_auth[1]}
            self.scidb_auth = (scidb_auth[0], Password_Placeholder())
        else:
            self._scidb_auth = self.scidb_auth = None

        self.arrays = Arrays(self)

        self.operators = self.iquery_readlines(
            "project(list('operators'), name)")
        self.operators.extend(('arrays', 'iquery', 'iquery_readlines'))
        self.operators.sort()

    def __iter__(self):
        return (i for i in (
            self.scidb_url,
            self.scidb_auth,
            self.http_auth,
            self.role,
            self.namespace,
            self.verify))

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            type(self).__name__, *self)

    def __str__(self):
        return '''\
scidb_url  = '{}'
scidb_auth = {}
http_auth  = {}
role       = {}
namespace  = {}
verify     = {}'''.format(*self)

    def __getattr__(self, name):
        if name in self.operators:
            return SciDB(self, name)
        else:
            raise AttributeError(
                '{.__name__!r} object has no attribute {!r}'.format(
                    type(self), name))

    def __dir__(self):
        return self.operators

    def iquery(self,
               query,
               fetch=False,
               atts_only=False,
               as_dataframe=False,
               dataframe_promo=True,
               schema=None):
        """Execute query in SciDB

        :param bool fetch: If `True`, download SciDB array (default
        `False`)

        :param bool atts_only: If `True`, download only SciDB array
        attributes without dimensions (default `False`)

        :param bool as_dataframe: If `True`, return a Pandas
        DataFrame. If `False`, return a NumPy array (default `False`)

        :param bool dataframe_promo: If `True`, nullable types are
        promoted as per Pandas promotion scheme
        http://pandas.pydata.org/pandas-docs/stable/gotchas.html
        #na-type-promotions If `False`, object records are used for
        nullable types (default `True`)

        :param schema: Schema of the SciDB array to use when
        downloading the array. Schema is not verified. If schema is a
        Schema instance, it is copied. Otherwise, a :py:class:`Schema`
        object is built using :py:func:`Schema.fromstring` (default
        `None`).

        >>> DB().iquery('build(<x:int64>[i=0:1; j=0:1], i + j)', fetch=True)
        ... # doctest: +NORMALIZE_WHITESPACE
        array([(0, 0, (255, 0)),
               (0, 1, (255, 1)),
               (1, 0, (255, 1)),
               (1, 1, (255, 2))],
              dtype=[('i', '<i8'), ('j', '<i8'),
                     ('x', [('null', 'u1'), ('val', '<i8')])])

        """
        id = self._shim(Shim.new_session).text

        if fetch:
            # Use provided schema or get schema from SciDB
            if schema:
                # Deep-copy schema since we might be mutating it
                if isinstance(schema, Schema):
                    sch = copy.deepcopy(schema)
                else:
                    sch = Schema.fromstring(schema)
            else:
                # Execute 'show(...)' and Download text
                self._shim(
                    Shim.execute_query,
                    id=id,
                    query=DB._show_query.format(query.replace("'", "\\'")),
                    save='tsv')
                sch = Schema.fromstring(
                    self._shim(Shim.read_bytes, id=id, n=0).text)
                logging.debug(sch)

            # Unpack
            if not atts_only:
                if sch.make_dims_unique():
                    # Dimensions renamed due to collisions. Need to
                    # cast.
                    query = 'cast({}, {:h})'.format(query, sch)

                query = 'project(apply({}, {}), {})'.format(
                    query,
                    ', '.join('{0}, {0}'.format(d.name) for d in sch.dims),
                    ', '.join(i.name for i in itertools.chain(
                        sch.dims, sch.atts)))

                sch.make_dims_atts()
                logging.debug(query)
                logging.debug(sch)

            # Execute Query and Download content
            self._shim(
                Shim.execute_query, id=id, query=query, save=sch.atts_fmt)
            buf = self._shim(Shim.read_bytes, id=id, n=0).content

            self._shim(Shim.release_session, id=id)

            # Scan content and build (offset, size) metadata
            off = 0
            buf_meta = []
            while off < len(buf):
                meta = []
                for att in sch.atts:
                    sz = att.itemsize(buf, off)
                    meta.append((off, sz))
                    off += sz
                buf_meta.append(meta)

            # Create NumPy record array
            if as_dataframe and dataframe_promo:
                ar = numpy.empty((len(buf_meta),),
                                 dtype=sch.get_promo_atts_dtype())
            else:
                ar = numpy.empty((len(buf_meta),), dtype=sch.atts_dtype)

            # Extract values using (offset, size) metadata
            # Populate NumPy record array
            pos = 0
            for meta in buf_meta:
                ar.put((pos,),
                       tuple(att.frombytes(
                           buf,
                           off,
                           sz,
                           promo=as_dataframe and dataframe_promo)
                             for (att, (off, sz)) in zip(sch.atts, meta)))
                pos += 1

            # Return NumPy array or Pandas dataframe
            if as_dataframe:
                return pandas.DataFrame.from_records(ar)
            else:
                return ar

        else:                   # fetch=False
            self._shim(Shim.execute_query, id=id, query=query, release=1)

    def iquery_readlines(self, query):
        """Execute query in SciDB

        >>> DB().iquery_readlines('build(<x:int64>[i=0:2], i * i)')
        ... # doctest: +ELLIPSIS
        [...'0', ...'1', ...'4']

        >>> DB().iquery_readlines(
        ...   'apply(build(<x:int64>[i=0:2], i), y, i + 10)')
        ... # doctest: +ELLIPSIS
        [...'0', ...'10', ...'1', ...'11', ...'2', ...'12']
        """
        id = self._shim(Shim.new_session).text
        self._shim(Shim.execute_query, id=id, query=query, save='tsv')
        ret = self._shim(Shim.read_bytes, id=id, n=0).text.split()
        self._shim(Shim.release_session, id=id)

        return ret

    def _shim(self, endpoint, **kwargs):
        """Make request on Shim endpoint"""
        if self._scidb_auth and endpoint in (Shim.cancel, Shim.execute_query):
            kwargs.update(self._scidb_auth)
        req = requests.get(
            requests.compat.urljoin(self.scidb_url, endpoint.value),
            params=kwargs,
            auth=self._http_auth,
            verify=self.verify)
        req.reason = req.content
        req.raise_for_status()
        return req


class Arrays(object):
    """Access to arrays available in SciDB"""
    def __init__(self, db):
        self._db = db
        self._schema = Schema(
            atts=(Attribute('name', 'string', not_null=True),),
            dims=(Dimension('i'),))

    def __getattr__(self, name):
        return str(name)

    def __dir__(self):
        """Download the list of SciDB arrays. Use 'project(list(), name)' to
        download only names and schemas
        """
        return self._db.iquery_readlines('project(list(), name)')


class SciDB(object):
    """Unevaluated SciDB expression"""
    def __init__(self, db, operator, *args):
        self.db = db
        self.operator = operator

        self.args = list(args)
        self.is_lazy = self.operator.lower() not in (
            'create_array', 'remove')

    def __call__(self, *args):
        """Returns self for lazy expressions. Executes immediate expressions.
        """
        self.args = list(args)

        if self.operator.lower().startswith('create_array') \
           and len(self.args) < 3:
            # Set temporary = False for create array
            self.args.append(False)

        if self.is_lazy:
            return self
        else:
            return self.db.iquery(str(self))

    def __repr__(self):
        return '{}(db={!r}, operator={!r}, args=[{}])'.format(
            type(self).__name__,
            self.db,
            self.operator,
            ', '.join('{!r}'.format(i) for i in self.args))

    def __str__(self):
        args_fmt = ('{}'.format(i) for i in self.args)
        return '{}({})'.format(self.operator, ', '.join(args_fmt))


connect = DB
iquery = DB.iquery


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

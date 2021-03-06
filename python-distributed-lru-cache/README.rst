========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
.. |version| image:: https://img.shields.io/pypi/v/distributed-lru-cache.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/distributed-lru-cache

.. |wheel| image:: https://img.shields.io/pypi/wheel/distributed-lru-cache.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/distributed-lru-cache

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/distributed-lru-cache.svg
    :alt: Supported versions
    :target: https://pypi.org/project/distributed-lru-cache

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/distributed-lru-cache.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/distributed-lru-cache



.. end-badges

An example package. Geo Distributed LRU (Least Recently Used) cache with expiration time

* Free software: BSD 3-Clause License

Installation
============

::

    pip install distributed-lru-cache

You can also install the in-development version with::

    pip install https://github.com/pcu4dros/pedro_cuadros_test/python-distributed-lru-cache/archive/master.zip


Documentation
=============

=======
Project
=======

We want to optimize every bits of software we write. Your goal is to write a new library that can
be integrated to our stack. Dealing with network issues everyday, latency is our biggest problem.
Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with
time expiration. This library will be used extensively by many of our services so it needs to meet
the following criteria::

  1 - Simplicity. Integration needs to be dead simple.
      [covered, this is an standard library]
  2 - Resilient to network failures or crashes.
      [covered, using redis]
  3 - Near real time replication of data across Geolocation. Writes need to be in real time.
      [covered, using redis, replication of the data occurs in near real time and writes on redis are considered in real time]
  4 - Data consistency across regions
      [covered, using redis, the data is always consistent through the database]
  5 - Locality of reference, data should almost always be available from the closest region
      [partially covered, an additional iteration is needed in order to indicate on which region/instance/etc the data will be obtained]
  6 - Flexible Schema
      [is a flexible schema, keys are stored in strings and values to, but the data could be parsed from an specific structure or model]
  7 - Cache can expire
      [partially covered, the expiration functionality is rusty and need to be more flexible and robust]


=================
How does it work?
=================

This Distributed LRU Cache:

An LRU cache is an efficient cache data structure that can be used to figure out what we should evict when the cache is full. The goal is to always have the least-recently used item accessible in O(1) time.

========================
LRU Cache Implementation
========================

To create the LRU logic were necessary to use the following collections, data structures and tools:

Deque
=============

A double-ended queue, or deque, supports adding and removing elements from either end.

collections.deque::
    Returns a new deque object initialized left-to-right (using append()) with data from iterable. If iterable is not specified, the new deque    is empty.

Deques are a generalization of stacks and queues (the name is pronounced “deck” and is short for “double-ended queue”). Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

Dictionary
=============

A dictionary is used to map or associate things you want to store the keys you need to get them. A dictionary in Python is just like a dictionary in the real world. Python Dictionary are defined into two elements Keys and Values.

    Keys will be a single element
    Values can be a list or list within a list, numbers, etc.

Redis
=============

Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

This library use HASHes
=======================

Redis HASHes store a mapping of keys to values. The values that can be stored in HASHes are the same as what can be stored as normal STRINGs: strings themselves.

Note: This in order to maintain the data backed on a in-memory database and speed up the writes and replications.

Life cycle of the methods
=========================
life-cycle of a PUT::

    The item is created/updated on the queue using a dictionary
    LRU cache is updated (item is bumped up if it already exists)
    Validates the capacity of the cache and remove the Last Recently Used key if no more space is found using the popleft() command
    Validates if the key is in the cache instance and remove that key in order to create it again:
       - Create the key again on the local instance and redis
    If a ttl(Time to live) was given, the item will expire in that amount of time


life-cycle of a GET::

    LRU cache is checked for item, if it exists item is returned (item is bumped up) and the queue using the following steps:
    - Remove the item from the queue
    - Remove the key from redis hash
    - Append the node again on the queue
    - Create the key on redis hash again
    - Obtain the value from the node/key and the value is returned


=====
Usage
=====

To use Distributed LRU Cache in a project::


	from distributed_lru_cache.cache import LRUCache

        lru = LRUCache(capacity=2, cache_name='lrucache', redis_host='localhost', redis_port=6379, redis_db=0, ttl=5)

        lru.put('10', '1')
        lru.put('20', '1', ttl=1)
        lru.get('10')



Where::

   capacity: The capacity of the cache instance (128 by default)
   cache_name: The name of the cache instance to create ('lrucache' by default)
   redis_host: The host name of redis server ('localhost' by default)
   redis_port: The port of redis server (6379 by default)
   redis_db: The database to use on redis (0 by default)
   ttl: time to live, the expiration time (0 by default = No expiration)


methods::

   put: To create a cache item into the cache instance could have an extra argument (ttl) to expire this specific item
   get: The obtain a cache item altering the order of the items
   peek: The obtain a cache item without altering the order of the items
   set_redis_conn: To instantiate a specific redis connection after the item creation
   clear_cache_instance: To clear the entire cache instance


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

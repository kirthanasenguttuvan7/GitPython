# util.py
# Copyright (C) 2008, 2009 Michael Trier (mtrier@gmail.com) and contributors
#
# This module is part of GitPython and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php
"""
Module for general utility functions
"""
import re
from git.actor import Actor

def get_object_type_by_name(object_type_name):
	"""
	Returns
		type suitable to handle the given object type name.
		Use the type to create new instances.
		
	``object_type_name``
		Member of TYPES
		
	Raises
		ValueError: In case object_type_name is unknown
	"""
	if object_type_name == "commit":
		import commit
		return commit.Commit
	elif object_type_name == "tag":
		import tag
		return tag.TagObject
	elif object_type_name == "blob":
		import blob
		return blob.Blob
	elif object_type_name == "tree":
		import tree
		return tree.Tree
	else:
		raise ValueError("Cannot handle unknown object type: %s" % object_type_name)
		
	
# precompiled regex
_re_actor_epoch = re.compile(r'^.+? (.*) (\d+) .*$')

def parse_actor_and_date(line):
	"""
	Parse out the actor (author or committer) info from a line like::
	
	 author Tom Preston-Werner <tom@mojombo.com> 1191999972 -0700
	
	Returns
		[Actor, int_seconds_since_epoch]
	"""
	m = _re_actor_epoch.search(line)
	actor, epoch = m.groups()
	return (Actor._from_string(actor), int(epoch))
	
	
	
class ProcessStreamAdapter(object):
	"""
	Class wireing all calls to the contained Process instance.
	
	Use this type to hide the underlying process to provide access only to a specified 
	stream. The process is usually wrapped into an AutoInterrupt class to kill 
	it if the instance goes out of scope.
	"""
	__slots__ = ("_proc", "_stream")
	def __init__(self, process, stream_name):
		self._proc = process
		self._stream = getattr(process, stream_name)
	
	def __getattr__(self, attr):
		return getattr(self._stream, attr)
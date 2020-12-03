#!/usr/bin/env python3
import pdb, traceback, sys
import json
import config
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from collections import defaultdict
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Set, Dict
import pathlib
import copy
from bs4 import BeautifulSoup
posts_by_hashtag = defaultdict(set)
hashtag_counter = Counter()

def default_field(obj):
  return field(default_factory=lambda: copy.copy(obj))

@dataclass
class GPlusPost:
  path: pathlib.Path
  post: Dict = default_field({})
  content: str = None
  hashtags: Set[str] = default_field(set([]))
  soup: BeautifulSoup = None

  def __post_init__(self):
    with self.path.open() as f:
      self.post = json.load(f)
    self.content = self.post.get('content')
    if self.content:
      self.set_soup()
      for hashtag_link in self.soup.select('.ot-hashtag'):
        hashtag = hashtag_link.text.split('#')[1]
        self.hashtags.add(hashtag)

  def set_soup(self):
    if self.content:
      self.soup = BeautifulSoup(self.content, features="html.parser", from_encoding='utf-8')

  def __hash__(self):
    return hash(repr(str(self.path.resolve())))

  def __getstate__(self):
    state = self.__dict__.copy()
    del state['soup']
    return state

  def __setstate__(self, d):
    self.__dict__ = d
    self.set_soup()

def main():
  # for post_path in config.gplus_all_imported_posts_path.glob('20120820_-_FiXato_s_Favourite_Mac_OS_X_Apps_Just_p.json'):
  if config.hashtag_counter_path.exists() and config.posts_by_hashtag_path.exists():
    posts_by_hashtag, hashtag_counter = restore()
  else:
    for post_path in config.gplus_all_imported_posts_path.glob('*.json'):
      print(f"""Processing post at {str(post_path)}""")
      post = GPlusPost(path = post_path)
      if (len(post.hashtags) > 0):
        for hashtag in post.hashtags:
          print(f"""Hashtag: {hashtag}""")
          hashtag_counter[hashtag.lower()] += 1
          posts_by_hashtag[hashtag.lower()].add(post)
        print(posts_by_hashtag.keys())
        store('hashtag_counter')
    store()
  for (hashtag, count) in hashtag_counter.most_common(50):
    hashtags_for_post = list(posts_by_hashtag[hashtag])[0].hashtags
    hashtags_with_capitals = [post_hashtag for post_hashtag in hashtags_for_post if post_hashtag.lower() == hashtag and post_hashtag != post_hashtag.lower()]
    hashtag_with_capitals = hashtags_with_capitals[0] if hashtags_with_capitals else hashtag
    print(f"""{count} {hashtag_with_capitals}""")
  breakpoint()

def print_posts_for_hashtag(hashtag, posts_by_hashtag):
  print('\n\n'.join([html2text(post.content) for post in posts_by_hashtag[hashtag.lower()]]))

def restore():
  with open(config.posts_by_hashtag_path) as f:
    posts_by_hashtag = load(f, Loader=Loader)
  with open(config.hashtag_counter_path) as f:
    hashtag_counter = load(f, Loader=Loader)
  return posts_by_hashtag, hashtag_counter

def store(data_types=None):
  if not data_types:
    data_types = ['posts_by_hashtag', 'hashtag_counter']
  if 'posts_by_hashtag' in data_types:
    print(f"""Storing {len(posts_by_hashtag.keys())} keys to {config.posts_by_hashtag_path}""")
    with open(config.posts_by_hashtag_path, 'w+') as f:
      f.write(dump(posts_by_hashtag, Dumper=Dumper, default_flow_style=False, allow_unicode=True))
  if 'hashtag_counter' in data_types:
    print(f"""Storing to {config.hashtag_counter_path}""")
    with open(config.hashtag_counter_path, 'w+') as f:
      f.write(dump(hashtag_counter, Dumper=Dumper, default_flow_style=False, allow_unicode=True))

if __name__ == '__main__':
  try:
    main()
  except Exception as err:
    extype, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)

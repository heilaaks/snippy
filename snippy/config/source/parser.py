#!/usr/bin/env python3

"""parser.py: Parse config source parameters."""

import re


class Parser(object):
    """Parse configuration source parameters."""

    @staticmethod
    def keywords(keywords, sort_=True):
        """Parse user provided keyword list. The keywords are tags or search
        keywords. User may use various formats so each item in a list may be
        for example a string of comma separated tags.

        The dot is a special case. It is allowed for the regexp to match and
        print all records."""

        # Examples: Support processing of:
        #           1. -t docker container cleanup
        #           2. -t docker, container, cleanup
        #           3. -t 'docker container cleanup'
        #           4. -t 'docker, container, cleanup'
        #           5. -t dockertesting', container-managemenet', cleanup_testing
        #           6. --sall '.'
        list_ = []
        for tag in keywords:
            list_ = list_ + re.findall(r"[\w\-\.]+", tag)

        if sort_:
            list_ = sorted(list_)

        return tuple(list_)

    @staticmethod
    def links(links):
        """Parse user provided link list. Because URL and keyword have different
        forbidden characters, the methods to parse keywords are simular but still
        they are separated. URLs can be separated only with space and bar. These
        are defined 'unsafe characters' in URL character set /1/.

        /1/ https://perishablepress.com/stop-using-unsafe-characters-in-urls/"""

        # Examples: Support processing of:
        #           1. -l link1 link2
        #           2. -l link1| link2| link3
        #           3. -l link1|link2|link3
        #           4. -l 'link1 link2 link3'
        #           5. -l 'link1| link2| link3'
        #           6. -l 'link1|link2|link3'
        #           7. -l '.'
        list_ = []
        for link in links:
            list_ = list_ + re.split(r"[\s+|+]", link)

        sorted_list = sorted(list_)

        return tuple(sorted_list)

import re


class PatternParser:
    """
    Parses a pattern and provides method parse_text to find patterns in a list of lines (from file iteration)
    """

    # TO DO: add Flags support
    def __init__(self, search_pattern: str, use_regex=False):
        """
        Initialises  PatternParser with new pattern

        :param search_pattern: str either not compiled regex or simple string
        :param use_regex: whether to escape the string for use in regex or not
        """

        self.use_regex = use_regex

        search_pattern_lines = search_pattern.splitlines()

        # We will use regex for search anyway, so escape it if it is not meant to be a regex
        if not self.use_regex:
            search_pattern_lines = [re.escape(search_pattern_line) for search_pattern_line in search_pattern_lines]

        self.search_pattern_lines = [re.compile(search_pattern_line) for search_pattern_line in search_pattern_lines]

        self.possible_patterns = dict()
        self.current_text_line = ''

    def reset(self):
        """
        Use, if you start new text

        :return:
        """
        self.possible_patterns = dict()
        self.current_text_line = ''

    def _parse_first_lines(self):
        """
        Finds occurrences of first line of pattern and populates self.possible_patterns with Possible Patterns

        TO DO: Works first come first save – so with pattern

        x
        y
        x

        and text

        x
        y
        x
        y
        x

        only one (the first) occurrence will be found

        x
        y
        x  x
           y
           x

        will work however

        """

        first_line_pattern = self.search_pattern_lines[0]
        start = 0
        while True:
            match = first_line_pattern.search(self.current_text_line, start)
            if match is None:
                break
            position = match.start()
            if position not in self.possible_patterns:   # Assuming First come, first serve
                self.possible_patterns[position] = PotentialPattern(self.search_pattern_lines, position)
            start = match.end()

    def _continue_parsing_possible_objects(self) -> int:
        """
        Triggers parsing of current line for Possible Patterns and returns found complete occurrences
        :return: int found completed patterns
        """

        positions_to_remove = set()
        found = 0

        for position, possible_pattern in self.possible_patterns.items():

            result = possible_pattern.parse_line(self.current_text_line)

            if result is False:
                positions_to_remove.add(position)               # Pattern did not continue - remove
                continue
            if result is None:
                continue                                        # Nothing to do
            if result is True:
                found += 1
                positions_to_remove.add(position)               # pattern is finished - count and free slot
                continue

        self.possible_patterns = {position: self.possible_patterns[position] for position in
                                  self.possible_patterns.keys() if position not in positions_to_remove}

        return found

    def parse_text(self, text_line: str) -> int:
        """
        Use to parse line from the text, where you are searching your patterns in it.
        :param text_line: the unit of text to look in
        :return: int found completed patterns
        """
        self.current_text_line = text_line
        self._parse_first_lines()
        return self._continue_parsing_possible_objects()


class PotentialPattern:
    """
    Keeps track if a pattern is followed over multiple strings (lines of a file for example)
    """

    def __init__(self, regex_list: list, start: int):
        """
        Initialises a potential pattern, with a list of compiled regular expression and the position where to start looking …
        :param regex_list: a list of compiled regexes, in order of appearance
        :param start: Wwere to start looking
        """

        self.regex_list = regex_list
        self.start = start
        self.line_number = 0
        self.lines = len(regex_list)

    def parse_line(self, line_text: str):
        """
        Parse a line of text, to see if it (contains) the patterns
        :param line_text: The line of text to parse
        :return: False if pattern was not found, None if pattern is ont yet complete and True if pattern is completed
        """
        regex = self.regex_list[self.line_number]
        self.line_number += 1

        match = regex.match(line_text, self.start)

        if match is None:  # no match, no fun
            return False
        if self.line_number is self.lines and match:  # last line and match: Winner
            return True
        if self.line_number < self.lines and match:  # still uncertain, but keep on going
            return None
        else:
            raise Exception(self)  # No clue what is going on – debug!

import os
import sys

p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, p + '\\' + p.split('\\')[-1])
sys.path.insert(0, p)


from bagel.ingest import (
    form_data_reader, lower_first_letter, has_alphanumeric_last,
    remove_white_space_and_trailing_punctuation, str2list,
    remove_left_white_space, str2list
)

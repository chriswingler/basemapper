import unittest
import sys
import os

# Adjust sys.path to include the parent directory (root of the repository)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basemapper import create_file_id

class TestCreateFileId(unittest.TestCase):

    def test_simple_path(self):
        self.assertEqual(create_file_id("path/to/file.txt"), "file_path_to_file_txt")

    def test_path_with_spaces(self):
        # Uses \s from the regex r"[/\.\\\s\(\)\[\]\{\}:;,'\"`!@#\$%\^&\*\+=\|~]"
        self.assertEqual(create_file_id("my path with spaces/file name.py"), "file_my_path_with_spaces_file_name_py")

    def test_path_with_mixed_case(self):
        self.assertEqual(create_file_id("Path/To/File.TXT"), "file_path_to_file_txt")

    def test_already_safe_path(self):
        self.assertEqual(create_file_id("normal_file_name"), "file_normal_file_name")

    def test_empty_string(self):
        self.assertEqual(create_file_id(""), "file_")

    def test_leading_trailing_chars_replaced(self):
        # ./file. -> should become file___file_
        # / is replaced, . is replaced by the regex r"[/\.\\\s..."
        self.assertEqual(create_file_id("./file."), "file___file_")

    def test_comprehensive_special_chars(self):
        # This test uses the regex believed to be in basemapper.py:
        # r"[/\.\\\s\(\)\[\]\{\}:;,'\"`!@#\$%\^&\*\+=\|~]"
        # Which replaces: / \ . \s ( ) [ ] { } : ; , ' " ` ! @ # $ % ^ & * + = | ~
        test_str = r"test/path\with spaces.and(all)[these]{chars}:;, '\"`!@#$%^&*+=|~end.txt"
        # Expected:
        # test / path \ with (space) spaces . and ( all ) [ these ] { chars } (block of 20) end . txt
        # t_p_w_s_a_a_t_c [20_underscores] e_t
        # Counting underscores:
        # test_path_with_spaces_and_all_these_chars -> 10 underscores from / \ . ( ) [ ] { }
        # :;, '\"`!@#$%^&*+=|~ -> 20 chars, all replaced by _ (space is also in regex via \s)
        # end_txt -> 1 underscore from .
        # Total = 10 + 20 + 1 = 31 underscores
        self.assertEqual(create_file_id(test_str), "file_test_path_with_spaces_and_all_these_chars____________________end_txt")

    def test_specific_prompt_special_chars(self):
        # This test addresses the specific string from the prompt:
        # "!@#$%^&*()+-={}[]|\:";',.<>?~\`py"
        # Using the regex: r"[/\.\\\s\(\)\[\]\{\}:;,'\"`!@#\$%\^&\*\+=\|~]"
        # Characters NOT in this regex and thus preserved: - < > ?
        # Characters IN this regex and replaced by _: !@#$%^&*()+={}[]|\:";',.~` and \ (backslash)
        # Input: "!@#$%^&*()+-={}[]|\:";',.<>?~\`py"
        # Breakdown:
        # !@#$%^&*()+  -> ___________ (11 underscores)
        # -            -> - (preserved)
        # =            -> _ (1 underscore)
        # {}           -> __ (2 underscores)
        # []           -> __ (2 underscores)
        # |            -> _ (1 underscore)
        # \            -> _ (1 underscore, due to \\ in regex)
        # :            -> _ (1 underscore)
        # ;            -> _ (1 underscore)
        # '            -> _ (1 underscore)
        # ,            -> _ (1 underscore)
        # .            -> _ (1 underscore)
        # <            -> < (preserved)
        # >            -> > (preserved)
        # ?            -> ? (preserved)
        # ~            -> _ (1 underscore)
        # `            -> _ (1 underscore, backtick)
        # py           -> py (preserved)
        # Concatenated: ___________-_.__.___\_________<>?__py
        # Total underscores: 11+1+2+2+1+1+1+1+1+1+1+1+1 = 25
        expected = "file____________-_-__-_\_________<>?__py"
        self.assertEqual(create_file_id("!@#$%^&*()+-={}[]|\:";',.<>?~\`py"), expected)

    def test_path_with_unhandled_special_chars_like_angle_brackets(self):
        # Characters like < > ? are not in the regex r"[/\.\\\s\(\)\[\]\{\}:;,'\"`!@#\$%\^&\*\+=\|~]"
        # and should remain.
        test_str = "file/path_with<angle_brackets>and?question.mark"
        # Expected: file_file_path_with<angle_brackets>and?question_mark
        # / replaced by _
        # . replaced by _
        # < > ? should remain
        # \s is not present here.
        self.assertEqual(create_file_id(test_str), "file_file_path_with<angle_brackets>and?question_mark")


if __name__ == '__main__':
    unittest.main()

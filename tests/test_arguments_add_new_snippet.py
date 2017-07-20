import sys


class TestArgumentsAddNewSnippet(object):

    def test_no_value(self):
        from cuma.config import Arguments
        sys.argv = ["cuma"]
        obj = Arguments()
        assert obj.get_snippet() == ''
        assert obj.get_tags() == ''
        assert obj.get_comment() == ''

    def test_valid_value_no_tags(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        sys.argv = ["cuma", "-s", command]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == ''
        assert obj.get_comment() == ''

    def test_valid_value_one_tag(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == ''

    def test_valid_value_with_tags(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == ''

    def test_valid_value_with_tags_and_comment(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-t", tags, "-c", comment]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == tags
        assert obj.get_comment() == comment

    def test_valid_value_with_comment_no_tags(self):
        from cuma.config import Arguments
        command = "'docker rm $(docker ps -a -q)'"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-c", comment]
        obj = Arguments()
        assert obj.get_snippet() == command
        assert obj.get_tags() == ''
        assert obj.get_comment() == comment

    @classmethod
    def setup_class(cls):
        print('setup_class()')

        sys.argv = ["cuma"]

    @classmethod
    def teardown_class(cls):
        print('teardown_class()')

        sys.argv = ["cuma"]

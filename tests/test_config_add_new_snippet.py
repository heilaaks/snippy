import sys


class TestConfigAddNewSnippet(object):

    def test_no_value(self):
        from cuma.config import Config
        sys.argv = ["cuma"]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert len(obj.get_snippet()) == 0
        assert len(obj.get_tags()) == 0
        assert len(obj.get_comment()) == 0

    def test_valid_value_no_tags(self):
        from cuma.config import Config
        command = "'docker rm $(docker ps -a -q)'"
        sys.argv = ["cuma", "-s", command]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert len(obj.get_tags()) == 0
        assert len(obj.get_comment()) == 0

    def test_valid_value_one_tag(self):
        from cuma.config import Config
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 1
        assert len(obj.get_comment()) == 0

    def test_valid_value_with_tags(self):
        from cuma.config import Config
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        sys.argv = ["cuma", "-s", command, "-t", tags]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 3
        assert len(obj.get_comment()) == 0

    def test_valid_value_with_tags_and_comment(self):
        from cuma.config import Config
        command = "'docker rm $(docker ps -a -q)'"
        tags = "docker, image, cleanup"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-t", tags, "-c", comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert set(obj.get_tags()) == set(tags.split(','))
        assert len(obj.get_tags()) == 3
        assert obj.get_comment() == comment

    def test_valid_value_with_comment_no_tags(self):
        from cuma.config import Config
        command = "'docker rm $(docker ps -a -q)'"
        comment = "Remove docker container"
        sys.argv = ["cuma", "-s", command, "-c", comment]
        obj = Config()
        assert isinstance(obj.get_snippet(), str)
        assert isinstance(obj.get_tags(), list)
        assert isinstance(obj.get_comment(), str)
        assert obj.get_snippet() == command
        assert len(obj.get_tags()) == 0
        assert obj.get_comment() == comment

    @classmethod
    def setup_class(cls):
        print('setup_class()')
        sys.argv = ["cuma"]

    @classmethod
    def teardown_class(cls):
        print('teardown_class()')

        sys.argv = ["cuma"]

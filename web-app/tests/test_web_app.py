import pymongo

class Tests:

    def test_sanity_check(self):
        """
        Test debugging... making sure that we can run a simple test that always passes.
        """
        expected = True # the value we expect to be present
        actual = True # the value we see in reality
        assert actual == expected, "Expected True to be equal to True!"